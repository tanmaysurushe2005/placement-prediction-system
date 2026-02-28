import { useState } from "react"
import axios from "axios"

const initialForm = {
  ssc_percentage:                70,
  hsc_percentage:                70,
  degree_percentage:             70,
  cgpa:                          7.5,
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

export default function SinglePrediction() {
  const [form,    setForm]    = useState(initialForm)
  const [result,  setResult]  = useState(null)
  const [loading, setLoading] = useState(false)
  const [error,   setError]   = useState(null)

  const handleChange = (name, value) => {
    setForm(prev => ({ ...prev, [name]: value }))
  }

  const handlePredict = async () => {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const res = await axios.post("http://localhost:8000/predict", form)
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

  return (
    <div>
      <h1 className="page-title">🔮 Single Prediction</h1>
      <p className="page-subtitle">Enter student details to predict placement probability</p>

      <div className="grid-2">

        {/* ── LEFT — Input Form ── */}
        <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>

          {/* Academic */}
          <div className="card">
            <h3 className="section-title">🎓 Academic Information</h3>
            <SliderInput label="SSC Percentage (10th)"  name="ssc_percentage"    min={40}  max={100} step={0.5} value={form.ssc_percentage}    onChange={handleChange} />
            <SliderInput label="HSC Percentage (12th)"  name="hsc_percentage"    min={40}  max={100} step={0.5} value={form.hsc_percentage}    onChange={handleChange} />
            <SliderInput label="Degree Percentage"      name="degree_percentage" min={40}  max={100} step={0.5} value={form.degree_percentage} onChange={handleChange} />
            <SliderInput label="CGPA"                   name="cgpa"              min={4}   max={10}  step={0.1} value={form.cgpa}              onChange={handleChange} />
            <NumberInput label="Active Backlogs"        name="active_backlogs"   min={0}   max={10}             value={form.active_backlogs}   onChange={handleChange} />
          </div>

          {/* Skills */}
          <div className="card">
            <h3 className="section-title">💡 Skills & Assessment</h3>
            <SliderInput label="Aptitude Test Score"       name="aptitude_test_score"       min={0} max={100} value={form.aptitude_test_score}       onChange={handleChange} />
            <SliderInput label="Coding Test Score"         name="coding_test_score"         min={0} max={100} value={form.coding_test_score}         onChange={handleChange} />
            <SliderInput label="Technical Interview Score" name="technical_interview_score" min={0} max={100} value={form.technical_interview_score} onChange={handleChange} />
            <SliderInput label="Communication Score"       name="communication_score"       min={0} max={100} value={form.communication_score}       onChange={handleChange} />
          </div>

          {/* Activities */}
          <div className="card">
            <h3 className="section-title">🏆 Activities & Experience</h3>
            <NumberInput label="Internships Count"        name="internships_count"       min={0} max={10}  value={form.internships_count}       onChange={handleChange} />
            <NumberInput label="Projects Count"           name="projects_count"          min={0} max={20}  value={form.projects_count}          onChange={handleChange} />
            <NumberInput label="Certifications Count"     name="certifications_count"    min={0} max={20}  value={form.certifications_count}    onChange={handleChange} />
            <NumberInput label="Hackathons Participated"  name="hackathons_participated"  min={0} max={20}  value={form.hackathons_participated}  onChange={handleChange} />
            <NumberInput label="Work Experience (months)" name="work_experience_months"  min={0} max={24}  value={form.work_experience_months}  onChange={handleChange} />
          </div>

          {/* Personal */}
          <div className="card">
            <h3 className="section-title">👤 Personal Details</h3>
            <SliderInput label="Attendance Percentage" name="attendance_percentage" min={40} max={100} step={0.5} value={form.attendance_percentage} onChange={handleChange} />
            <SelectInput
              label="Extracurricular Participation"
              name="extracurricular_participation"
              value={form.extracurricular_participation}
              onChange={handleChange}
              options={[
                { value: 0, label: "No"  },
                { value: 1, label: "Yes" }
              ]}
            />
            <SelectInput
              label="Branch"
              name="branch"
              value={form.branch}
              onChange={handleChange}
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
              value={form.gender}
              onChange={handleChange}
              options={[
                { value: "Male",   label: "Male"   },
                { value: "Female", label: "Female" },
              ]}
            />
          </div>

          <button
            className="btn btn-primary btn-full"
            onClick={handlePredict}
            disabled={loading}
          >
            {loading ? "Predicting..." : "🔮 Predict Placement"}
          </button>
        </div>

        {/* ── RIGHT — Results ── */}
        <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>

          {/* Live Score Cards */}
          <div className="grid-3">
            <div className="metric-card">
              <div className="metric-value" style={{ fontSize: "20px" }}>
                {(0.3*form.ssc_percentage + 0.3*form.hsc_percentage + 0.4*form.degree_percentage).toFixed(1)}
              </div>
              <div className="metric-label">Academic Score</div>
            </div>
            <div className="metric-card">
              <div className="metric-value" style={{ fontSize: "20px" }}>
                {((form.aptitude_test_score + form.coding_test_score + form.technical_interview_score + form.communication_score) / 4).toFixed(1)}
              </div>
              <div className="metric-label">Skill Score</div>
            </div>
            <div className="metric-card">
              <div className="metric-value" style={{ fontSize: "20px" }}>
                {form.internships_count + form.projects_count + form.certifications_count + form.hackathons_participated}
              </div>
              <div className="metric-label">Activity Score</div>
            </div>
          </div>

          {/* Error */}
          {error && <div className="alert alert-error">❌ {error}</div>}

          {/* Loading */}
          {loading && (
            <div className="loading">
              <div className="spinner"></div>
              Predicting placement...
            </div>
          )}

          {/* Result */}
          {result && (
            <>
              {/* Main Result */}
              <div className={result.placed ? "result-placed" : "result-not-placed"}>
                <div style={{ fontSize: "40px", marginBottom: "8px" }}>
                  {result.placed ? "✅" : "❌"}
                </div>
                <div style={{ fontSize: "22px", fontWeight: "800", marginBottom: "8px" }}>
                  {result.placed ? "Likely to be PLACED" : "At Risk of NOT being Placed"}
                </div>
                <div style={{ fontSize: "32px", fontWeight: "800", color: result.placed ? "var(--accent-green)" : "var(--accent)" }}>
                  {result.probability}%
                </div>
                <div style={{ color: "var(--text-secondary)", marginBottom: "12px" }}>
                  Placement Probability
                </div>
                <div className="progress-bar-container">
                  <div
                    className="progress-bar-fill"
                    style={{ width: `${result.probability}%` }}
                  />
                </div>
                <div style={{ marginTop: "12px" }}>
                  <span className={`risk-badge ${getRiskClass(result.risk)}`}>
                    {result.risk}
                  </span>
                </div>
              </div>

              {/* Score Breakdown */}
              <div className="card">
                <h3 className="section-title">📊 Score Breakdown</h3>
                {[
                  { label: "Academic Score", value: result.scores.academic_score, max: 100 },
                  { label: "Skill Score",    value: result.scores.skill_score,    max: 100 },
                  { label: "Activity Score", value: result.scores.activity_score, max: 20  },
                ].map(item => (
                  <div key={item.label} style={{ marginBottom: "16px" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "6px" }}>
                      <span style={{ fontSize: "14px", color: "var(--text-secondary)" }}>{item.label}</span>
                      <span style={{ fontSize: "14px", fontWeight: "700" }}>{item.value}</span>
                    </div>
                    <div className="progress-bar-container">
                      <div
                        className="progress-bar-fill"
                        style={{ width: `${(item.value / item.max) * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>

              {/* Profile Summary */}
              <div className="card">
                <h3 className="section-title">📋 Profile Summary</h3>
                <div className="grid-3">
                  {[
                    { label: "CGPA",           value: form.cgpa           },
                    { label: "Backlogs",        value: form.active_backlogs },
                    { label: "Internships",     value: form.internships_count },
                    { label: "Projects",        value: form.projects_count },
                    { label: "Certifications",  value: form.certifications_count },
                    { label: "Attendance",      value: `${form.attendance_percentage}%` },
                  ].map(item => (
                    <div key={item.label} style={{ textAlign: "center", padding: "12px", background: "var(--bg-secondary)", borderRadius: "8px" }}>
                      <div style={{ fontSize: "20px", fontWeight: "800", color: "var(--accent-blue)" }}>{item.value}</div>
                      <div style={{ fontSize: "11px", color: "var(--text-secondary)", marginTop: "4px" }}>{item.label}</div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}

          {/* Placeholder when no result */}
          {!result && !loading && !error && (
            <div className="card" style={{ textAlign: "center", padding: "60px 24px" }}>
              <div style={{ fontSize: "60px", marginBottom: "16px" }}>🎓</div>
              <div style={{ fontSize: "18px", fontWeight: "700", marginBottom: "8px" }}>
                Ready to Predict
              </div>
              <div style={{ color: "var(--text-secondary)" }}>
                Fill in the student details and click Predict Placement
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

