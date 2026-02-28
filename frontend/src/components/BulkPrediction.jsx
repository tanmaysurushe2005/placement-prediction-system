import { useState } from "react"
import axios from "axios"

export default function BulkPrediction() {
  const [file,    setFile]    = useState(null)
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error,   setError]   = useState(null)

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
    setResults(null)
    setError(null)
  }

  const handlePredict = async () => {
    if (!file) return
    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const formData = new FormData()
      formData.append("file", file)
      const res = await axios.post("http://localhost:8000/predict/bulk", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      })
      setResults(res.data)
    } catch (err) {
      setError("Failed to connect to backend. Make sure FastAPI is running.")
    } finally {
      setLoading(false)
    }
  }

  const downloadResults = () => {
    if (!results) return
    const headers = ["Branch","Gender","CGPA","Placement","Probability (%)","Risk Level","Academic Score","Skill Score","Activity Score"]
    const rows = results.results.map(r => [
      r.branch, r.gender, r.cgpa,
      r.placed ? "Placed" : "Not Placed",
      r.probability, r.risk,
      r.scores?.academic_score,
      r.scores?.skill_score,
      r.scores?.activity_score
    ])
    const csv = [headers, ...rows].map(r => r.join(",")).join("\n")
    const link = document.createElement("a")
    link.href = URL.createObjectURL(new Blob([csv], { type: "text/csv" }))
    link.download = "placement_results.csv"
    link.click()
  }

  const getRiskClass = (risk) => {
    if (risk === "Low Risk")    return "risk-low"
    if (risk === "Medium Risk") return "risk-medium"
    return "risk-high"
  }

  const csvColumns = [
    "ssc_%", "hsc_%", "degree_%", "cgpa", "backlogs",
    "aptitude", "coding", "technical", "communication",
    "internships", "projects", "certs", "hackathons",
    "attendance", "extra", "work_exp", "branch", "gender"
  ]

  const csvSample = [
    "75.0", "70.0", "72.0", "7.5", "0",
    "65.0", "70.0", "68.0", "72.0",
    "1", "3", "2", "1",
    "85.0", "1", "0", "CSE", "Male"
  ]

  return (
    <div>
      <h1 className="page-title">📂 Bulk Prediction</h1>
      <p className="page-subtitle">Upload a CSV or Excel file to predict placement for multiple students at once</p>

      <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>

        {/* ── Upload Section ── */}
        <div className="card">
          <h3 className="section-title">📤 Upload Student Data</h3>

          <label
            htmlFor="file-upload"
            className="upload-area"
            style={{
              display:     "block",
              borderColor: file ? "var(--accent-green)" : "var(--border)",
            }}
          >
            <div style={{ fontSize: "48px", marginBottom: "12px" }}>
              {file ? "✅" : "📁"}
            </div>
            <div style={{ fontSize: "16px", fontWeight: "700", marginBottom: "8px" }}>
              {file ? file.name : "Click to upload CSV or Excel file"}
            </div>
            <div style={{ color: "var(--text-secondary)", fontSize: "13px" }}>
              {file
                ? `File selected — ${(file.size / 1024).toFixed(1)} KB`
                : "Supports .csv, .xlsx, .xls files"}
            </div>
            <input
              id="file-upload"
              type="file"
              accept=".csv,.xlsx,.xls"
              onChange={handleFileChange}
              style={{ display: "none" }}
            />
          </label>

          {file && (
            <button
              className="btn btn-primary btn-full"
              onClick={handlePredict}
              disabled={loading}
              style={{ marginTop: "16px" }}
            >
              {loading ? "Predicting..." : "🔮 Predict for All Students"}
            </button>
          )}
        </div>

        {/* ── Sample Format ── */}
        <div className="card">
          <h3 className="section-title">📋 Required CSV Format</h3>
          <div style={{
            overflowX:    "auto",
            borderRadius: "8px",
            border:       "1px solid var(--border)"
          }}>
            <table style={{ fontSize: "12px", whiteSpace: "nowrap" }}>
              <thead>
                <tr>
                  {csvColumns.map(h => (
                    <th key={h} style={{
                      padding:         "8px 12px",
                      background:      "var(--bg-hover)",
                      color:           "var(--accent-blue)",
                      fontSize:        "11px",
                      textTransform:   "uppercase",
                      letterSpacing:   "0.5px",
                      borderBottom:    "1px solid var(--border)"
                    }}>
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                <tr>
                  {csvSample.map((v, i) => (
                    <td key={i} style={{
                      padding:    "8px 12px",
                      color:      "var(--text-primary)",
                      background: "var(--bg-secondary)"
                    }}>
                      {v}
                    </td>
                  ))}
                </tr>
              </tbody>
            </table>
          </div>
          <p style={{
            color:     "var(--text-secondary)",
            fontSize:  "13px",
            marginTop: "12px"
          }}>
            ⚠️ Make sure your file column names match exactly as shown above.
          </p>
        </div>

        {/* ── Error ── */}
        {error && (
          <div className="alert alert-error">❌ {error}</div>
        )}

        {/* ── Loading ── */}
        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            Processing all students...
          </div>
        )}

        {/* ── Results ── */}
        {results && (
          <>
            {/* Summary Cards */}
            <div className="grid-4">
              <div className="metric-card">
                <div className="metric-value">{results.summary.total}</div>
                <div className="metric-label">Total Students</div>
              </div>
              <div className="metric-card">
                <div className="metric-value" style={{ color: "var(--accent-green)" }}>
                  {results.summary.placed}
                </div>
                <div className="metric-label">Likely Placed</div>
              </div>
              <div className="metric-card">
                <div className="metric-value" style={{ color: "var(--accent-orange)" }}>
                  {results.summary.not_placed}
                </div>
                <div className="metric-label">At Risk</div>
              </div>
              <div className="metric-card">
                <div className="metric-value" style={{ color: "var(--accent)" }}>
                  {results.summary.high_risk}
                </div>
                <div className="metric-label">High Risk</div>
              </div>
            </div>

            {/* Results Table */}
            <div className="card">
              <div style={{
                display:        "flex",
                justifyContent: "space-between",
                alignItems:     "center",
                marginBottom:   "16px"
              }}>
                <h3 className="section-title" style={{ marginBottom: 0 }}>
                  📊 Prediction Results
                </h3>
                <button className="btn btn-success" onClick={downloadResults}>
                  ⬇️ Download CSV
                </button>
              </div>

              <div className="table-container">
                <table>
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Branch</th>
                      <th>Gender</th>
                      <th>CGPA</th>
                      <th>Placement</th>
                      <th>Probability</th>
                      <th>Risk Level</th>
                      <th>Skill Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    {results.results.map((r, i) => (
                      <tr key={i}>
                        <td style={{ color: "var(--text-secondary)" }}>{i + 1}</td>
                        <td>{r.branch}</td>
                        <td>{r.gender}</td>
                        <td>{r.cgpa}</td>
                        <td>
                          <span style={{
                            color:      r.placed ? "var(--accent-green)" : "var(--accent)",
                            fontWeight: "700"
                          }}>
                            {r.placed ? "✅ Placed" : "❌ Not Placed"}
                          </span>
                        </td>
                        <td>
                          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                            <div className="progress-bar-container" style={{ width: "80px" }}>
                              <div
                                className="progress-bar-fill"
                                style={{ width: `${r.probability}%` }}
                              />
                            </div>
                            <span style={{ fontSize: "13px", fontWeight: "700" }}>
                              {r.probability}%
                            </span>
                          </div>
                        </td>
                        <td>
                          <span className={`risk-badge ${getRiskClass(r.risk)}`}>
                            {r.risk}
                          </span>
                        </td>
                        <td>{r.scores?.skill_score}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}