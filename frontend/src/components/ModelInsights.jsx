import { useState, useEffect } from "react"
import axios from "axios"

export default function ModelInsights() {
  const [modelInfo, setModelInfo] = useState(null)
  const [loading,   setLoading]   = useState(true)
  const [error,     setError]     = useState(null)

  useEffect(() => {
    const fetchModelInfo = async () => {
      try {
        const res = await axios.get("http://localhost:8000/model/info")
        setModelInfo(res.data)
      } catch (err) {
        setError("Failed to connect to backend. Make sure FastAPI is running.")
      } finally {
        setLoading(false)
      }
    }
    fetchModelInfo()
  }, [])

  const metrics = [
    { label: "Model Type",       value: "Random Forest Classifier", color: "var(--accent-blue)"   },
    { label: "Baseline Model",   value: "Logistic Regression",      color: "var(--accent-green)"  },
    { label: "Dataset",          value: "Kaggle Campus Placement",  color: "var(--accent-orange)" },
    { label: "Total Students",   value: "215 Records",              color: "var(--accent)"        },
  ]

  const features_info = [
    { category: "🎓 Academic",   items: ["SSC %", "HSC %", "Degree %", "CGPA", "Active Backlogs"]                                          },
    { category: "💡 Skills",     items: ["Aptitude Score", "Coding Score", "Technical Score", "Communication Score"]                        },
    { category: "🏆 Activities", items: ["Internships", "Projects", "Certifications", "Hackathons", "Work Experience"]                      },
    { category: "📊 Engagement", items: ["Attendance %", "Extracurricular"]                                                                 },
    { category: "🔢 Derived",    items: ["Academic Score (weighted)", "Skill Score (average)", "Activity Score (sum)"]                      },
    { category: "👤 Personal",   items: ["Branch", "Gender"]                                                                                },
  ]

  const whyRF = [
    { point: "Works extremely well on tabular student data"             },
    { point: "Handles non-linear relationships automatically"           },
    { point: "No heavy feature scaling needed"                          },
    { point: "Robust against noise and outliers"                        },
    { point: "Gives feature importance for explainability"              },
    { point: "Outperforms Logistic Regression on this dataset"          },
  ]

  const riskLevels = [
    { label: "🟢 Low Risk",    range: "Above 60%",    cls: "risk-low",    desc: "Strong placement chances"        },
    { label: "🟡 Medium Risk", range: "40% to 60%",   cls: "risk-medium", desc: "Needs improvement in some areas" },
    { label: "🔴 High Risk",   range: "Below 40%",    cls: "risk-high",   desc: "Immediate attention needed"      },
  ]

  return (
    <div>
      <h1 className="page-title">📊 Model Insights</h1>
      <p className="page-subtitle">Understand how the placement prediction model works</p>

      <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>

        {/* ── Model Overview ── */}
        <div className="grid-4">
          {metrics.map((m, i) => (
            <div key={i} className="metric-card" style={{ borderTop: `3px solid ${m.color}` }}>
              <div style={{ fontSize: "14px", fontWeight: "800", color: m.color, marginBottom: "6px" }}>
                {m.value}
              </div>
              <div className="metric-label">{m.label}</div>
            </div>
          ))}
        </div>

        {/* ── Model Info from API ── */}
        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            Loading model information...
          </div>
        )}

        {error && (
          <div className="alert alert-error">❌ {error}</div>
        )}

        {modelInfo && (
          <div className="card">
            <h3 className="section-title">🤖 Live Model Information</h3>
            <div className="grid-3">
              <div style={{ textAlign: "center", padding: "16px", background: "var(--bg-secondary)", borderRadius: "8px" }}>
                <div style={{ fontSize: "24px", fontWeight: "800", color: "var(--accent-blue)" }}>
                  {modelInfo.total_features}
                </div>
                <div style={{ fontSize: "13px", color: "var(--text-secondary)", marginTop: "4px" }}>
                  Total Features
                </div>
              </div>
              <div style={{ textAlign: "center", padding: "16px", background: "var(--bg-secondary)", borderRadius: "8px" }}>
                <div style={{ fontSize: "24px", fontWeight: "800", color: "var(--accent-green)" }}>
                  ~92%
                </div>
                <div style={{ fontSize: "13px", color: "var(--text-secondary)", marginTop: "4px" }}>
                  RF Accuracy
                </div>
              </div>
              <div style={{ textAlign: "center", padding: "16px", background: "var(--bg-secondary)", borderRadius: "8px" }}>
                <div style={{ fontSize: "24px", fontWeight: "800", color: "var(--accent-orange)" }}>
                  ~85%
                </div>
                <div style={{ fontSize: "13px", color: "var(--text-secondary)", marginTop: "4px" }}>
                  LR Accuracy
                </div>
              </div>
            </div>

            {/* Feature List */}
            <div style={{ marginTop: "20px" }}>
              <p style={{ color: "var(--text-secondary)", fontSize: "13px", marginBottom: "12px", textTransform: "uppercase", letterSpacing: "0.5px" }}>
                All Features Used
              </p>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                {modelInfo.features.map((f, i) => (
                  <span key={i} style={{
                    background:    "var(--bg-hover)",
                    color:         "var(--accent-blue)",
                    padding:       "4px 12px",
                    borderRadius:  "999px",
                    fontSize:      "12px",
                    fontWeight:    "600",
                    border:        "1px solid var(--border)"
                  }}>
                    {f}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* ── Feature Categories ── */}
        <div className="card">
          <h3 className="section-title">📋 Feature Categories</h3>
          <div className="grid-3">
            {features_info.map((cat, i) => (
              <div key={i} style={{
                background:    "var(--bg-secondary)",
                borderRadius:  "8px",
                padding:       "16px",
                border:        "1px solid var(--border)"
              }}>
                <div style={{ fontWeight: "700", marginBottom: "12px", fontSize: "14px" }}>
                  {cat.category}
                </div>
                {cat.items.map((item, j) => (
                  <div key={j} style={{
                    fontSize:     "13px",
                    color:        "var(--text-secondary)",
                    padding:      "4px 0",
                    borderBottom: j < cat.items.length - 1 ? "1px solid var(--border)" : "none"
                  }}>
                    → {item}
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>

        {/* ── Why Random Forest ── */}
        <div className="card">
          <h3 className="section-title">🌲 Why Random Forest?</h3>
          <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
            {whyRF.map((item, i) => (
              <div key={i} style={{
                display:       "flex",
                alignItems:    "center",
                gap:           "12px",
                padding:       "12px 16px",
                background:    "var(--bg-secondary)",
                borderRadius:  "8px",
                border:        "1px solid var(--border)"
              }}>
                <div style={{
                  width:          "28px",
                  height:         "28px",
                  borderRadius:   "50%",
                  background:     "linear-gradient(135deg, var(--accent-blue), var(--accent))",
                  display:        "flex",
                  alignItems:     "center",
                  justifyContent: "center",
                  fontSize:       "12px",
                  fontWeight:     "800",
                  flexShrink:     0
                }}>
                  {i + 1}
                </div>
                <div style={{ fontSize: "14px", color: "var(--text-primary)" }}>
                  {item.point}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* ── Risk Classification ── */}
        <div className="card">
          <h3 className="section-title">🚦 Risk Classification Logic</h3>
          <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
            {riskLevels.map((r, i) => (
              <div key={i} style={{
                display:        "flex",
                alignItems:     "center",
                justifyContent: "space-between",
                padding:        "16px 20px",
                background:     "var(--bg-secondary)",
                borderRadius:   "8px",
                border:         "1px solid var(--border)"
              }}>
                <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
                  <span className={`risk-badge ${r.cls}`}>{r.label}</span>
                  <span style={{ color: "var(--text-secondary)", fontSize: "14px" }}>{r.desc}</span>
                </div>
                <div style={{
                  fontSize:   "14px",
                  fontWeight: "700",
                  color:      "var(--accent-blue)"
                }}>
                  {r.range}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* ── Tech Stack ── */}
        <div className="card">
          <h3 className="section-title">🏗️ Tech Stack</h3>
          <div className="grid-4">
            {[
              { name: "Python",       role: "Core Language",  color: "var(--accent-blue)"   },
              { name: "scikit-learn", role: "ML Library",     color: "var(--accent-orange)" },
              { name: "FastAPI",      role: "Backend API",    color: "var(--accent-green)"  },
              { name: "React",        role: "Frontend UI",    color: "var(--accent)"        },
              { name: "Pandas",       role: "Data Handling",  color: "var(--accent-blue)"   },
              { name: "NumPy",        role: "Computation",    color: "var(--accent-orange)" },
              { name: "Vite",         role: "Build Tool",     color: "var(--accent-green)"  },
              { name: "Joblib",       role: "Model Storage",  color: "var(--accent)"        },
            ].map((t, i) => (
              <div key={i} style={{
                textAlign:     "center",
                padding:       "16px",
                background:    "var(--bg-secondary)",
                borderRadius:  "8px",
                border:        `1px solid ${t.color}33`
              }}>
                <div style={{ fontSize: "16px", fontWeight: "800", color: t.color, marginBottom: "4px" }}>
                  {t.name}
                </div>
                <div style={{ fontSize: "12px", color: "var(--text-secondary)" }}>
                  {t.role}
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  )
}

