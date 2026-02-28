import { useState } from "react"
import Navbar from "./components/Navbar"
import SinglePrediction from "./components/SinglePrediction"
import BulkPrediction from "./components/BulkPrediction"
import Comparison from "./components/Comparison"
import ModelInsights from "./components/ModelInsights"
import "./index.css"

export default function App() {
  const [activePage, setActivePage] = useState("single")

  const renderPage = () => {
    switch (activePage) {
      case "single":   return <SinglePrediction />
      case "bulk":     return <BulkPrediction />
      case "compare":  return <Comparison />
      case "insights": return <ModelInsights />
      default:         return <SinglePrediction />
    }
  }

  return (
    <div style={{ minHeight: "100vh", background: "var(--bg-primary)" }}>
      <Navbar activePage={activePage} setActivePage={setActivePage} />
      <main style={{ maxWidth: "1200px", margin: "0 auto", padding: "32px 24px" }}>
        {renderPage()}
      </main>
      <footer style={{
        textAlign:    "center",
        padding:      "24px",
        color:        "var(--text-secondary)",
        fontSize:     "13px",
        borderTop:    "1px solid var(--border)",
        marginTop:    "48px"
      }}>
      </footer>
    </div>
  )
}