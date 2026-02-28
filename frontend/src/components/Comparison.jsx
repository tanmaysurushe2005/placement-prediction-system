import { useState } from "react"
import axios from "axios"

const initialStudent = {
  ssc_percentage:                70,
  hsc_percentage:                70,
  degree_percentage:             70,
  cgpa:                          7.0,
  active_backlogs:               0,
  aptitude_test_score:           60,
  coding_test_score:             60,
  technical_interview_score:     60,
  communication_score:           60,
  internships_count:             0,
  projects_count:                2,
  certifications_count:          1,
  hackathons_participated:       0,
  attendance_percentage:         80,
  extracurricular_participation: 0,
  work_experience_months:        0,
  branch:                        "CSE",
  gender:                        "Male"
}

const SliderInput = ({ label, name, min, max, step=1, value, onChange }) => (
  <div className="input-group">
    <label>{label}</label>
    <input
      type="range"
      min={min} max={max} step={step}
      value={value}
      onChange={e => onChange(name, parseFloat(e.target.value))}
    />
    <span className="range-value">{value}</span>
  </div>
)

const NumberInput = ({ label, name, min, max, value, onChange }) => (
  <div className="input-group">
    <label>{label}</label>
    <input
      type="number"
      min={min} max={max}
      value={value}
      onChange={e => onChange(name, parseInt(e.target.value))}
    />
  </div>
)

const SelectInput = ({ label, name, options, value, onChange }) => (
  <div className="input-group">
    <label>{label}</label>
    <select value={value} onChange={e => onChange(name, e.target.value)}>
      {options.map(o => (
        <option key={o.value} value={o.value}>{o.label}</option>
      ))}
    </select>
  </div>
)

const StudentForm = ({ title, color, data, onChange }) => (
  <div className="card" style={{ borderTop: `3px solid ${color}` }}>
    <h3 style={{
      fontSize:     "18px",
      fontWeight:   "800",
      color:        color,
      marginBottom: "20px"
    }}>
      {title}
    </h3>

    <p style={{ color: "var(--text-secondary)", fontSize: "12px", marginBottom: "16px", textTransform: "uppercase", letterSpacing: "0.5px" }}>🎓 Academic</p>
    <SliderInput label="SSC %"         name="ssc_percentage"    min={40}  max={100} step={0.5} value={data.ssc_percentage}    onChange={onChange} />
    <SliderInput label="HSC %"         name="hsc_percentage"    min={40}  max={100} step={0.5} value={data.hsc_percentage}    onChange={onChange} />
    <SliderInput label="Degree %"      name="degree_percentage" min={40}  max={100} step={0.5} value={data.degree_percentage} onChange={onChange} />
    <SliderInput label="CGPA"          name="cgpa"              min={4}   max={10}  step={0.1} value={data.cgpa}              onChange={onChange} />
    <NumberInput label="Backlogs"      name="active_backlogs"   min={0}   max={10}             value={data.active_backlogs}   onChange={onChange} />

    <hr className="divider" />

    <p style={{ color: "var(--text-secondary)", fontSize: "12px", marginBottom: "16px", textTransform: "uppercase", letterSpacing: "0.5px" }}>💡 Skills</p>
    <SliderInput label="Aptitude"      name="aptitude_test_score"       min={0} max={100} value={data.aptitude_test_score}       onChange={onChange} />
    <SliderInput label="Coding"        name="coding_test_score"         min={0} max={100} value={data.coding_test_score}         onChange={onChange} />
    <SliderInput label="Technical"     name="technical_interview_score" min={0} max={100} value={data.technical_interview_score} onChange={onChange} />
    <SliderInput label="Communication" name="communication_score"       min={0} max={100} value={data.communication_score}       onChange={onChange} />

    <hr className="divider" />

    <p style={{ color: "var(--text-secondary)", fontSize: "12px", marginBottom: "16px", textTransform: "uppercase", letterSpacing: "0.5px" }}>🏆 Activities</p>
    <NumberInput label="Internships"    name="internships_count"       min={0} max={10} value={data.internships_count}       onChange={onChange} />
    <NumberInput label="Projects"       name="projects_count"          min={0} max={20} value={data.projects_count}          onChange={onChange} />
    <NumberInput label="Certifications" name="certifications_count"    min={0} max={20} value={data.certifications_count}    onChange={onChange} />
    <NumberInput label="Hackathons"     name="hackathons_participated"  min={0} max={20} value={data.hackathons_participated}  onChange={onChange} />
    <NumberInput label="Work Exp (mo)"  name="work_experience_months"  min={0} max={24} value={data.work_experience_months}  onChange={onChange} />

    <hr className="divider" />

    <p style={{ color: "var(--text-secondary)", fontSize: "12px", marginBottom: "16px", textTransform: "uppercase", letterSpacing: "0.5px" }}>👤 Personal</p>
    <SliderInput label="Attendance %" name="attendance_percentage" min={40} max={100} step={0.5} value={data.attendance_percentage} onChange={onChange} />
    <SelectInput
      label="Extracurricular"
      name="extracurricular_participation"
      value={data.extracurricular_participation}
      onChange={onChange}
      options={[{ value: 0, label: "No" }, { value: 1, label: "Yes" }]}
    />
    <SelectInput
      label="Branch"
      name="branch"
      value={data.branch}
      onChange={onChange}
      options={[
        { value: "CSE",        label: "CSE"        },
        { value: "IT",         label: "IT"         },
        { value: "ECE",        label: "ECE"        },
        { value: "Mechanical", label: "Mechanical" },
        { value: "Civil",      label: "Civil"      },
      ]}
    />
    <SelectInput
      label="Gender"
      name="gender"
      value={data.gender}
      onChange={onChange}
      options={[
        { value: "Male",   label: "Male"   },
        { value: "Female", label: "Female" },
      ]}
    />
  </div>
)

export default function Comparison() {
  const [student1, setStudent1] = useState({ ...initialStudent, cgpa: 7.5, coding_test_score: 75 })
  const [student2, setStudent2] = useState({ ...initialStudent, cgpa: 6.5, coding_test_score: 50, active_backlogs: 1 })
  const [result,   setResult]   = useState(null)
  const [loading,  setLoading]  = useState(false)
  const [error,    setError]    = useState(null)

  const handleChange1 = (name, value) => setStudent1(prev => ({ ...prev, [name]: value }))
  const handleChange2 = (name, value) => setStudent2(prev => ({ ...prev, [name]: value }))

  const handleCompare = async () => {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const res = await axios.post("http://localhost:8000/compare", {
        student1, student2
      })
      setResult(res.data)
    } catch (err) {
      setError("Failed to connect to backend. Make sure FastAPI is running.")
    } finally {
      setLoading(false)
    }
  }

  const getRiskClass = (risk) => {
    if (risk === "Low Risk")    return "risk-low"
    if (risk === "Medium Risk") return "risk-medium"
    return "risk-high"
  }

  const metrics = result ? [
    { label: "Placement %",    s1: result.student1.probability,          s2: result.student2.probability,          suffix: "%"  },
    { label: "Academic Score", s1: result.student1.scores.academic_score, s2: result.student2.scores.academic_score, suffix: ""   },
    { label: "Skill Score",    s1: result.student1.scores.skill_score,    s2: result.student2.scores.skill_score,    suffix: ""   },
    { label: "Activity Score", s1: result.student1.scores.activity_score, s2: result.student2.scores.activity_score, suffix: ""   },
  ] : []

  return (
    <div>
      <h1 className="page-title">🆚 Student Comparison</h1>
      <p className="page-subtitle">Compare two students side by side to see who has better placement chances</p>

      {/* ── Student Forms ── */}
      <div className="grid-2" style={{ marginBottom: "24px" }}>
        <StudentForm
          title="👤 Student 1"
          color="var(--accent-blue)"
          data={student1}
          onChange={handleChange1}
        />
        <StudentForm
          title="👤 Student 2"
          color="var(--accent-orange)"
          data={student2}
          onChange={handleChange2}
        />
      </div>

      {/* ── Compare Button ── */}
      <button
        className="btn btn-primary btn-full"
        onClick={handleCompare}
        disabled={loading}
        style={{ marginBottom: "24px", padding: "16px" }}
      >
        {loading ? "Comparing..." : "🆚 Compare Students"}
      </button>

      {/* ── Error ── */}
      {error && <div className="alert alert-error">❌ {error}</div>}

      {/* ── Loading ── */}
      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          Comparing students...
        </div>
      )}

      {/* ── Results ── */}
      {result && (
        <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>

          {/* Result Cards */}
          <div className="grid-2">
            {[
              { label: "👤 Student 1", data: result.student1, color: "var(--accent-blue)"   },
              { label: "👤 Student 2", data: result.student2, color: "var(--accent-orange)" },
            ].map((s, i) => (
              <div key={i} className="card" style={{ borderTop: `3px solid ${s.color}`, textAlign: "center" }}>
                <h3 style={{ color: s.color, marginBottom: "16px", fontSize: "18px", fontWeight: "800" }}>
                  {s.label}
                </h3>
                <div style={{ fontSize: "48px", marginBottom: "8px" }}>
                  {s.data.placed ? "✅" : "❌"}
                </div>
                <div style={{ fontSize: "18px", fontWeight: "700", marginBottom: "12px" }}>
                  {s.data.placed ? "Likely PLACED" : "At Risk"}
                </div>
                <div style={{ fontSize: "36px", fontWeight: "800", color: s.color, marginBottom: "8px" }}>
                  {s.data.probability}%
                </div>
                <div style={{ color: "var(--text-secondary)", fontSize: "13px", marginBottom: "12px" }}>
                  Placement Probability
                </div>
                <div className="progress-bar-container">
                  <div className="progress-bar-fill" style={{ width: `${s.data.probability}%` }} />
                </div>
                <div style={{ marginTop: "12px" }}>
                  <span className={`risk-badge ${getRiskClass(s.data.risk)}`}>
                    {s.data.risk}
                  </span>
                </div>
              </div>
            ))}
          </div>

          {/* Verdict */}
          <div className="card" style={{
            textAlign:  "center",
            background: "linear-gradient(135deg, rgba(67,97,238,0.1), rgba(233,69,96,0.1))",
            border:     "1px solid var(--accent-blue)"
          }}>
            <div style={{ fontSize: "32px", marginBottom: "8px" }}>🏆</div>
            <div style={{ fontSize: "20px", fontWeight: "800", color: "var(--accent-yellow)" }}>
              {result.verdict}
            </div>
          </div>

          {/* Score Comparison Bars */}
          <div className="card">
            <h3 className="section-title">📊 Score Comparison</h3>
            {metrics.map(m => (
              <div key={m.label} style={{ marginBottom: "20px" }}>
                <div style={{
                  display:        "flex",
                  justifyContent: "space-between",
                  marginBottom:   "8px",
                  fontSize:       "13px",
                  fontWeight:     "700"
                }}>
                  <span style={{ color: "var(--accent-blue)" }}>
                    S1: {m.s1}{m.suffix}
                  </span>
                  <span style={{ color: "var(--text-secondary)" }}>{m.label}</span>
                  <span style={{ color: "var(--accent-orange)" }}>
                    S2: {m.s2}{m.suffix}
                  </span>
                </div>
                <div style={{ display: "flex", gap: "4px", alignItems: "center" }}>
                  {/* Student 1 bar */}
                  <div style={{ flex: 1 }}>
                    <div style={{
                      height:       "10px",
                      borderRadius: "999px",
                      background:   "var(--bg-secondary)",
                      overflow:     "hidden"
                    }}>
                      <div style={{
                        height:       "100%",
                        width:        `${Math.min((m.s1 / 100) * 100, 100)}%`,
                        background:   "var(--accent-blue)",
                        borderRadius: "999px",
                        transition:   "width 0.5s ease",
                        float:        "right"
                      }} />
                    </div>
                  </div>
                  <div style={{ width: "8px", height: "8px", background: "var(--border)", borderRadius: "50%" }} />
                  {/* Student 2 bar */}
                  <div style={{ flex: 1 }}>
                    <div style={{
                      height:       "10px",
                      borderRadius: "999px",
                      background:   "var(--bg-secondary)",
                      overflow:     "hidden"
                    }}>
                      <div style={{
                        height:       "100%",
                        width:        `${Math.min((m.s2 / 100) * 100, 100)}%`,
                        background:   "var(--accent-orange)",
                        borderRadius: "999px",
                        transition:   "width 0.5s ease"
                      }} />
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Detailed Table */}
          <div className="card">
            <h3 className="section-title">📋 Detailed Comparison Table</h3>
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Metric</th>
                    <th style={{ color: "var(--accent-blue)" }}>Student 1</th>
                    <th style={{ color: "var(--accent-orange)" }}>Student 2</th>
                    <th>Winner</th>
                  </tr>
                </thead>
                <tbody>
                  {[
                    { metric: "Placement %",    s1: result.student1.probability,          s2: result.student2.probability,          higher: true  },
                    { metric: "Academic Score", s1: result.student1.scores.academic_score, s2: result.student2.scores.academic_score, higher: true  },
                    { metric: "Skill Score",    s1: result.student1.scores.skill_score,    s2: result.student2.scores.skill_score,    higher: true  },
                    { metric: "Activity Score", s1: result.student1.scores.activity_score, s2: result.student2.scores.activity_score, higher: true  },
                  ].map((row, i) => {
                    const s1Wins = row.higher ? row.s1 > row.s2 : row.s1 < row.s2
                    const s2Wins = row.higher ? row.s2 > row.s1 : row.s2 < row.s1
                    return (
                      <tr key={i}>
                        <td style={{ fontWeight: "600" }}>{row.metric}</td>
                        <td style={{
                          color:      s1Wins ? "var(--accent-green)" : "var(--text-primary)",
                          fontWeight: s1Wins ? "700" : "400"
                        }}>
                          {row.s1}
                        </td>
                        <td style={{
                          color:      s2Wins ? "var(--accent-green)" : "var(--text-primary)",
                          fontWeight: s2Wins ? "700" : "400"
                        }}>
                          {row.s2}
                        </td>
                        <td>
                          {s1Wins ? (
                            <span style={{ color: "var(--accent-blue)", fontWeight: "700" }}>👤 S1</span>
                          ) : s2Wins ? (
                            <span style={{ color: "var(--accent-orange)", fontWeight: "700" }}>👤 S2</span>
                          ) : (
                            <span style={{ color: "var(--text-secondary)" }}>🤝 Tie</span>
                          )}
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Placeholder */}
      {!result && !loading && !error && (
        <div className="card" style={{ textAlign: "center", padding: "60px 24px" }}>
          <div style={{ fontSize: "60px", marginBottom: "16px" }}>🆚</div>
          <div style={{ fontSize: "18px", fontWeight: "700", marginBottom: "8px" }}>
            Ready to Compare
          </div>
          <div style={{ color: "var(--text-secondary)" }}>
            Fill in both student details and click Compare Students
          </div>
        </div>
      )}
    </div>
  )
}