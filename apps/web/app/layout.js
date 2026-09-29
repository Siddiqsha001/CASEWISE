import './globals.css'
import './analysis.css'
import './auth.css'
export const metadata = { title: 'CaseWise AI', description: 'Legal case management and intelligence' }
export default function RootLayout({ children }) {
  return <html lang="en"><body>{children}</body></html>
}
