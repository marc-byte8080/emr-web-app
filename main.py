import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

# -----------------------------
# Scenario-based EMR (ONLY data given; missing -> Not indicated / No data provided)
# -----------------------------
PATIENTS = {
    "ML-2026-001": {
        "registration": {
            "Patient Name": "Marie Lopez",
            "Age": "27 years old",
            "Sex": "Female",
            "Civil Status": "In a long-term relationship",
            "Address": "Confidential – Simulation",
            "Date of Admission": "Feb 5, 2026",
            "Time of Admission": "08:45 AM",
            "Chief Complaint": "Left lower abdominal pain",
            "Admitting Diagnosis": "Probable Ruptured Ovarian Cyst",
            "Allergies": "NKA",
            "Attending Physician": "On-duty MD",
        },
        "health_assessment": {
            "General Appearance": "Awake, alert, not in acute distress.",
            "Neurologic (LOC/GCS)": "Awake/alert; GCS: Not indicated (No data provided).",
            "Respiratory": "RR 16 cpm; other respiratory assessment: No data provided.",
            "Cardiovascular": "HR 76 bpm; BP 122/70; other CV assessment: No data provided.",
            "Gastrointestinal": (
                "Abdomen slightly distended; tenderness suprapubic & left iliac fossa; "
                "mild rebound tenderness; no guarding; no palpable masses."
            ),
            "Genitourinary": "Denies urinary symptoms; other GU data: No data provided.",
            "Musculoskeletal": "No data provided.",
            "Skin Integrity": "No data provided.",
            "Pain": "Left iliac fossa/LLQ pain; Pain score 3/10 at time of assessment.",
        },
        "problem_list": [
            "Probable ruptured ovarian cyst",
            "Acute abdominal pain (improving per patient report)"
        ],
        "vitals": [
            {
                "Date/Time": "Feb 5, 2026 – Initial assessment (time not indicated)",
                "BP": "122/70 mmHg",
                "Temp": "37.8 °C",
                "PR": "76 bpm",
                "RR": "16 cpm",
                "SpO2": "Not indicated (No data provided)"
            }
        ],
        "io": {
            "Oral Intake": "No data provided.",
            "IV Fluids": "PNSS 1 liter IV, KVO (rate not indicated).",
            "Urine Output": "No data provided.",
            "Stool Output": "No data provided."
        },
        "meds": [
            {
                "Generic Name": "0.9% Sodium Chloride (PNSS)",
                "Dose": "1 liter",
                "Route": "IV",
                "Frequency": "KVO",
                "Indication": "Maintain IV access / hydration support as ordered.",
                "Nursing Considerations": "Monitor IV site; monitor for fluid overload as indicated."
            }
        ],
        "labs": [
            {"Test": "Complete Blood Count (CBC)", "Date Requested": "Feb 5, 2026", "Result": "Pending / No data provided"},
            {"Test": "Serum β-hCG (Pregnancy Test)", "Date Requested": "Feb 5, 2026", "Result": "Pending / No data provided"},
            {"Test": "Urinalysis", "Date Requested": "Feb 5, 2026", "Result": "Pending / No data provided"},
            {"Test": "Blood Typing and Rh Factor", "Date Requested": "Feb 5, 2026", "Result": "Pending / No data provided"},
        ],
        "imaging": [
            {"Type": "Transvaginal Ultrasound (UTZ)", "Date Ordered": "Feb 5, 2026", "Result": "Pending official reading"}
        ],
        "mar": [
            {
                "Date/Time": "Not indicated (No data provided)",
                "Medication": "PNSS 0.9% NaCl",
                "Dose": "1 liter",
                "Route": "IV",
                "Nurse Initials": "Not indicated",
                "Remarks": "KVO as ordered; no further administration data provided."
            }
        ],
        "nursing_notes": {
            "Format": "SOAP",
            "S": "Reports LLQ/left iliac fossa pain; nausea and loss of appetite prior to admission. Denies vaginal bleeding/discharge; denies urinary/bowel symptoms.",
            "O": "Awake, alert, not in acute distress. Pain score 3/10. Abdomen slightly distended; tenderness suprapubic & left iliac fossa; mild rebound; no guarding.",
            "A": "Probable ruptured ovarian cyst; acute abdominal pain (improving per patient report).",
            "P": "Monitor VS; ensure PNSS KVO per MD order; provide comfort measures; prepare for labs & UTZ; ongoing assessment.",
            "End-of-Shift": "Stable; pain improved per report; diagnostics pending."
        },
        "ncp": {
            "Diagnosis (NANDA)": "Acute Pain r/t suspected ovarian cyst rupture AEB LLQ pain and abdominal tenderness.",
            "Cues (S/O)": "S: sudden LLQ pain, nausea, anorexia. O: tenderness LLQ/suprapubic; mild rebound; pain 3/10 at assessment.",
            "Goals": "Patient will report decreased pain and maintain stable VS while awaiting diagnostic results.",
            "Interventions/Rationale": [
                "Assess pain regularly to evaluate trends and response to comfort measures.",
                "Maintain PNSS KVO as ordered to support IV access while diagnostics are ongoing.",
                "Promote comfort positioning and reduce stimuli to help decrease pain perception.",
                "Monitor VS and abdominal findings for worsening pain or instability."
            ],
            "Evaluation": "Partially met: pain improved compared with initial episode; continue monitoring."
        },
        "health_teaching": {
            "Topic": "Condition overview (possible ovarian cyst rupture), diagnostics (labs/UTZ), warning signs to report.",
            "Method": "Verbal instruction.",
            "Response": "Verbalized understanding; teach-back: Not indicated (No data provided)."
        },
        "discharge_planning": {
            "Medications": "Not indicated (No data provided).",
            "Diet": "Not indicated (No data provided).",
            "Activity": "Not indicated (No data provided).",
            "Follow-up": "Not indicated (No data provided).",
            "Seek Help If": "Not indicated (No data provided)."
        },

        # FLOWSHEET (time-based charting)
        "flowsheet": [
            {
                "Date/Time": "Feb 5, 2026 09:00",
                "Temp": "37.8",
                "PR": "76",
                "RR": "16",
                "BP": "122/70",
                "Pain": "3",
                "Notes": "Initial assessment; stable. Awaiting diagnostics."
            }
        ]
    }
}


# -----------------------------
# UI Theme
# -----------------------------
BG = "#0f172a"
PANEL = "#111f36"
CARD = "#162a46"
CARD2 = "#0b223d"
TEXT = "#e5e7eb"
MUTED = "#9ca3af"
ACCENT = "#22d3ee"
HILITE = "#fbbf24"

ABNORMAL_BG = "#7f1d1d"   # deep red
ABNORMAL_FG = "#ffffff"

def now_stamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# -----------------------------
# Helpers for abnormal detection
# -----------------------------
def _to_float_maybe(x):
    """Try to convert strings like '37.8 °C', '110 bpm', '8/10' to float."""
    if x is None:
        return None
    s = str(x).strip()
    if not s:
        return None

    # remove common units
    for token in ["°c", "°C", "bpm", "cpm", "mmhg", "mmHg"]:
        s = s.replace(token, "")

    # pain like "8/10"
    if "/" in s:
        try:
            s = s.split("/")[0].strip()
        except Exception:
            pass

    # keep digits, dot, minus
    cleaned = []
    for ch in s:
        if ch.isdigit() or ch in [".", "-"]:
            cleaned.append(ch)
        elif ch == " ":
            continue
    s2 = "".join(cleaned)

    try:
        return float(s2)
    except Exception:
        return None


def _systolic(bp_value):
    """Extract systolic from '122/70' or '122/70 mmHg'."""
    if bp_value is None:
        return None
    s = str(bp_value).strip()
    # remove units
    s = s.replace("mmHg", "").replace("mmhg", "").strip()
    if "/" in s:
        left = s.split("/")[0].strip()
        return _to_float_maybe(left)
    return _to_float_maybe(s)


def is_abnormal_flowsheet_row(r: dict) -> bool:
    """
    Simple adult thresholds (demo):
    Temp >= 38.0
    PR >= 100
    RR >= 24
    SBP >= 140
    Pain >= 7
    """
    temp = _to_float_maybe(r.get("Temp"))
    pr = _to_float_maybe(r.get("PR"))
    rr = _to_float_maybe(r.get("RR"))
    sbp = _systolic(r.get("BP"))
    pain = _to_float_maybe(r.get("Pain"))

    if temp is not None and temp >= 38.0:
        return True
    if pr is not None and pr >= 100:
        return True
    if rr is not None and rr >= 24:
        return True
    if sbp is not None and sbp >= 140:
        return True
    if pain is not None and pain >= 7:
        return True
    return False


# -----------------------------
# App
# -----------------------------
class EMRApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Hospital EMR Dashboard (Simulation) — Advanced + Flowsheet Highlights")
        self.root.geometry("1400x780")
        self.root.configure(bg=BG)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("TFrame", background=BG)
        self.style.configure("TLabel", background=BG, foreground=TEXT)
        self.style.configure("TLabelframe", background=BG, foreground=TEXT)
        self.style.configure("TLabelframe.Label", background=BG, foreground=TEXT, font=("Segoe UI", 10, "bold"))
        self.style.configure("TNotebook", background=BG, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=PANEL, foreground=TEXT, padding=(12, 8))
        self.style.map("TNotebook.Tab", background=[("selected", CARD)], foreground=[("selected", ACCENT)])
        self.style.configure("Treeview", background=CARD2, fieldbackground=CARD2, foreground=TEXT, rowheight=26, borderwidth=0)
        self.style.configure("Treeview.Heading", background=PANEL, foreground=TEXT, relief="flat", font=("Segoe UI", 10, "bold"))
        self.style.map("Treeview.Heading", background=[("active", PANEL)])

        self.current_patient_id = list(PATIENTS.keys())[0]

        self.build_header()
        self.build_main()
        self.load_patient(self.current_patient_id)

        self.audit(f"Opened chart: {self.current_patient_id}")

    # ---------- Header ----------
    def build_header(self):
        header = tk.Frame(self.root, bg="#08213f", height=64)
        header.pack(fill="x")

        tk.Label(
            header,
            text="HOSPITAL EMR SYSTEM — ADVANCED VIEWER (SIMULATION)",
            bg="#08213f", fg=TEXT, font=("Segoe UI", 16, "bold")
        ).pack(side="left", padx=18, pady=14)

        right = tk.Frame(header, bg="#08213f")
        right.pack(side="right", padx=14)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            right, textvariable=self.search_var,
            bg=CARD, fg=TEXT, insertbackground=TEXT,
            relief="flat", width=32, font=("Segoe UI", 11)
        )
        search_entry.pack(side="left", padx=(0, 8), pady=14)
        search_entry.bind("<Return>", lambda e: self.search_patient())

        tk.Button(
            right, text="Search",
            bg="#115e9c", fg=TEXT, relief="flat",
            activebackground="#1b78c2", activeforeground=TEXT,
            command=self.search_patient
        ).pack(side="left", padx=6, pady=14)

        tk.Button(
            right, text="Export JSON",
            bg="#115e9c", fg=TEXT, relief="flat",
            activebackground="#1b78c2", activeforeground=TEXT,
            command=self.export_json
        ).pack(side="left", padx=6, pady=14)

    # ---------- Main Layout ----------
    def build_main(self):
        self.body = tk.Frame(self.root, bg=BG)
        self.body.pack(fill="both", expand=True)

        # Left sidebar
        self.sidebar = tk.Frame(self.body, bg=PANEL, width=320)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(self.sidebar, text="PATIENTS", bg=PANEL, fg=TEXT, font=("Segoe UI", 11, "bold")).pack(
            anchor="w", padx=14, pady=(16, 8)
        )

        self.patient_list = tk.Listbox(
            self.sidebar, bg=CARD2, fg=TEXT, relief="flat",
            highlightthickness=0, selectbackground="#1f6aa5", selectforeground=TEXT,
            height=6
        )
        self.patient_list.pack(fill="x", padx=14, pady=(0, 14))
        for pid, pdata in PATIENTS.items():
            self.patient_list.insert(tk.END, f"{pid} — {pdata['registration']['Patient Name']}")
        self.patient_list.bind("<<ListboxSelect>>", self.on_select_patient)
        self.patient_list.select_set(0)

        # Summary card
        self.summary_card = tk.Frame(self.sidebar, bg=CARD)
        self.summary_card.pack(fill="x", padx=14, pady=(0, 14))

        self.lbl_name = tk.Label(self.summary_card, text="", bg=CARD, fg=TEXT, font=("Segoe UI", 14, "bold"))
        self.lbl_name.pack(anchor="w", padx=12, pady=(10, 2))

        self.lbl_demo = tk.Label(self.summary_card, text="", bg=CARD, fg=MUTED, font=("Segoe UI", 10))
        self.lbl_demo.pack(anchor="w", padx=12)

        self.lbl_adm = tk.Label(self.summary_card, text="", bg=CARD, fg=MUTED, font=("Segoe UI", 10))
        self.lbl_adm.pack(anchor="w", padx=12)

        tk.Label(self.summary_card, text="Chief Complaint:", bg=CARD, fg=TEXT, font=("Segoe UI", 10, "bold")).pack(
            anchor="w", padx=12, pady=(8, 0)
        )
        self.lbl_cc = tk.Label(self.summary_card, text="", bg=CARD, fg=HILITE, wraplength=280, justify="left",
                               font=("Segoe UI", 10, "bold"))
        self.lbl_cc.pack(anchor="w", padx=12, pady=(0, 12))

        # Problem list
        self.problem_frame = tk.LabelFrame(self.sidebar, text="PROBLEM LIST", bg=PANEL, fg=TEXT)
        self.problem_frame.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        self.problem_listbox = tk.Listbox(
            self.problem_frame, bg=CARD2, fg=TEXT, relief="flat",
            highlightthickness=0, selectbackground=CARD2, height=10
        )
        self.problem_listbox.pack(fill="both", expand=True, padx=10, pady=10)

        # Right content
        self.content = tk.Frame(self.body, bg=BG)
        self.content.pack(side="right", fill="both", expand=True)

        self.notebook = ttk.Notebook(self.content)
        self.notebook.pack(fill="both", expand=True, padx=16, pady=(16, 10))
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        # Tabs
        self.tab_overview = ttk.Frame(self.notebook)
        self.tab_assessment = ttk.Frame(self.notebook)
        self.tab_vitals = ttk.Frame(self.notebook)
        self.tab_io = ttk.Frame(self.notebook)
        self.tab_meds = ttk.Frame(self.notebook)
        self.tab_labs = ttk.Frame(self.notebook)
        self.tab_imaging = ttk.Frame(self.notebook)
        self.tab_mar = ttk.Frame(self.notebook)
        self.tab_flowsheet = ttk.Frame(self.notebook)
        self.tab_notes = ttk.Frame(self.notebook)
        self.tab_ncp = ttk.Frame(self.notebook)
        self.tab_teaching = ttk.Frame(self.notebook)
        self.tab_discharge = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_overview, text="Overview")
        self.notebook.add(self.tab_assessment, text="Assessment")
        self.notebook.add(self.tab_vitals, text="Vitals")
        self.notebook.add(self.tab_io, text="I&O")
        self.notebook.add(self.tab_meds, text="Meds")
        self.notebook.add(self.tab_labs, text="Labs")
        self.notebook.add(self.tab_imaging, text="Imaging")
        self.notebook.add(self.tab_mar, text="MAR")
        self.notebook.add(self.tab_flowsheet, text="Flowsheet")
        self.notebook.add(self.tab_notes, text="Nursing Notes")
        self.notebook.add(self.tab_ncp, text="NCP")
        self.notebook.add(self.tab_teaching, text="Health Teaching")
        self.notebook.add(self.tab_discharge, text="Discharge Plan")

        # Audit log
        audit_wrap = tk.Frame(self.content, bg=BG)
        audit_wrap.pack(fill="x", padx=16, pady=(0, 16))

        tk.Label(audit_wrap, text="AUDIT LOG", bg=BG, fg=TEXT, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.audit_text = tk.Text(
            audit_wrap, height=5, bg=CARD2, fg=TEXT, insertbackground=TEXT,
            relief="flat", highlightthickness=0, font=("Consolas", 10)
        )
        self.audit_text.pack(fill="x", pady=(6, 0))
        self.audit_text.config(state="disabled")

        self.build_tabs()

    # ---------- Tab builders ----------
    def build_tabs(self):
        self.txt_overview = self.make_readonly_text(self.tab_overview)
        self.txt_assessment = self.make_readonly_text(self.tab_assessment)
        self.txt_io = self.make_readonly_text(self.tab_io)
        self.txt_notes = self.make_readonly_text(self.tab_notes)
        self.txt_ncp = self.make_readonly_text(self.tab_ncp)
        self.txt_teaching = self.make_readonly_text(self.tab_teaching)
        self.txt_discharge = self.make_readonly_text(self.tab_discharge)

        # Tables
        self.vitals_tree = self.make_tree(self.tab_vitals, ["Date/Time", "BP", "Temp", "PR", "RR", "SpO2"])
        self.meds_tree = self.make_tree(self.tab_meds, ["Generic Name", "Dose", "Route", "Frequency", "Indication", "Nursing Considerations"])
        self.labs_tree = self.make_tree(self.tab_labs, ["Test", "Date Requested", "Result"])
        self.imaging_tree = self.make_tree(self.tab_imaging, ["Type", "Date Ordered", "Result"])
        self.mar_tree = self.make_tree(self.tab_mar, ["Date/Time", "Medication", "Dose", "Route", "Nurse Initials", "Remarks"])

        # FLOWSHEET: table + entry form
        flowsheet_container = tk.Frame(self.tab_flowsheet, bg=BG)
        flowsheet_container.pack(fill="both", expand=True)

        self.flowsheet_tree = self.make_tree(
            flowsheet_container,
            ["Date/Time", "Temp", "PR", "RR", "BP", "Pain", "Notes"]
        )

        # Tag style for abnormal rows (applies to flowsheet tree)
        self.flowsheet_tree.tag_configure("abnormal", background=ABNORMAL_BG, foreground=ABNORMAL_FG)

        form = tk.Frame(flowsheet_container, bg=BG)
        form.pack(fill="x", padx=10, pady=10)

        def mk_label(text):
            return tk.Label(form, text=text, bg=BG, fg=TEXT, font=("Segoe UI", 10, "bold"))

        self.fs_temp = tk.Entry(form, width=10, bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat")
        self.fs_pr = tk.Entry(form, width=10, bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat")
        self.fs_rr = tk.Entry(form, width=10, bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat")
        self.fs_bp = tk.Entry(form, width=14, bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat")
        self.fs_pain = tk.Entry(form, width=8, bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat")
        self.fs_notes = tk.Entry(form, width=38, bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat")

        mk_label("Temp").pack(side="left")
        self.fs_temp.pack(side="left", padx=6)

        mk_label("PR").pack(side="left")
        self.fs_pr.pack(side="left", padx=6)

        mk_label("RR").pack(side="left")
        self.fs_rr.pack(side="left", padx=6)

        mk_label("BP").pack(side="left")
        self.fs_bp.pack(side="left", padx=6)

        mk_label("Pain").pack(side="left")
        self.fs_pain.pack(side="left", padx=6)

        mk_label("Notes").pack(side="left")
        self.fs_notes.pack(side="left", padx=6)

        tk.Button(
            form,
            text="Add Entry",
            bg="#115e9c", fg=TEXT, relief="flat",
            activebackground="#1b78c2", activeforeground=TEXT,
            command=self.add_flowsheet_entry
        ).pack(side="left", padx=10)

        tk.Label(
            flowsheet_container,
            text="Abnormal auto-flag: Temp≥38, PR≥100, RR≥24, SBP≥140, Pain≥7",
            bg=BG, fg=MUTED, font=("Segoe UI", 9)
        ).pack(anchor="w", padx=14, pady=(0, 8))

    def make_readonly_text(self, parent):
        frame = tk.Frame(parent, bg=BG)
        frame.pack(fill="both", expand=True)

        text = tk.Text(
            frame, bg=CARD2, fg=TEXT, insertbackground=TEXT, wrap="word",
            relief="flat", highlightthickness=0, font=("Segoe UI", 11)
        )
        yscroll = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=yscroll.set)

        text.pack(side="left", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")
        text.config(state="disabled")
        return text

    def make_tree(self, parent, columns):
        frame = tk.Frame(parent, bg=BG)
        frame.pack(fill="both", expand=True, padx=8, pady=8)

        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=170, anchor="w")
        tree.pack(side="left", fill="both", expand=True)

        yscroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=yscroll.set)
        yscroll.pack(side="right", fill="y")

        return tree

    # ---------- Flowsheet ----------
    def add_flowsheet_entry(self):
        pid = self.current_patient_id
        p = PATIENTS[pid]

        entry = {
            "Date/Time": datetime.now().strftime("%b %d, %Y %H:%M"),
            "Temp": self.fs_temp.get().strip() or "Not indicated",
            "PR": self.fs_pr.get().strip() or "Not indicated",
            "RR": self.fs_rr.get().strip() or "Not indicated",
            "BP": self.fs_bp.get().strip() or "Not indicated",
            "Pain": self.fs_pain.get().strip() or "Not indicated",
            "Notes": self.fs_notes.get().strip() or ""
        }

        p.setdefault("flowsheet", []).append(entry)

        self.fill_tree(
            self.flowsheet_tree,
            p["flowsheet"],
            ["Date/Time", "Temp", "PR", "RR", "BP", "Pain", "Notes"],
            highlight_flowsheet=True
        )

        # clear fields
        for w in [self.fs_temp, self.fs_pr, self.fs_rr, self.fs_bp, self.fs_pain, self.fs_notes]:
            w.delete(0, tk.END)

        self.audit("Added flowsheet entry")

    # ---------- Data -> UI ----------
    def load_patient(self, patient_id: str):
        self.current_patient_id = patient_id
        p = PATIENTS[patient_id]
        reg = p["registration"]

        # Summary
        self.lbl_name.config(text=reg["Patient Name"])
        self.lbl_demo.config(text=f"Age: {reg['Age']}   |   Sex: {reg['Sex']}   |   Civil: {reg['Civil Status']}")
        self.lbl_adm.config(text=f"Admission: {reg['Date of Admission']} — {reg['Time of Admission']}")
        self.lbl_cc.config(text=reg["Chief Complaint"])

        # Problem list
        self.problem_listbox.delete(0, tk.END)
        for item in p.get("problem_list", []):
            self.problem_listbox.insert(tk.END, f"• {item}")

        # Text tabs
        self.set_text(self.txt_overview, self.format_overview(p))
        self.set_text(self.txt_assessment, self.format_kv_block("HEALTH ASSESSMENT", p["health_assessment"]))
        self.set_text(self.txt_io, self.format_kv_block("INPUT / OUTPUT (I&O)", p["io"]))
        self.set_text(self.txt_notes, self.format_notes(p["nursing_notes"]))
        self.set_text(self.txt_ncp, self.format_ncp(p["ncp"]))
        self.set_text(self.txt_teaching, self.format_kv_block("HEALTH TEACHING", p["health_teaching"]))
        self.set_text(self.txt_discharge, self.format_kv_block("DISCHARGE PLANNING", p["discharge_planning"]))

        # Tables
        self.fill_tree(self.vitals_tree, p["vitals"], ["Date/Time", "BP", "Temp", "PR", "RR", "SpO2"])
        self.fill_tree(self.meds_tree, p["meds"], ["Generic Name", "Dose", "Route", "Frequency", "Indication", "Nursing Considerations"])
        self.fill_tree(self.labs_tree, p["labs"], ["Test", "Date Requested", "Result"])
        self.fill_tree(self.imaging_tree, p["imaging"], ["Type", "Date Ordered", "Result"])
        self.fill_tree(self.mar_tree, p["mar"], ["Date/Time", "Medication", "Dose", "Route", "Nurse Initials", "Remarks"])

        # Flowsheet (with abnormal highlighting)
        self.fill_tree(
            self.flowsheet_tree,
            p.get("flowsheet", []),
            ["Date/Time", "Temp", "PR", "RR", "BP", "Pain", "Notes"],
            highlight_flowsheet=True
        )

    def fill_tree(self, tree, rows, cols, highlight_flowsheet=False):
        for item in tree.get_children():
            tree.delete(item)
 
        for r in rows:
            values = [r.get(c, "Not indicated") for c in cols]
            tags = ()

            # ✅ Abnormal row highlight ONLY for flowsheet
            if highlight_flowsheet:
                if is_abnormal_flowsheet_row(r):
                    tags = ("abnormal",)

            tree.insert("", tk.END, values=values, tags=tags)

    def set_text(self, widget: tk.Text, content: str):
        widget.config(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert("1.0", content)
        widget.config(state="disabled")

    # ---------- Formatters ----------
    def format_overview(self, p):
        reg = p["registration"]
        lines = []
        lines.append("REGISTRATION SHEET")
        lines.append("===================")
        for k, v in reg.items():
            lines.append(f"{k}: {v}")
        lines.append("")
        lines.append("HPI (SCENARIO)")
        lines.append("==============")
        lines.append(p["nursing_notes"].get("S", "No data provided"))
        lines.append("")
        lines.append("INITIAL MD IMPRESSION")
        lines.append("=====================")
        lines.append(reg.get("Admitting Diagnosis", "Not indicated"))
        return "\n".join(lines)

    def format_kv_block(self, title, dct):
        lines = [title, "=" * len(title)]
        for k, v in dct.items():
            lines.append(f"{k}: {v}")
        return "\n".join(lines)

    def format_notes(self, notes):
        lines = [f"NURSING NOTES ({notes.get('Format','Not indicated')})", "====================="]
        for k in ["S", "O", "A", "P"]:
            lines.append(f"{k}: {notes.get(k,'Not indicated')}\n")
        lines.append(f"End-of-Shift: {notes.get('End-of-Shift','Not indicated')}")
        return "\n".join(lines).strip()

    def format_ncp(self, ncp):
        lines = ["NURSING CARE PLAN (NCP)", "========================"]
        lines.append(f"Diagnosis (NANDA): {ncp.get('Diagnosis (NANDA)','Not indicated')}\n")
        lines.append(f"Cues (S/O): {ncp.get('Cues (S/O)','Not indicated')}\n")
        lines.append(f"Goals/Expected Outcomes: {ncp.get('Goals','Not indicated')}\n")
        lines.append("Interventions with Rationale:")
        for i, item in enumerate(ncp.get("Interventions/Rationale", []), start=1):
            lines.append(f"  {i}. {item}")
        lines.append(f"\nEvaluation: {ncp.get('Evaluation','Not indicated')}")
        return "\n".join(lines)

    # ---------- Events ----------
    def on_select_patient(self, event):
        if not self.patient_list.curselection():
            return
        selected = self.patient_list.get(self.patient_list.curselection())
        patient_id = selected.split(" — ")[0].strip()
        self.load_patient(patient_id)
        self.audit(f"Selected patient: {patient_id}")

    def on_tab_changed(self, event):
        tab_text = self.notebook.tab(self.notebook.select(), "text")
        self.audit(f"Viewed section: {tab_text}")

    def audit(self, msg: str):
        line = f"[{now_stamp()}] {msg}"
        self.audit_text.config(state="normal")
        self.audit_text.insert(tk.END, line + "\n")
        self.audit_text.see(tk.END)
        self.audit_text.config(state="disabled")

    def search_patient(self):
        q = self.search_var.get().strip().lower()
        if not q:
            messagebox.showinfo("Search", "Type a Patient ID or Name, then press Enter.")
            return

        for idx in range(self.patient_list.size()):
            item = self.patient_list.get(idx)
            if q in item.lower():
                self.patient_list.select_clear(0, tk.END)
                self.patient_list.select_set(idx)
                self.patient_list.event_generate("<<ListboxSelect>>")
                self.audit(f"Searched: '{q}' → matched {item.split(' — ')[0].strip()}")
                return

        messagebox.showwarning("Search", f"No patient matched: {q}")
        self.audit(f"Searched: '{q}' → no match")

    # ---------- Export ----------
    def export_json(self):
        pid = self.current_patient_id
        data = PATIENTS[pid]

        export = {
            "A. REGISTRATION SHEET": data["registration"],
            "B. HEALTH ASSESSMENT": data["health_assessment"],
            "C. VITAL SIGNS": data["vitals"],
            "D. INPUT / OUTPUT (I&O)": data["io"],
            "E. MEDICATION": data["meds"],
            "F. LABORATORY RESULTS": data["labs"],
            "G. IMAGING RESULTS": data["imaging"],
            "H. MAR": data["mar"],
            "Flowsheet": data.get("flowsheet", []),
            "I. NURSING NOTES": data["nursing_notes"],
            "J. NCP": data["ncp"],
            "K. HEALTH TEACHING": data["health_teaching"],
            "L. DISCHARGE PLANNING": data["discharge_planning"],
        }

        default_name = f"EMR_{pid}.json"
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            initialfile=default_name,
            filetypes=[("JSON files", "*.json")]
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(export, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Export", f"Saved JSON:\n{path}")
            self.audit(f"Exported JSON for {pid}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))
            self.audit(f"Export failed: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = EMRApp(root)
    root.mainloop()















