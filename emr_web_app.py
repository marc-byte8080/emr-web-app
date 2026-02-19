# emr_web_app.py
import json
from datetime import datetime
from pathlib import Path

import streamlit as st
import streamlit as st
# =========================
# LOGIN (simple)
# =========================
USERS = {
    "admin": "admin123",
    "nurse": "nurse123",
    "student": "student123",
}

if "auth_ok" not in st.session_state:
    st.session_state.auth_ok = False
if "auth_user" not in st.session_state:
    st.session_state.auth_user = ""

def do_logout():
    st.session_state.auth_ok = False
    st.session_state.auth_user = ""
    st.rerun()

def login_screen():
    st.markdown(
        """
        <style>
          .login-wrap {
            max-width: 420px;
            margin: 8vh auto 0 auto;
            background: #0f2a52;
            border: 1px solid #143a6b;
            border-radius: 18px;
            padding: 22px 22px 18px 22px;
          }
          .login-title { font-size: 26px; font-weight: 900; color: #e5e7eb; margin-bottom: 6px; }
          .login-sub { color: #94a3b8; margin-bottom: 16px; }
          .login-note { color: #94a3b8; font-size: 12px; margin-top: 10px; }
        </style>
        <div class="login-wrap">
          <div class="login-title">Hospital EMR Login</div>
          <div class="login-sub">Enter your username and password to continue.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Inputs
    u = st.text_input("Username", placeholder="e.g., nurse")
    p = st.text_input("Password", type="password", placeholder="••••••••")

    col1, col2 = st.columns([1, 1])
    with col1:
        login_btn = st.button("Login", use_container_width=True)
    with col2:
        st.button("Clear", use_container_width=True, on_click=lambda: None)

    if login_btn:
        if u in USERS and p == USERS[u]:
            st.session_state.auth_ok = True
            st.session_state.auth_user = u
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.caption("Demo accounts: admin/admin123, nurse/nurse123, student/student123")

# If not logged in, show login screen and STOP the app here
if not st.session_state.auth_ok:
    login_screen()
    st.stop()

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Hospital EMR — Advanced Viewer",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ✅ Change this to your real JSON filename (must be in same folder as this .py)
DATA_FILE = "emr_data.json"

# =========================================================
# CSS (DARK THEME, NO TRANSPARENCY, HIDE WHITE HEADER BAR)
# =========================================================
st.markdown(
    """
<style>
/* ---- FULL PAGE LOCK ---- */
html, body, .stApp {
  background: #071a2f !important;
  color: #e6edf3 !important;
}

/* Remove the white header/top bar completely */
header[data-testid="stHeader"]{
  background: transparent !important;
  height: 0px !important;
  min-height: 0px !important;
  visibility: hidden !important;
}
div[data-testid="stToolbar"]{ visibility: hidden !important; height: 0px !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }

/* Main container spacing */
.block-container{
  padding-top: 1.1rem !important;
  padding-bottom: 1.1rem !important;
}

/* Sidebar */
section[data-testid="stSidebar"]{
  background: #081a33 !important;
  border-right: 1px solid #0f2a52 !important;
}
section[data-testid="stSidebar"] *{
  color: #e6edf3 !important;
}

/* Inputs */
input, textarea, div[data-baseweb="input"] input {
  background: #0f2646 !important;
  color: #e6edf3 !important;
  border: 1px solid #153a6d !important;
  border-radius: 10px !important;
}

/* Selectbox (BaseWeb) */
div[data-baseweb="select"] > div{
  background: #0f2646 !important;
  border: 1px solid #153a6d !important;
  border-radius: 10px !important;
  color: #e6edf3 !important;
}
div[data-baseweb="select"] *{ color: #e6edf3 !important; }

/* Buttons */
.stButton > button, .stDownloadButton > button{
  background: #115e9c !important;
  color: #e6edf3 !important;
  border: 0 !important;
  border-radius: 12px !important;
  padding: .65rem 1rem !important;
  font-weight: 700 !important;
}
.stButton > button:hover, .stDownloadButton > button:hover{
  background: #1b78c2 !important;
}

/* Headings */
.emr-title{
  font-size: 34px;
  font-weight: 900;
  letter-spacing: .5px;
  line-height: 1.05;
}
.emr-sub{
  color: #9bb7d6;
  margin-top: 6px;
}

/* Cards */
.emr-card{
  background: #0f2a52 !important;
  border: 1px solid #143a6b !important;
  border-radius: 16px !important;
  padding: 14px 14px !important;
  margin-bottom: 12px !important;
}

/* Viewer panel (big text) */
.emr-viewer{
  background: #071c35 !important;
  border: 1px solid #143a6b !important;
  border-radius: 18px !important;
  padding: 18px !important;
  font-family: Consolas, monospace !important;
  font-size: 15px !important;
  white-space: pre-wrap !important;
  line-height: 1.55 !important;
  color: #e6edf3 !important;
}

/* Audit */
.emr-audit{
  background: #071c35 !important;
  border: 1px solid #143a6b !important;
  border-radius: 14px !important;
  padding: 12px 14px !important;
  font-family: Consolas, monospace !important;
  font-size: 13px !important;
  white-space: pre-wrap !important;
  color: #cbd5e1 !important;
}

/* Section nav column (where you drew) */
.nav-wrap{
  background: #071c35 !important;
  border: 1px solid #143a6b !important;
  border-radius: 16px !important;
  padding: 12px 12px !important;
}

/* Radio styling (not perfect in Streamlit, but readable) */
div[role="radiogroup"] label{
  color: #e6edf3 !important;
}

/* Dataframe: force dark background (Streamlit/AgGrid styles vary, this helps a lot) */
div[data-testid="stDataFrame"]{
  background: #071c35 !important;
  border: 1px solid #143a6b !important;
  border-radius: 16px !important;
  padding: 10px !important;
}
div[data-testid="stDataFrame"] *{
  color: #e6edf3 !important;
}

/* Abnormal callout */
.abn{
  background: #7f1d1d !important;
  border: 1px solid #b91c1c !important;
  border-radius: 12px !important;
  padding: 10px 12px !important;
  color: #ffffff !important;
  font-weight: 800 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# HELPERS
# =========================================================
def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def audit(msg: str):
    st.session_state.audit_log.append(f"[{now_stamp()}] {msg}")


def load_records(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        st.error(
            f"Cannot find data file: {path}\n\n"
            f"Make sure it is in the SAME folder as emr_web_app.py"
        )
        st.stop()

    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        st.error(
            "Your JSON file exists, but it cannot be read.\n\n"
            f"Error: {e}\n\n"
            "Tip: JSON must use DOUBLE QUOTES, not single quotes."
        )
        st.stop()


def safe_get(d, key, default="Not indicated / No data provided"):
    return d.get(key, default) if isinstance(d, dict) else default


def format_kv(title: str, d: dict) -> str:
    lines = [title, "=" * len(title)]
    if not isinstance(d, dict) or not d:
        return "\n".join(lines + ["Not indicated / No data provided"])
    for k, v in d.items():
        lines.append(f"{k}: {v}")
    return "\n".join(lines)


def format_notes(notes: dict) -> str:
    fmt = safe_get(notes, "Format", "SOAP")
    lines = [f"NURSING NOTES ({fmt})", "====================="]
    for k in ["S", "O", "A", "P"]:
        lines.append(f"{k}: {safe_get(notes, k)}\n")
    lines.append(f"End-of-Shift: {safe_get(notes, 'End-of-Shift')}")
    return "\n".join(lines).strip()


def _to_float_maybe(x):
    if x is None:
        return None
    s = str(x).strip()
    if not s:
        return None
    for token in ["°c", "°C", "bpm", "cpm", "mmhg", "mmHg"]:
        s = s.replace(token, "")
    if "/" in s:
        s = s.split("/")[0].strip()
    cleaned = "".join(ch for ch in s if ch.isdigit() or ch in [".", "-"])
    try:
        return float(cleaned)
    except Exception:
        return None


def _systolic(bp):
    if bp is None:
        return None
    s = str(bp).replace("mmHg", "").replace("mmhg", "").strip()
    if "/" in s:
        return _to_float_maybe(s.split("/")[0].strip())
    return _to_float_maybe(s)


def is_abnormal(row: dict) -> bool:
    temp = _to_float_maybe(row.get("Temp"))
    pr = _to_float_maybe(row.get("PR"))
    rr = _to_float_maybe(row.get("RR"))
    sbp = _systolic(row.get("BP"))
    pain = _to_float_maybe(row.get("Pain"))
    return (
        (temp is not None and temp >= 38.0)
        or (pr is not None and pr >= 100)
        or (rr is not None and rr >= 24)
        or (sbp is not None and sbp >= 140)
        or (pain is not None and pain >= 7)
    )


def viewer(text: str):
    st.markdown(f'<div class="emr-viewer">{text}</div>', unsafe_allow_html=True)


# =========================================================
# STATE (prevents spammy audit entries)
# =========================================================
if "audit_log" not in st.session_state:
    st.session_state.audit_log = []
if "selected_pid" not in st.session_state:
    st.session_state.selected_pid = None
if "last_pid" not in st.session_state:
    st.session_state.last_pid = None
if "section" not in st.session_state:
    st.session_state.section = "A. Registration"
if "last_section" not in st.session_state:
    st.session_state.last_section = None
if "search_value" not in st.session_state:
    st.session_state.search_value = ""


# =========================================================
# LOAD JSON
# =========================================================
records = load_records(DATA_FILE)
patient_ids = list(records.keys())
if not patient_ids:
    st.error("Your JSON file is empty.")
    st.stop()

if st.session_state.selected_pid is None:
    st.session_state.selected_pid = patient_ids[0]

# audit open chart once
if st.session_state.last_pid != st.session_state.selected_pid:
    audit(f"Opened chart: {st.session_state.selected_pid}")
    st.session_state.last_pid = st.session_state.selected_pid

# =========================================================
# HEADER (title + search + export)
# =========================================================
h1, h2, h3 = st.columns([2.4, 2.2, 1.2], vertical_alignment="center")

with h1:
    st.markdown(
        '<div class="emr-title">HOSPITAL EMR SYSTEM —<br>ADVANCED VIEWER<br>(SIMULATION)</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="emr-sub">Dark hospital-style dashboard • Data loaded from JSON</div>',
        unsafe_allow_html=True,
    )

with h2:
    st.session_state.search_value = st.text_input(
        "Search Patient (ID or Name)",
        value=st.session_state.search_value,
        placeholder="Type here…",
    )

with h3:
    current = records.get(st.session_state.selected_pid, {})
    export_bytes = json.dumps(
        {st.session_state.selected_pid: current}, indent=2, ensure_ascii=False
    ).encode("utf-8")
    st.download_button(
        "Export JSON",
        data=export_bytes,
        file_name=f"EMR_{st.session_state.selected_pid}.json",
        mime="application/json",
        use_container_width=True,
    )

# =========================================================
# SIDEBAR (patient list + summary + problems)
# =========================================================
with st.sidebar:
    st.markdown("## PATIENTS")

    labels = []
    for pid in patient_ids:
        reg = records.get(pid, {}).get("registration", {})
        name = safe_get(reg, "Patient Name", "Not indicated")
        labels.append(f"{pid} — {name}")

    selected_label = st.selectbox(
        "Choose Patient",
        labels,
        index=patient_ids.index(st.session_state.selected_pid)
        if st.session_state.selected_pid in patient_ids
        else 0,
    )
    new_pid = selected_label.split(" — ")[0].strip()

    # Search match (updates selected patient)
    q = st.session_state.search_value.strip().lower()
    if q:
        for pid in patient_ids:
            reg = records.get(pid, {}).get("registration", {})
            name = safe_get(reg, "Patient Name", "").lower()
            if q in pid.lower() or q in name:
                new_pid = pid
                break

    if new_pid != st.session_state.selected_pid:
        st.session_state.selected_pid = new_pid
        audit(f"Selected patient: {new_pid}")

    p = records.get(st.session_state.selected_pid, {})
    reg = p.get("registration", {})

    st.markdown('<div class="emr-card">', unsafe_allow_html=True)
    st.markdown(f"### {safe_get(reg,'Patient Name','Not indicated')}")
    st.write(f"**Age:** {safe_get(reg,'Age')}")
    st.write(f"**Sex:** {safe_get(reg,'Sex')}")
    st.write(f"**Civil:** {safe_get(reg,'Civil Status')}")
    st.write(f"**Admission:** {safe_get(reg,'Date of Admission')} — {safe_get(reg,'Time of Admission')}")
    st.write("**Chief Complaint:**")
    st.write(f"{safe_get(reg,'Chief Complaint')}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### PROBLEM LIST")
    problems = p.get("problem_list", [])
    if problems:
        for pr in problems:
            st.write(f"• {pr}")
    else:
        st.caption("Not indicated / No data provided")

    st.caption("Abnormal flag (Flowsheet): Temp≥38, PR≥100, RR≥24, SBP≥140, Pain≥7")

    st.markdown("---")
    st.caption("**BY:**")
    st.caption("GROUP 3: BSN 2-2")
    st.caption("Members: OGALESCO, MARC RIJN" "/" " "
    "ABDUL, SANDRA" "/" " " "PADILLA, JESSICA" "/" " " "SUMAIT, RISHA" "/" " " "TEJERO MONALISA" "/" " " "YBIOSA, PRINCESS ERICKA")

# refresh patient object after sidebar changes
p = records.get(st.session_state.selected_pid, {})

# =========================================================
# MAIN AREA LAYOUT:
# LEFT = SECTION NAV (where you drew)
# RIGHT = CONTENT VIEWER / TABLES
# =========================================================
nav_col, main_col = st.columns([1.1, 4.2], vertical_alignment="top")

SECTION_LABELS = [
    "A. Registration",
    "B. Assessment",
    "C. Vital Signs",
    "D. I&O",
    "E. Medication",
    "F. Laboratory",
    "G. Imaging",
    "H. MAR",
    "I. Nursing Notes",
    "J. NCP",
    "K. Health Teaching",
    "L. Discharge Plan",
    "Flowsheet",
    "Audit Log",
]

with nav_col:
    st.markdown('<div class="nav-wrap">', unsafe_allow_html=True)
    st.markdown("### Sections")
    st.session_state.section = st.radio(
        "Choose section",
        SECTION_LABELS,
        index=SECTION_LABELS.index(st.session_state.section)
        if st.session_state.section in SECTION_LABELS
        else 0,
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

# audit section only when it changes (no spam)
if st.session_state.last_section != st.session_state.section:
    audit(f"Viewed section: {st.session_state.section}")
    st.session_state.last_section = st.session_state.section

# =========================================================
# RENDER SECTION CONTENT
# =========================================================
with main_col:
    sec = st.session_state.section

    if sec == "A. Registration":
        viewer(format_kv("REGISTRATION SHEET", p.get("registration", {})))

    elif sec == "B. Assessment":
        viewer(format_kv("HEALTH ASSESSMENT", p.get("health_assessment", {})))

    elif sec == "C. Vital Signs":
        st.subheader("VITAL SIGNS")
        st.dataframe(p.get("vitals", []), use_container_width=True)

    elif sec == "D. I&O":
        viewer(format_kv("INPUT / OUTPUT (I&O)", p.get("io", {})))

    elif sec == "E. Medication":
        st.subheader("MEDICATION")
        st.dataframe(p.get("meds", []), use_container_width=True)

    elif sec == "F. Laboratory":
        st.subheader("LABORATORY")
        st.dataframe(p.get("labs", []), use_container_width=True)

    elif sec == "G. Imaging":
        st.subheader("IMAGING")
        st.dataframe(p.get("imaging", []), use_container_width=True)

    elif sec == "H. MAR":
        st.subheader("MAR")
        st.dataframe(p.get("mar", []), use_container_width=True)

    elif sec == "I. Nursing Notes":
        viewer(format_notes(p.get("nursing_notes", {})))

    elif sec == "J. NCP":
        ncp = p.get("ncp", {})
        block = []
        block.append("NURSING CARE PLAN (NCP)")
        block.append("========================")
        block.append(f"Diagnosis (NANDA): {safe_get(ncp,'Diagnosis (NANDA)')}\n")
        block.append(f"Cues (S/O): {safe_get(ncp,'Cues (S/O)')}\n")
        block.append(f"Goals: {safe_get(ncp,'Goals')}\n")
        block.append("Interventions/Rationale:")
        for i, it in enumerate(ncp.get("Interventions/Rationale", []), start=1):
            block.append(f"  {i}. {it}")
        block.append(f"\nEvaluation: {safe_get(ncp,'Evaluation')}")
        viewer("\n".join(block))

    elif sec == "K. Health Teaching":
        viewer(format_kv("HEALTH TEACHING", p.get("health_teaching", {})))

    elif sec == "L. Discharge Plan":
        viewer(format_kv("DISCHARGE PLANNING", p.get("discharge_planning", {})))

    elif sec == "Flowsheet":
        st.subheader("FLOWSHEET")
        flows = p.get("flowsheet", [])
        if flows:
            if any(is_abnormal(row) for row in flows if isinstance(row, dict)):
                st.markdown('<div class="abn">ABNORMAL FLOWSHEET ENTRY DETECTED</div>', unsafe_allow_html=True)
            st.dataframe(flows, use_container_width=True)
        else:
            st.info("No flowsheet entries yet.")

    elif sec == "Audit Log":
        st.subheader("AUDIT LOG")
        if st.session_state.audit_log:
            st.markdown(
                f'<div class="emr-audit">{"\\n".join(st.session_state.audit_log[-200:])}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.caption("No audit entries yet.")
