"""Provider boundaries for local and future AI implementations."""
import os
from typing import Protocol

import httpx


class LLMProvider(Protocol):
    model: str
    async def generate_answer(self, prompt: str) -> str: ...
    async def generate_structured_output(self, prompt: str) -> dict: ...


class EmbeddingProvider(Protocol):
    def embed(self, texts: list[str]) -> list[list[float]]: ...


class OllamaProvider:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5:0.5b")

    async def generate_answer(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(f"{self.base_url}/api/generate", json={"model": self.model, "prompt": prompt, "stream": False})
            response.raise_for_status()
            return response.json().get("response", "").strip()

    async def generate_structured_output(self, prompt: str) -> dict:
        import json
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(f"{self.base_url}/api/generate", json={"model": self.model, "prompt": prompt, "stream": False, "format": "json"})
            response.raise_for_status()
            return json.loads(response.json().get("response", "{}"))


class GeminiProvider:
    """Gemini REST adapter; the API key is sent only from the AI container."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.answer_model = os.getenv("GEMINI_ANSWER_MODEL", "gemini-2.5-flash")
        self.analysis_model = os.getenv("GEMINI_ANALYSIS_MODEL", self.answer_model)
        self.model = self.analysis_model

    async def _generate(self, prompt: str, model: str, structured: bool = False) -> str:
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to the ignored .env file.")
        payload = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
        if structured:
            payload["generationConfig"] = {"responseMimeType": "application/json"}
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                headers={"x-goog-api-key": self.api_key},
                json=payload,
            )
            response.raise_for_status()
            parts = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [])
        answer = "".join(part.get("text", "") for part in parts).strip()
        if not answer:
            raise RuntimeError("Gemini returned no answer")
        return answer

    async def generate_answer(self, prompt: str) -> str:
        return await self._generate(prompt, self.answer_model)

    async def generate_structured_output(self, prompt: str) -> dict:
        import json
        return json.loads(await self._generate(prompt, self.analysis_model, structured=True))


class LocalBGEProvider:
    def __init__(self):
        self.model_name = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
        self._model = None

    def embed(self, texts: list[str]) -> list[list[float]]:
        if self._model is None:
            from fastembed import TextEmbedding
            self._model = TextEmbedding(model_name=self.model_name)
        return [vector.tolist() for vector in self._model.embed(texts)]


llm_provider: LLMProvider = GeminiProvider() if os.getenv("LLM_PROVIDER", "ollama").lower() == "gemini" else OllamaProvider()
embedding_provider: EmbeddingProvider = LocalBGEProvider()
