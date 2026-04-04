"""
Virtual Study Session Participation and Remote Focus Ability Survey
Fundamentals of Programming - 4BUIS008C
Psychological State Survey Application (Streamlit Web Version)
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
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'DM Serif Display', serif !important;
}

.main {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 760px;
}

.survey-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(12px);
}

.question-number {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    color: #a78bfa;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

.result-banner {
    text-align: center;
    padding: 2.5rem;
    border-radius: 20px;
    margin: 1.5rem 0;
}

.stRadio > div {
    gap: 0.4rem;
}

div[data-testid="stRadio"] label {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    width: 100%;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-bottom: 0.3rem;
}

div[data-testid="stRadio"] label:hover {
    background: rgba(167, 139, 250, 0.15);
    border-color: #a78bfa;
}

.stButton button {
    background: linear-gradient(135deg, #7c3aed, #a78bfa);
    color: white;
    border: none;
    border-radius: 12px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    padding: 0.7rem 2.2rem;
    cursor: pointer;
    transition: all 0.2s ease;
    width: 100%;
}

.stButton button:hover {
    background: linear-gradient(135deg, #6d28d9, #8b5cf6);
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(124,58,237,0.4);
}

.stTextInput input, .stSelectbox select, .stDateInput input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: white !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stDownloadButton button {
    background: rgba(167,139,250,0.15) !important;
    border: 1px solid #a78bfa !important;
    color: #a78bfa !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}

.pill {
    display: inline-block;
    background: rgba(167,139,250,0.2);
    border: 1px solid #a78bfa;
    border-radius: 99px;
    padding: 0.2rem 0.9rem;
    font-size: 0.78rem;
    font-weight: 600;
    color: #c4b5fd;
    margin-right: 0.4rem;
    margin-bottom: 0.4rem;
}

.score-box {
    background: linear-gradient(135deg, rgba(124,58,237,0.3), rgba(167,139,250,0.15));
    border: 1px solid #7c3aed;
    border-radius: 16px;
    text-align: center;
    padding: 1.5rem;
    margin: 1rem 0;
}

.info-box {
    background: rgba(167,139,250,0.08);
    border-left: 3px solid #a78bfa;
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    font-size: 0.9rem;
    color: #c4b5fd;
}

div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.04);
    border: 1px dashed rgba(167,139,250,0.4);
    border-radius: 12px;
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SURVEY DATA  (loaded from external file OR hardcoded)
# ─────────────────────────────────────────────
QUESTIONS_FILE = "questions.json"


def load_questions_from_file(filepath: str) -> list:
    """Load survey questions from an external JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def get_hardcoded_questions() -> list:
    """Return the hardcoded list of survey questions as a fallback."""
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
            "text": "How often do you find yourself multitasking (e.g., social media, gaming) during virtual study sessions?",
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
    """Load questions: prefer external file, fall back to hardcoded."""
    if os.path.exists(QUESTIONS_FILE):
        try:
            return load_questions_from_file(QUESTIONS_FILE)
        except Exception:
            pass
    return get_hardcoded_questions()


# ─────────────────────────────────────────────
# SCORING LOGIC
# ─────────────────────────────────────────────
PSYCHOLOGICAL_STATES = [
    (0, 14,  "🌟 High Virtual Participation",
     "You are an outstanding remote learner. Your virtual participation is excellent and your focus ability is exceptional. Keep it up!",
     "#10b981"),
    (15, 24, "✅ Good Remote Focus",
     "You participate well and maintain solid focus in virtual settings. Continue your good habits and explore ways to make sessions even more effective.",
     "#3b82f6"),
    (25, 34, "⚡ Moderate Ability – Minor Adjustments Needed",
     "Your remote study habits are decent but there is noticeable room for improvement. Try reducing distractions and setting clearer session goals.",
     "#f59e0b"),
    (35, 44, "⚠️ Low Focus – Distraction Management Needed",
     "You struggle with focus and participation in virtual sessions. Consider setting camera-on rules, using website blockers, and scheduling structured breaks.",
     "#f97316"),
    (45, 54, "🔴 Poor Remote Engagement",
     "Virtual study sessions are significantly challenging for you. Seek peer support, improve your study environment, and consider speaking with an academic advisor.",
     "#ef4444"),
    (55, 60, "🚨 Critical Disengagement – Support Recommended",
     "Your virtual participation and remote focus are critically low. Please reach out to your academic support team. Immediate changes to your study routine are essential.",
     "#dc2626"),
]


def get_psychological_state(score: int) -> tuple:
    """Return the (label, description, color) for a given score."""
    for low, high, label, desc, color in PSYCHOLOGICAL_STATES:
        if low <= score <= high:
            return label, desc, color
    return "Unknown", "Score out of expected range.", "#6b7280"


# ─────────────────────────────────────────────
# VALIDATION FUNCTIONS
# ─────────────────────────────────────────────
def validate_name(name: str) -> bool:
    """Allow letters, hyphens, apostrophes, and spaces only."""
    pattern = r"^[a-zA-Z\-' ]+$"
    return bool(re.match(pattern, name.strip())) and len(name.strip()) >= 2


def validate_student_id(sid: str) -> bool:
    """Student ID must contain digits only."""
    return sid.strip().isdigit() and len(sid.strip()) >= 4


def validate_dob(dob: date) -> bool:
    """Date of birth must be in the past and plausible (age 10–100)."""
    today = date.today()
    age = (today - dob).days // 365
    return 10 <= age <= 100


# ─────────────────────────────────────────────
# FILE GENERATION FUNCTIONS
# ─────────────────────────────────────────────
def build_txt(result: dict) -> str:
    lines = [
        "=" * 50,
        "REMOTE FOCUS ABILITY SURVEY – RESULTS",
        "=" * 50,
        f"Name       : {result['name']}",
        f"Student ID : {result['student_id']}",
        f"Date of Birth : {result['dob']}",
        f"Date Taken : {result['date_taken']}",
        "",
        f"Total Score: {result['score']} / 60",
        f"State      : {result['state']}",
        "",
        "Assessment:",
        result['description'],
        "",
        "Answer breakdown:",
    ]
    for i, ans in enumerate(result["answers"], 1):
        lines.append(f"  Q{i:02d}: {ans['selected']} (score: {ans['score']})")
    lines += ["", "=" * 50]
    return "\n".join(lines)


def build_csv(result: dict) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Field", "Value"])
    writer.writerow(["Name", result["name"]])
    writer.writerow(["Student ID", result["student_id"]])
    writer.writerow(["Date of Birth", result["dob"]])
    writer.writerow(["Date Taken", result["date_taken"]])
    writer.writerow(["Total Score", result["score"]])
    writer.writerow(["Psychological State", result["state"]])
    writer.writerow([])
    writer.writerow(["Question No", "Selected Answer", "Points"])
    for i, ans in enumerate(result["answers"], 1):
        writer.writerow([f"Q{i:02d}", ans["selected"], ans["score"]])
    return output.getvalue()


def build_json(result: dict) -> str:
    return json.dumps(result, indent=2, ensure_ascii=False)


# ─────────────────────────────────────────────
# LOAD SAVED RESULT FROM UPLOADED FILE
# ─────────────────────────────────────────────
def parse_uploaded_result(uploaded_file) -> dict | None:
    name = uploaded_file.name
    content = uploaded_file.read()
    try:
        if name.endswith(".json"):
            return json.loads(content)
        elif name.endswith(".csv"):
            reader = csv.reader(io.StringIO(content.decode("utf-8")))
            rows = list(reader)
            data = {}
            for row in rows:
                if len(row) == 2 and row[0] not in ("Field", "Question No", ""):
                    data[row[0]] = row[1]
            return data
        elif name.endswith(".txt"):
            text = content.decode("utf-8")
            data = {}
            for line in text.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    data[k.strip()] = v.strip()
            return data
    except Exception:
        return None
    return None


# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "home",          # home | details | survey | result | load
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
# ── PAGE: HOME ──
# ─────────────────────────────────────────────
def page_home():
    st.markdown("""
    <div style='text-align:center; padding: 1.5rem 0 0.5rem;'>
        <div style='font-size:3.5rem;'>🧠</div>
        <h1 style='color:white; font-size:2.2rem; margin:0.3rem 0 0.1rem;'>Remote Focus Survey</h1>
        <p style='color:#a78bfa; font-size:1rem; letter-spacing:0.06em; text-transform:uppercase; font-weight:500;'>
            Virtual Study Session Participation & Remote Focus Ability
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box'>
        This survey contains <strong>15 questions</strong> and evaluates your participation in virtual 
        study sessions and your ability to maintain focus in remote learning environments.
        The results will help identify your psychological readiness for remote study.
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

    st.markdown("---")
    st.markdown("<p style='color:#6b7280; font-size:0.78rem; text-align:center;'>Fundamentals of Programming · 4BUIS008C · WIUT</p>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ── PAGE: DETAILS ──
# ─────────────────────────────────────────────
def page_details():
    st.markdown("<h2 style='color:white;'>Your Details</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9ca3af;'>Please fill in your information before starting the survey.</p>", unsafe_allow_html=True)

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
        # Validation using for loop (LO requirement)
        required_fields = [
            (name, "name"),
            (student_id, "student_id"),
            (str(dob), "dob"),
        ]
        for value, field in required_fields:
            if not value or not value.strip():
                errors.append(f"Field '{field}' cannot be empty.")

        # While-loop style validation for name
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
            errors.append("Date of birth is invalid. Age must be between 10 and 100 years.")

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

    if st.button("← Back"):
        st.session_state.page = "home"
        st.rerun()


# ─────────────────────────────────────────────
# ── PAGE: SURVEY ──
# ─────────────────────────────────────────────
def page_survey():
    questions: list = st.session_state.questions

    st.markdown(f"<h2 style='color:white;'>Survey</h2>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='color:#9ca3af;'>Answer all <strong>{len(questions)}</strong> questions below.</p>",
        unsafe_allow_html=True,
    )

    # Progress bar
    answered = len(st.session_state.answers)
    st.progress(min(answered / len(questions), 1.0))

    selected_answers = []
    all_answered = True

    for i, q in enumerate(questions):
        option_labels = [opt["label"] for opt in q["options"]]
        st.markdown(f"""
        <div class='question-number'>Question {i + 1} of {len(questions)}</div>
        """, unsafe_allow_html=True)

        choice = st.radio(
            q["text"],
            options=option_labels,
            key=f"q_{i}",
            index=None,
        )

        if choice is None:
            all_answered = False
            selected_answers.append(None)
        else:
            # Find score for chosen label
            score_val = next(
                (opt["score"] for opt in q["options"] if opt["label"] == choice), 0
            )
            selected_answers.append({"selected": choice, "score": score_val})

        st.markdown("<div style='margin-bottom:1.2rem;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("← Back"):
            st.session_state.page = "details"
            st.rerun()
    with col2:
        if st.button("Submit Survey →"):
            if not all_answered:
                st.warning("⚠️ Please answer all questions before submitting.")
            else:
                total = sum(a["score"] for a in selected_answers)
                st.session_state.answers = selected_answers
                st.session_state.score = total
                st.session_state.page = "result"
                st.rerun()


# ─────────────────────────────────────────────
# ── PAGE: RESULT ──
# ─────────────────────────────────────────────
def page_result():
    score: int = st.session_state.score
    name: str = st.session_state.name
    answers: list = st.session_state.answers
    questions: list = st.session_state.questions

    label, description, color = get_psychological_state(score)
    max_score = len(questions) * 4

    st.markdown(f"<h2 style='color:white;'>Your Results</h2>", unsafe_allow_html=True)

    # Score box
    st.markdown(f"""
    <div class='score-box'>
        <p style='color:#c4b5fd; font-size:0.85rem; margin:0 0 0.3rem; letter-spacing:0.1em; text-transform:uppercase;'>Total Score</p>
        <p style='color:white; font-size:3rem; font-weight:700; margin:0; font-family:DM Serif Display, serif;'>{score} <span style='font-size:1.4rem; color:#9ca3af;'>/ {max_score}</span></p>
    </div>
    """, unsafe_allow_html=True)

    # State banner
    st.markdown(f"""
    <div class='result-banner' style='background: {color}22; border: 2px solid {color};'>
        <p style='color:{color}; font-size:1.5rem; font-weight:700; margin:0 0 0.5rem; font-family:DM Serif Display, serif;'>{label}</p>
        <p style='color:#d1d5db; font-size:0.95rem; margin:0;'>{description}</p>
    </div>
    """, unsafe_allow_html=True)

    # Score ranges reference
    with st.expander("📊 View all scoring bands"):
        for low, high, lbl, _, clr in PSYCHOLOGICAL_STATES:
            st.markdown(f"""
            <span class='pill' style='background:{clr}22; border-color:{clr}; color:{clr};'>{low}–{high}</span> {lbl}<br>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Save options
    st.markdown("<h3 style='color:white;'>💾 Save Your Results</h3>", unsafe_allow_html=True)

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

    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            "⬇ Download TXT",
            data=build_txt(result_data),
            file_name=f"{st.session_state.student_id}_result.txt",
            mime="text/plain",
        )
    with col2:
        st.download_button(
            "⬇ Download CSV",
            data=build_csv(result_data),
            file_name=f"{st.session_state.student_id}_result.csv",
            mime="text/csv",
        )
    with col3:
        st.download_button(
            "⬇ Download JSON",
            data=build_json(result_data),
            file_name=f"{st.session_state.student_id}_result.json",
            mime="application/json",
        )

    st.markdown("---")

    # Answer breakdown
    with st.expander("📋 View answer breakdown"):
        for i, (q, a) in enumerate(zip(questions, answers), 1):
            st.markdown(f"""
            <div style='margin-bottom:0.8rem;'>
                <span style='color:#9ca3af; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.1em;'>Q{i:02d}</span><br>
                <span style='color:#e5e7eb; font-size:0.88rem;'>{q['text']}</span><br>
                <span style='color:#a78bfa; font-size:0.85rem;'>→ {a['selected']} <span style='color:#6b7280;'>(+{a['score']} pts)</span></span>
            </div>
            """, unsafe_allow_html=True)

    if st.button("🔄 Take Survey Again"):
        for key in ["page", "name", "student_id", "dob", "answers", "score"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()


# ─────────────────────────────────────────────
# ── PAGE: LOAD ──
# ─────────────────────────────────────────────
def page_load():
    st.markdown("<h2 style='color:white;'>Load Saved Results</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9ca3af;'>Upload a previously saved survey file (.json, .csv, or .txt).</p>", unsafe_allow_html=True)

    uploaded = st.file_uploader("Choose a result file", type=["json", "csv", "txt"])

    if uploaded:
        result = parse_uploaded_result(uploaded)
        if result:
            st.success("✅ File loaded successfully!")
            fields = [
                ("Name", result.get("name", "—")),
                ("Student ID", result.get("student_id", result.get("Student ID", "—"))),
                ("Date of Birth", result.get("dob", result.get("Date of Birth", "—"))),
                ("Date Taken", result.get("date_taken", result.get("Date Taken", "—"))),
                ("Total Score", result.get("score", result.get("Total Score", "—"))),
                ("Psychological State", result.get("state", result.get("Psychological State", "—"))),
            ]
            for field, val in fields:
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; padding:0.5rem 0; border-bottom:1px solid rgba(255,255,255,0.07);'>
                    <span style='color:#9ca3af; font-size:0.88rem;'>{field}</span>
                    <span style='color:white; font-size:0.88rem; font-weight:500;'>{val}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("❌ Could not parse the file. Please upload a valid survey result file.")

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
