export default function Navbar({ activePage, setActivePage }) {
  const navItems = [
    { id: "single",   label: "🔮 Single Prediction" },
    { id: "bulk",     label: "📂 Bulk Prediction"   },
    { id: "compare",  label: "🆚 Comparison"         },
    { id: "insights", label: "📊 Model Insights"     },
  ]

  return (
    <nav style={{
      background:   "var(--bg-secondary)",
      borderBottom: "1px solid var(--border)",
      padding:      "0 24px",
      position:     "sticky",
      top:          0,
      zIndex:       100,
      boxShadow:    "0 2px 20px rgba(0,0,0,0.3)"
    }}>
      <div style={{
        maxWidth:       "1200px",
        margin:         "0 auto",
        display:        "flex",
        alignItems:     "center",
        justifyContent: "space-between",
        height:         "64px"
      }}>

        {/* Logo */}
        <div style={{
          fontSize:   "20px",
          fontWeight: "800",
          background: "linear-gradient(135deg, #4361ee, #e94560)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor:  "transparent"
        }}>
          🎓 PlacementAI
        </div>

        {/* Nav Links */}
        <div style={{ display: "flex", gap: "4px" }}>
          {navItems.map(item => (
            <button
              key={item.id}
              onClick={() => setActivePage(item.id)}
              style={{
                background:   activePage === item.id
                                ? "linear-gradient(135deg, var(--accent-blue), var(--accent))"
                                : "transparent",
                color:        activePage === item.id
                                ? "white"
                                : "var(--text-secondary)",
                border:       "none",
                borderRadius: "8px",
                padding:      "8px 16px",
                fontSize:     "14px",
                fontWeight:   activePage === item.id ? "700" : "500",
                cursor:       "pointer",
                transition:   "all 0.2s ease",
              }}
              onMouseEnter={e => {
                if (activePage !== item.id) {
                  e.target.style.background = "var(--bg-hover)"
                  e.target.style.color      = "white"
                }
              }}
              onMouseLeave={e => {
                if (activePage !== item.id) {
                  e.target.style.background = "transparent"
                  e.target.style.color      = "var(--text-secondary)"
                }
              }}
            >
              {item.label}
            </button>
          ))}
        </div>
      </div>
    </nav>
  )
}