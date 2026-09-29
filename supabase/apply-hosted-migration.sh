#!/bin/sh
set -eu

if [ -z "${SUPABASE_DB_URL:-}" ]; then
  echo "SUPABASE_DB_URL is required for the hosted database."
  exit 1
fi

if ! state=$(psql "$SUPABASE_DB_URL" -Atqc "SELECT CASE WHEN to_regclass('public.casewise_schema_migrations') IS NOT NULL THEN 'applied' WHEN to_regclass('public.cases') IS NOT NULL OR to_regclass('public.profiles') IS NOT NULL THEN 'partial' ELSE 'empty' END" 2>&1); then
  echo "PostgreSQL connection diagnostic (credentials redacted):"
  printf '%s\n' "$state" | sed -E 's#(postgres(ql)?://)[^@[:space:]]+@#\1[redacted]@#g; s#(password=)[^[:space:]]+#\1[redacted]#g'
  case "$state" in
    *"no usable address"*|*"could not translate host name"*)
      echo "The database host is not reachable from this Docker network. Check the Session pooler host in .env."
      ;;
    *"password authentication failed"*)
      echo "Check the database password in the Session pooler URI. URL-encode special characters such as @ as %40."
      ;;
    *"Tenant or user not found"*)
      echo "Check the pooler username and region against the exact Session pooler URI in Supabase Dashboard → Connect."
      ;;
    *)
      echo "Could not connect to Supabase PostgreSQL. Use the diagnostic above to check TLS, host, port, and credentials."
      ;;
  esac
  exit 2
fi

case "$state" in
  applied)
    echo "CaseWise schema already applied."
    ;;
  empty)
    echo "Applying CaseWise schema to the hosted PostgreSQL database."
    psql "$SUPABASE_DB_URL" -v ON_ERROR_STOP=1 -1 -f /migrations/20260929_casewise_hosted.sql
    ;;
  partial)
    echo "CaseWise tables already exist without the migration marker. Inspect the database before applying changes."
    exit 1
    ;;
  *)
    echo "Could not determine hosted schema state."
    exit 1
    ;;
esac
