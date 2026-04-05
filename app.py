"""
Virtual Study Session Participation and Remote Focus Ability Survey
"""

import streamlit as st
import json
import csv
import io
import re
import os
from datetime import datetime, date

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Remote Focus Survey",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stApp {
    background: linear-gradient(160deg, #0d1b2a 0%, #1b2a3b 55%, #0a3d62 100%) !important;
    min-height: 100vh;
}

.block-container {
    max-width: 700px !important;
    padding: 2.5rem 1.5rem 4rem !important;
}

#MainMenu, footer, header { visibility: hidden; }

.page-title {
    color: #ffffff;
    font-size: 2rem;
    font-weight: 800;
    text-align: center;
    margin: 0 0 0.15rem;
}
.page-sub {
    color: #90e0ef;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    text-align: center;
    margin-bottom: 1.6rem;
}

.info-box {
    background: rgba(0,180,216,0.12);
    border-left: 4px solid #00b4d8;
    border-radius: 0 14px 14px 0;
    padding: 0.9rem 1.2rem;
    color: #caf0f8;
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 1.4rem;
}

.q-chip {
    display: inline-block;
    background: #00b4d8;
    color: #fff;
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 0.2rem 0.75rem;
    border-radius: 99px;
    margin-bottom: 0.4rem;
}

/* ── TEXT INPUTS ── */
div[data-baseweb="input"] {
    background: #f1f5f9 !important;
    border: 2px solid #cbd5e1 !important;
    border-radius: 12px !important;
}
div[data-baseweb="input"]:focus-within {
    border-color: #00b4d8 !important;
    box-shadow: 0 0 0 3px rgba(0,180,216,0.2) !important;
}
div[data-baseweb="input"] input,
div[data-baseweb="base-input"] input,
input[type="text"],
input[type="date"] {
    background: transparent !important;
    color: #0d1b2a !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.97rem !important;
    border: none !important;
    box-shadow: none !important;
    caret-color: #00b4d8 !important;
}
input::placeholder {
    color: #94a3b8 !important;
    font-weight: 400 !important;
    opacity: 1 !important;
}
div[data-baseweb="base-input"] {
    background: #f1f5f9 !important;
    border-radius: 12px !important;
}
div[data-testid="stDateInput"] > div {
    background: #f1f5f9 !important;
    border: 2px solid #cbd5e1 !important;
    border-radius: 12px !important;
}
div[data-testid="stDateInput"] input {
    color: #0d1b2a !important;
    background: transparent !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    box-shadow: none !important;
}
div[data-testid="stTextInput"] > label,
div[data-testid="stDateInput"] > label {
    color: #caf0f8 !important;
    font-weight: 700 !important;
    font-size: 0.87rem !important;
}

/* RADIO OPTIONS */
div[data-testid="stRadio"] > label {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 0.97rem !important;
}
div[data-testid="stRadio"] > div {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
}
div[data-testid="stRadio"] label {
    background: rgba(255,255,255,0.07) !important;
    border: 1.5px solid rgba(255,255,255,0.18) !important;
    border-radius: 12px !important;
    padding: 0.65rem 1rem !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
}
div[data-testid="stRadio"] label:hover {
    border-color: #00b4d8 !important;
    background: rgba(0,180,216,0.15) !important;
    transform: translateX(4px);
}
div[data-testid="stRadio"] label p,
div[data-testid="stRadio"] label span,
div[data-testid="stRadio"] label div,
div[data-testid="stRadio"] label * {
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

/* EXPANDER */
div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1.5px solid rgba(0,180,216,0.4) !important;
    border-radius: 16px !important;
}
div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] summary *,
div[data-testid="stExpander"] summary p,
div[data-testid="stExpander"] summary span,
div[data-testid="stExpander"] summary div,
div[data-testid="stExpander"] summary svg,
div[data-testid="stExpander"] > details > summary,
div[data-testid="stExpander"] > details > summary * {
    color: #00d4ff !important;
    fill: #00d4ff !important;
    font-weight: 700 !important;
}

/* BUTTONS */
.stButton > button {
    background: linear-gradient(135deg, #00b4d8, #0077b6) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.97rem !important;
    padding: 0.7rem 1.5rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(0,119,182,0.4) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #0096c7, #005f8e) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(0,119,182,0.5) !important;
}
.stDownloadButton > button {
    background: rgba(255,255,255,0.08) !important;
    color: #90e0ef !important;
    border: 1.5px solid #00b4d8 !important;
    border-radius: 12px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    transition: all 0.2s ease !important;
}
.stDownloadButton > button:hover {
    background: rgba(0,180,216,0.18) !important;
    transform: translateY(-1px) !important;
}

/* PROGRESS BAR */
div[data-testid="stProgressBar"] > div {
    background: rgba(255,255,255,0.1) !important;
    border-radius: 99px !important;
    height: 8px !important;
}
div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #00b4d8, #90e0ef) !important;
    border-radius: 99px !important;
}

/* SCORE / RESULT */
.score-box {
    background: rgba(0,180,216,0.1);
    border: 2px solid #00b4d8;
    border-radius: 18px;
    text-align: center;
    padding: 1.8rem;
    margin: 0.8rem 0 1.2rem;
}
.result-banner {
    border-radius: 18px;
    padding: 2rem;
    text-align: center;
    margin: 0.8rem 0 1.2rem;
}

hr {
    border-color: rgba(255,255,255,0.1) !important;
    margin: 1.2rem 0 !important;
}

div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.05) !important;
    border: 2px dashed #00b4d8 !important;
    border-radius: 14px !important;
}
div[data-testid="stFileUploader"] label {
    color: #caf0f8 !important;
    font-weight: 600 !important;
}
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SURVEY DATA
# ─────────────────────────────────────────────
QUESTIONS_FILE = "questions.json"


def load_questions_from_file(filepath: str) -> list:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def get_hardcoded_questions() -> list:
    return [
        {
            "text": "How often do you voluntarily join scheduled virtual study sessions?",
            "options": [
                {"label": "Every session without fail", "score": 0},
                {"label": "Most of the time", "score": 1},
                {"label": "Occasionally", "score": 2},
                {"label": "Rarely", "score": 3},
                {"label": "Almost never", "score": 4},
            ],
        },
        {
            "text": "How well can you maintain focus during an online group study call?",
            "options": [
                {"label": "Extremely well – I stay engaged throughout", "score": 0},
                {"label": "Fairly well – minor distractions only", "score": 1},
                {"label": "Somewhat – I drift but refocus quickly", "score": 2},
                {"label": "Poorly – I get distracted frequently", "score": 3},
                {"label": "Very poorly – I can barely follow along", "score": 4},
            ],
        },
        {
            "text": "When working remotely, how easily do you stick to a study schedule?",
            "options": [
                {"label": "Very easily – I follow my schedule strictly", "score": 0},
                {"label": "Mostly – with small deviations", "score": 1},
                {"label": "Sometimes – I often revise my schedule", "score": 2},
                {"label": "Rarely – my schedule breaks down often", "score": 3},
                {"label": "Never – I have no real schedule", "score": 4},
            ],
        },
        {
            "text": "How often do environmental distractions (noise, family, phone) interrupt your remote study?",
            "options": [
                {"label": "Never – my study space is distraction-free", "score": 0},
                {"label": "Rarely – minor interruptions only", "score": 1},
                {"label": "Sometimes – a few times per session", "score": 2},
                {"label": "Often – difficult to maintain focus", "score": 3},
                {"label": "Always – my environment is very disruptive", "score": 4},
            ],
        },
        {
            "text": "How comfortable do you feel contributing verbally in virtual study groups?",
            "options": [
                {"label": "Very comfortable – I actively lead discussions", "score": 0},
                {"label": "Comfortable – I participate regularly", "score": 1},
                {"label": "Neutral – I participate when necessary", "score": 2},
                {"label": "Uncomfortable – I mostly listen", "score": 3},
                {"label": "Very uncomfortable – I avoid speaking", "score": 4},
            ],
        },
        {
            "text": "How effectively do you use digital tools (shared docs, whiteboards, chat) during virtual study?",
            "options": [
                {"label": "Very effectively – I drive tool usage", "score": 0},
                {"label": "Effectively – I use them confidently", "score": 1},
                {"label": "Somewhat – I use them when prompted", "score": 2},
                {"label": "Barely – I find them difficult", "score": 3},
                {"label": "Not at all – I struggle with digital tools", "score": 4},
            ],
        },
        {
            "text": "After a virtual study session, how productive do you feel compared to in-person study?",
            "options": [
                {"label": "Much more productive", "score": 0},
                {"label": "About the same", "score": 1},
                {"label": "Slightly less productive", "score": 2},
                {"label": "Less productive", "score": 3},
                {"label": "Far less productive", "score": 4},
            ],
        },
        {
            "text": "How often do you experience screen fatigue during or after virtual study sessions?",
            "options": [
                {"label": "Never", "score": 0},
                {"label": "Rarely – only after very long sessions", "score": 1},
                {"label": "Sometimes – in sessions over 1 hour", "score": 2},
                {"label": "Often – most sessions tire me", "score": 3},
                {"label": "Always – even short sessions exhaust me", "score": 4},
            ],
        },
        {
            "text": "How well do you retain information from virtual study sessions versus self-study?",
            "options": [
                {"label": "Much better in virtual sessions", "score": 0},
                {"label": "About the same", "score": 1},
                {"label": "Slightly worse in virtual sessions", "score": 2},
                {"label": "Noticeably worse", "score": 3},
                {"label": "Significantly worse", "score": 4},
            ],
        },
        {
            "text": "How often do you feel socially disconnected or isolated when studying remotely?",
            "options": [
                {"label": "Never – I feel connected online", "score": 0},
                {"label": "Rarely", "score": 1},
                {"label": "Sometimes", "score": 2},
                {"label": "Often", "score": 3},
                {"label": "Always – remote study feels very isolating", "score": 4},
            ],
        },
        {
            "text": "How frequently do you take planned breaks during a remote study session?",
            "options": [
                {"label": "Always – I use structured break methods (e.g., Pomodoro)", "score": 0},
                {"label": "Usually – I take breaks every 45–60 min", "score": 1},
                {"label": "Sometimes – breaks are unplanned", "score": 2},
                {"label": "Rarely – I forget to take breaks", "score": 3},
                {"label": "Never – I study until I burn out", "score": 4},
            ],
        },
        {
            "text": "How well can you manage technical issues (poor Wi-Fi, software glitches) without losing focus?",
            "options": [
                {"label": "Very well – I resolve them quickly and refocus", "score": 0},
                {"label": "Well – minor frustration but I recover", "score": 1},
                {"label": "Moderately – technical issues disrupt my flow", "score": 2},
                {"label": "Poorly – they derail my entire session", "score": 3},
                {"label": "Very poorly – I give up and stop studying", "score": 4},
            ],
        },
        {
            "text": "How motivated do you feel to study when joining a virtual session compared to studying alone?",
            "options": [
                {"label": "Much more motivated in virtual sessions", "score": 0},
                {"label": "Slightly more motivated", "score": 1},
                {"label": "No difference", "score": 2},
                {"label": "Slightly less motivated", "score": 3},
                {"label": "Far less motivated", "score": 4},
            ],
        },
        {
            "text": "How often do you find yourself multitasking (e.g., social media, gaming) during virtual study?",
            "options": [
                {"label": "Never – I stay fully on task", "score": 0},
                {"label": "Rarely – a quick glance occasionally", "score": 1},
                {"label": "Sometimes – for short periods", "score": 2},
                {"label": "Often – it's hard to resist", "score": 3},
                {"label": "Always – I'm constantly doing something else", "score": 4},
            ],
        },
        {
            "text": "Overall, how satisfied are you with your ability to learn effectively in virtual/remote settings?",
            "options": [
                {"label": "Very satisfied", "score": 0},
                {"label": "Satisfied", "score": 1},
                {"label": "Neutral", "score": 2},
                {"label": "Dissatisfied", "score": 3},
                {"label": "Very dissatisfied", "score": 4},
            ],
        },
    ]


def load_questions() -> list:
    if os.path.exists(QUESTIONS_FILE):
        try:
            return load_questions_from_file(QUESTIONS_FILE)
        except Exception:
            pass
    return get_hardcoded_questions()


# ─────────────────────────────────────────────
# SCORING
# ─────────────────────────────────────────────
PSYCHOLOGICAL_STATES = [
    (0,  14, "🌟 High Virtual Participation",
     "You are an outstanding remote learner. Your participation and focus are exceptional — keep it up!",
     "#22d3ee", "rgba(0,180,216,0.15)"),
    (15, 24, "✅ Good Remote Focus",
     "You participate well and maintain solid focus. Keep building on your good habits!",
     "#34d399", "rgba(52,211,153,0.15)"),
    (25, 34, "⚡ Moderate Ability",
     "Your remote study habits are decent but there is room for improvement. Try reducing distractions.",
     "#fbbf24", "rgba(251,191,36,0.15)"),
    (35, 44, "⚠️ Low Focus – Action Needed",
     "You struggle with focus in virtual sessions. Consider website blockers and structured breaks.",
     "#fb923c", "rgba(251,146,60,0.15)"),
    (45, 54, "🔴 Poor Remote Engagement",
     "Virtual sessions are significantly challenging. Seek peer support and speak with an academic advisor.",
     "#f87171", "rgba(248,113,113,0.15)"),
    (55, 60, "🚨 Critical Disengagement",
     "Your virtual participation is critically low. Please reach out to your academic support team.",
     "#ef4444", "rgba(239,68,68,0.15)"),
]


def get_psychological_state(score: int) -> tuple:
    for low, high, label, desc, color, bg in PSYCHOLOGICAL_STATES:
        if low <= score <= high:
            return label, desc, color, bg
    return "Unknown", "Score out of range.", "#94a3b8", "rgba(148,163,184,0.15)"


# ─────────────────────────────────────────────
# SHORT LABEL HELPER
# ─────────────────────────────────────────────
def short_label(full_label: str, score: int) -> str:
    for sep in [" – ", " - ", " — "]:
        if sep in full_label:
            return f"{full_label.split(sep)[0].strip()} ({score} pts)"
    return f"{full_label.strip()} ({score} pts)"


# ─────────────────────────────────────────────
# VALIDATION
# ─────────────────────────────────────────────
def validate_name(name: str) -> bool:
    pattern = r"^[a-zA-Z\-' ]+$"
    return bool(re.match(pattern, name.strip())) and len(name.strip()) >= 2


def validate_student_id(sid: str) -> bool:
    return sid.strip().isdigit() and len(sid.strip()) >= 4


def validate_dob(dob: date) -> bool:
    age = (date.today() - dob).days // 365
    return 10 <= age <= 100


# ─────────────────────────────────────────────
# FILE BUILDERS
# ─────────────────────────────────────────────
def build_txt(r: dict) -> str:
    lines = [
        "=" * 52,
        "  REMOTE FOCUS ABILITY SURVEY – RESULTS",
        "=" * 52,
        f"Name          : {r['name']}",
        f"Student ID    : {r['student_id']}",
        f"Date of Birth : {r['dob']}",
        f"Date Taken    : {r['date_taken']}",
        "",
        f"Total Score   : {r['score']} / {r['max_score']}",
        f"State         : {r['state']}",
        "",
        "Assessment:",
        r['description'],
        "",
        "Answer Breakdown:",
    ]
    for i, a in enumerate(r["answers"], 1):
        lines.append(f"  Q{i:02d}: {a['selected']} (+{a['score']} pts)")
    lines += ["", "=" * 52]
    return "\n".join(lines)


def build_csv(r: dict) -> str:
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["Field", "Value"])
    for key in ["name", "student_id", "dob", "date_taken", "score", "max_score", "state"]:
        w.writerow([key.replace("_", " ").title(), r[key]])
    w.writerow([])
    w.writerow(["Q#", "Answer", "Points"])
    for i, a in enumerate(r["answers"], 1):
        w.writerow([f"Q{i:02d}", a["selected"], a["score"]])
    return out.getvalue()


def build_json(r: dict) -> str:
    return json.dumps(r, indent=2, ensure_ascii=False)


# ─────────────────────────────────────────────
# FILE LOADER
# ─────────────────────────────────────────────
def parse_uploaded_result(uploaded_file) -> dict | None:
    name = uploaded_file.name
    content = uploaded_file.read()
    try:
        if name.endswith(".json"):
            return json.loads(content)
        elif name.endswith(".csv"):
            data = {}
            for row in csv.reader(io.StringIO(content.decode("utf-8"))):
                if len(row) == 2 and row[0] not in ("Field", "Q#", ""):
                    data[row[0]] = row[1]
            return data
        elif name.endswith(".txt"):
            data = {}
            for line in content.decode("utf-8").splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    data[k.strip()] = v.strip()
            return data
    except Exception:
        return None


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "home",
        "name": "",
        "student_id": "",
        "dob": None,
        "answers": [],
        "score": 0,
        "questions": load_questions(),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─────────────────────────────────────────────
# PAGE: HOME
# ─────────────────────────────────────────────
def page_home():
    st.markdown("<div class='page-title'>🧠 Remote Focus Survey</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Virtual Study · Participation · Focus Ability</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box'>
        This survey contains <strong>15 original questions</strong> evaluating your participation
        in virtual study sessions and your remote focus ability.
        Results identify your psychological readiness for online study. 📚
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝  Start New Survey", use_container_width=True):
            st.session_state.page = "details"
            st.rerun()
    with col2:
        if st.button("📂  Load Saved Results", use_container_width=True):
            st.session_state.page = "load"
            st.rerun()


# ─────────────────────────────────────────────
# PAGE: DETAILS
# ─────────────────────────────────────────────
def page_details():
    st.markdown("<div class='page-title' style='font-size:1.6rem;'>👤 Your Details</div>",
                unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Fill in your info before the survey starts</div>",
                unsafe_allow_html=True)

    name = st.text_input("Full Name", placeholder="e.g. Mary Ann Smith-Jones")
    student_id = st.text_input("Student ID (digits only)", placeholder="e.g. 002345")
    dob = st.date_input(
        "Date of Birth",
        value=date(2004, 1, 1),
        min_value=date(1924, 1, 1),
        max_value=date.today(),
    )

    errors = []

    if st.button("Continue to Survey →"):
        required_fields = [(name, "Full Name"), (student_id, "Student ID")]
        for value, field in required_fields:
            if not value or not value.strip():
                errors.append(f"'{field}' cannot be empty.")

        attempt = 0
        name_valid = False
        while attempt < 1:
            if validate_name(name):
                name_valid = True
            attempt += 1

        if not name_valid and name:
            errors.append("Name may only contain letters, hyphens, apostrophes, and spaces.")
        if student_id and not validate_student_id(student_id):
            errors.append("Student ID must contain digits only (minimum 4 digits).")
        if dob and not validate_dob(dob):
            errors.append("Date of birth is invalid. Age must be between 10 and 100.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            st.session_state.name = name.strip()
            st.session_state.student_id = student_id.strip()
            st.session_state.dob = str(dob)
            st.session_state.answers = []
            st.session_state.page = "survey"
            st.rerun()

    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()


# ─────────────────────────────────────────────
# PAGE: SURVEY
# ─────────────────────────────────────────────
def page_survey():
    questions: list = st.session_state.questions

    st.markdown("<div class='page-title' style='font-size:1.6rem;'>📋 Survey Questions</div>",
                unsafe_allow_html=True)

    answered_count = sum(
        1 for i in range(len(questions))
        if st.session_state.get(f"q_{i}") is not None
    )
    st.markdown(
        f"<p style='color:#90e0ef;font-size:0.88rem;font-weight:600;text-align:center;margin-bottom:0.6rem;'>"
        f"{answered_count} of {len(questions)} answered</p>",
        unsafe_allow_html=True,
    )
    st.progress(answered_count / len(questions))
    st.markdown("<div style='margin-bottom:1.4rem;'></div>", unsafe_allow_html=True)

    selected_answers = []
    all_answered = True

    for i, q in enumerate(questions):
        option_labels = [opt["label"] for opt in q["options"]]
        st.markdown(f"<div class='q-chip'>Question {i + 1} of {len(questions)}</div>",
                    unsafe_allow_html=True)

        choice = st.radio(q["text"], options=option_labels, key=f"q_{i}", index=None)

        if choice is None:
            all_answered = False
            selected_answers.append(None)
        else:
            score_val = next(
                (opt["score"] for opt in q["options"] if opt["label"] == choice), 0
            )
            selected_answers.append({"selected": choice, "score": score_val})

        st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("← Back"):
            st.session_state.page = "details"
            st.rerun()
    with col2:
        if st.button("✅  Submit Survey"):
            if not all_answered:
                st.warning("⚠️ Please answer all questions before submitting.")
            else:
                st.session_state.answers = selected_answers
                st.session_state.score = sum(a["score"] for a in selected_answers)
                st.session_state.page = "result"
                st.rerun()


# ─────────────────────────────────────────────
# PAGE: RESULT
# ─────────────────────────────────────────────
def page_result():
    score: int = st.session_state.score
    name: str = st.session_state.name
    answers: list = st.session_state.answers
    questions: list = st.session_state.questions
    max_score = len(questions) * 4

    label, description, color, bg = get_psychological_state(score)

    st.markdown("<div class='page-title' style='font-size:1.6rem;'>🎯 Your Results</div>",
                unsafe_allow_html=True)
    st.markdown(
        f"<p style='color:#90e0ef;font-size:0.88rem;font-weight:600;text-align:center;"
        f"margin-bottom:1rem;'>Hi {name}! Here's how you did.</p>",
        unsafe_allow_html=True,
    )

    st.markdown(f"""
    <div class='score-box'>
        <p style='color:#90e0ef;font-size:0.75rem;font-weight:800;letter-spacing:0.14em;
                  text-transform:uppercase;margin:0 0 0.4rem;'>Total Score</p>
        <p style='color:#ffffff;font-size:3.2rem;font-weight:800;margin:0;line-height:1;'>
            {score}
            <span style='font-size:1.3rem;color:#90e0ef;font-weight:600;'>&nbsp;/ {max_score}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='result-banner' style='background:{bg};border:2px solid {color};'>
        <p style='color:{color};font-size:1.4rem;font-weight:800;margin:0 0 0.5rem;'>{label}</p>
        <p style='color:#ffffff;font-size:0.93rem;font-weight:600;margin:0;'>{description}</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📊 View all score bands"):
        for low, high, lbl, _, clr, _ in PSYCHOLOGICAL_STATES:
            st.markdown(
                f"<div style='display:flex;align-items:center;gap:0.8rem;margin-bottom:0.6rem;'>"
                f"<span style='background:{clr};color:#ffffff;border-radius:99px;"
                f"padding:0.2rem 0.85rem;font-size:0.75rem;font-weight:800;"
                f"white-space:nowrap;min-width:58px;text-align:center;display:inline-block;'>"
                f"{low}–{high}</span>"
                f"<span style='color:#ffffff;font-size:0.93rem;font-weight:700;'>{lbl}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<p style='color:#caf0f8;font-weight:700;font-size:1rem;margin-bottom:0.6rem;'>"
                "💾 Save Your Results</p>", unsafe_allow_html=True)

    result_data = {
        "name": name,
        "student_id": st.session_state.student_id,
        "dob": st.session_state.dob,
        "date_taken": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "score": score,
        "max_score": max_score,
        "state": label,
        "description": description,
        "answers": answers,
    }

    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button("⬇ TXT", data=build_txt(result_data),
                           file_name=f"{st.session_state.student_id}_result.txt",
                           mime="text/plain", use_container_width=True)
    with c2:
        st.download_button("⬇ CSV", data=build_csv(result_data),
                           file_name=f"{st.session_state.student_id}_result.csv",
                           mime="text/csv", use_container_width=True)
    with c3:
        st.download_button("⬇ JSON", data=build_json(result_data),
                           file_name=f"{st.session_state.student_id}_result.json",
                           mime="application/json", use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    with st.expander("📋 View your answer breakdown"):
        for i, (q, a) in enumerate(zip(questions, answers), 1):
            display = short_label(a["selected"], a["score"])
            if a["score"] == 0:
                pts_color = "#34d399"
            elif a["score"] <= 2:
                pts_color = "#fbbf24"
            else:
                pts_color = "#f87171"
            st.markdown(
                f"<div style='margin-bottom:1rem;padding-bottom:1rem;"
                f"border-bottom:1px solid rgba(255,255,255,0.1);'>"
                f"<span style='background:#00b4d8;color:#fff;border-radius:99px;"
                f"padding:0.15rem 0.7rem;font-size:0.72rem;font-weight:800;"
                f"letter-spacing:0.1em;'>Q{i:02d}</span><br>"
                f"<span style='color:#ffffff;font-size:0.9rem;font-weight:600;"
                f"line-height:1.6;display:block;margin:0.35rem 0 0.25rem;'>{q['text']}</span>"
                f"<span style='color:{pts_color};font-size:0.9rem;font-weight:700;'>"
                f"→ {display}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

    if st.button("🔄 Take Survey Again"):
        for key in ["page", "name", "student_id", "dob", "answers", "score"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()


# ─────────────────────────────────────────────
# PAGE: LOAD
# ─────────────────────────────────────────────
def page_load():
    st.markdown("<div class='page-title' style='font-size:1.6rem;'>📂 Load Saved Results</div>",
                unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Upload a .json, .csv, or .txt result file</div>",
                unsafe_allow_html=True)

    uploaded = st.file_uploader("Choose your saved result file", type=["json", "csv", "txt"])

    if uploaded:
        result = parse_uploaded_result(uploaded)
        if result:
            st.success("✅ File loaded successfully!")
            display_fields = [
                ("Name", result.get("name", "—")),
                ("Student ID", result.get("student_id", result.get("Student Id", "—"))),
                ("Date of Birth", result.get("dob", result.get("Dob", "—"))),
                ("Date Taken", result.get("date_taken", result.get("Date Taken", "—"))),
                ("Total Score", result.get("score", result.get("Score", "—"))),
                ("Psychological State", result.get("state", result.get("State", "—"))),
            ]
            for field, val in display_fields:
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;align-items:center;"
                    f"padding:0.6rem 0;border-bottom:1px solid rgba(255,255,255,0.08);'>"
                    f"<span style='color:#90e0ef;font-size:0.85rem;font-weight:600;'>{field}</span>"
                    f"<span style='color:#ffffff;font-size:0.88rem;font-weight:800;'>{val}</span></div>",
                    unsafe_allow_html=True,
                )
        else:
            st.error("❌ Could not read the file. Please upload a valid survey result file.")

    st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()


# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
page = st.session_state.get("page", "home")

if page == "home":
    page_home()
elif page == "details":
    page_details()
elif page == "survey":
    page_survey()
elif page == "result":
    page_result()
elif page == "load":
    page_load()
