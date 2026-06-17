import streamlit as st
import time
from dotenv import load_dotenv

load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MeetMind · AI Meeting Assistant",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Fonts ---- */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ---- Token system ---- */
:root {
    --bg:        #0A0D14;
    --surface:   #111520;
    --border:    #1E2535;
    --accent:    #4F8EF7;
    --accent2:   #7C5EF5;
    --text:      #E8ECF5;
    --muted:     #6B7A99;
    --success:   #3DD68C;
    --warn:      #F5A623;
    --card-bg:   #141927;
}

/* ---- Base ---- */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

.stApp { background: var(--bg); }

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ---- Header bar ---- */
.meetmind-header {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 28px 0 20px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 32px;
}
.meetmind-header .logo-ring {
    width: 48px; height: 48px;
    border-radius: 14px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    box-shadow: 0 0 24px rgba(79,142,247,0.35);
}
.meetmind-header h1 {
    font-size: 1.6rem; font-weight: 700; margin: 0; letter-spacing: -0.5px;
}
.meetmind-header span { color: var(--muted); font-size: 0.85rem; margin-top: 2px; display: block; }

/* ---- Step pills ---- */
.step-row { display: flex; gap: 8px; margin-bottom: 24px; flex-wrap: wrap; }
.step-pill {
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 4px 12px; border-radius: 100px;
    border: 1px solid var(--border);
    color: var(--muted);
    background: var(--surface);
}
.step-pill.active {
    border-color: var(--accent);
    color: var(--accent);
    background: rgba(79,142,247,0.1);
}
.step-pill.done {
    border-color: var(--success);
    color: var(--success);
    background: rgba(61,214,140,0.08);
}

/* ---- Cards ---- */
.insight-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 16px;
    transition: border-color 0.2s;
}
.insight-card:hover { border-color: #2A3652; }
.insight-card .card-label {
    font-size: 0.7rem; font-weight: 600; letter-spacing: 0.12em;
    text-transform: uppercase; color: var(--muted); margin-bottom: 10px;
}
.insight-card .card-title {
    font-size: 1.15rem; font-weight: 700; color: var(--text);
    line-height: 1.4;
}
.insight-card p { color: #A8B4CC; font-size: 0.9rem; line-height: 1.7; margin: 0; }

/* ---- Bullet list items ---- */
.item-row {
    display: flex; gap: 10px; align-items: flex-start;
    padding: 10px 0; border-bottom: 1px solid var(--border);
}
.item-row:last-child { border-bottom: none; }
.item-dot {
    width: 7px; height: 7px; border-radius: 50%;
    margin-top: 7px; flex-shrink: 0;
}
.item-dot.blue  { background: var(--accent); }
.item-dot.purple{ background: var(--accent2); }
.item-dot.green { background: var(--success); }
.item-dot.orange{ background: var(--warn); }
.item-text { font-size: 0.88rem; color: #B8C3D9; line-height: 1.6; }

/* ---- Transcript box ---- */
.transcript-box {
    background: #0D1017;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #7A8FA8;
    line-height: 1.8;
    max-height: 320px;
    overflow-y: auto;
}

/* ---- Chat ---- */
.chat-bubble-user {
    background: rgba(79,142,247,0.12);
    border: 1px solid rgba(79,142,247,0.25);
    border-radius: 12px 12px 4px 12px;
    padding: 12px 16px;
    margin: 8px 0 8px 60px;
    font-size: 0.88rem;
    color: var(--text);
}
.chat-bubble-ai {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px 12px 12px 4px;
    padding: 12px 16px;
    margin: 8px 60px 8px 0;
    font-size: 0.88rem;
    color: #A8B4CC;
    line-height: 1.7;
}
.chat-label { font-size: 0.68rem; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--muted); margin-bottom: 4px; }

/* ---- Buttons ---- */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 1.6rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* ---- Inputs ---- */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(79,142,247,0.15) !important;
}

/* ---- Progress bar ---- */
.stProgress > div > div > div { background: linear-gradient(90deg, var(--accent), var(--accent2)) !important; }

/* ---- Divider ---- */
hr { border-color: var(--border) !important; margin: 28px 0 !important; }

/* ---- Metric cards ---- */
.stat-row { display: flex; gap: 14px; margin-bottom: 24px; flex-wrap: wrap; }
.stat-card {
    flex: 1; min-width: 120px;
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 18px;
    text-align: center;
}
.stat-card .stat-num { font-size: 1.6rem; font-weight: 700; color: var(--accent); }
.stat-card .stat-lbl { font-size: 0.72rem; color: var(--muted); margin-top: 2px;
    text-transform: uppercase; letter-spacing: 0.08em; }

/* ---- Tab styling ---- */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px !important;
    background: var(--surface) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    color: var(--muted) !important;
}
.stTabs [aria-selected="true"] {
    background: var(--accent) !important;
    color: #fff !important;
}

/* ---- Hide Streamlit chrome ---- */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────────────────────────
for key in ["pipeline_result", "chat_history", "processing", "step"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "chat_history" else []
if "step" not in st.session_state or st.session_state.step is None:
    st.session_state.step = 0


# ── Helpers ────────────────────────────────────────────────────────────────────
def render_header():
    st.markdown("""
    <div class="meetmind-header">
        <div class="logo-ring">🎙️</div>
        <div>
            <h1>MeetMind</h1>
            <span>AI-powered meeting intelligence · transcribe · analyse · chat</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_steps(current: int):
    steps = ["Input", "Transcribe", "Analyse", "Results"]
    pills = ""
    for i, s in enumerate(steps):
        cls = "done" if i < current else ("active" if i == current else "")
        icon = "✓ " if i < current else ""
        pills += f'<div class="step-pill {cls}">{icon}{s}</div>'
    st.markdown(f'<div class="step-row">{pills}</div>', unsafe_allow_html=True)


def render_items(items_text: str, dot_class: str):
    """Parse newline-separated items and render as styled rows."""
    lines = [l.strip().lstrip("-•·*123456789.)").strip()
             for l in items_text.splitlines() if l.strip()]
    html = ""
    for line in lines:
        if line:
            html += f"""
            <div class="item-row">
                <div class="item-dot {dot_class}"></div>
                <div class="item-text">{line}</div>
            </div>"""
    st.markdown(html, unsafe_allow_html=True)


def run_pipeline_ui(source: str, language: str):
    """Run the pipeline with live progress feedback."""
    from utils.audio_processor import process_input
    from core.transcriber import transcribe_all
    from core.summarizer import summarize, generate_title
    from core.extractor import extract_action_items, extract_key_decisions, extract_questions
    from core.rag_engine import build_rag_chain

    progress = st.progress(0)
    status   = st.empty()

    steps_ui = [
        (10, "⬇️  Fetching & chunking audio…"),
        (30, "🎙️  Transcribing audio…"),
        (50, "📝  Generating title & summary…"),
        (70, "🔍  Extracting insights…"),
        (90, "🧠  Building RAG index…"),
        (100, "✅  Done!"),
    ]

    def tick(idx):
        pct, msg = steps_ui[idx]
        progress.progress(pct)
        status.markdown(f"<p style='color:#6B7A99;font-size:0.85rem'>{msg}</p>",
                        unsafe_allow_html=True)

    tick(0); chunks = process_input(source)
    tick(1); transcript = transcribe_all(chunks, language=language)
    tick(2)
    title   = generate_title(transcript)
    summary = summarize(transcript)
    tick(3)
    action_items = extract_action_items(transcript)
    decisions    = extract_key_decisions(transcript)
    questions    = extract_questions(transcript)
    tick(4); rag_chain = build_rag_chain(transcript)
    tick(5); time.sleep(0.4)

    progress.empty(); status.empty()

    return {
        "title":         title,
        "transcript":    transcript,
        "summary":       summary,
        "action_items":  action_items,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain":     rag_chain,
    }


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️  Settings")
    st.markdown("---")

    source = st.text_input(
        "YouTube URL or file path",
        placeholder="https://youtube.com/watch?v=... or /path/to/audio.mp3",
    )

    language = st.selectbox(
        "Transcription language",
        ["english", "hinglish"],
        index=0,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("▶  Run Pipeline", use_container_width=True)

    st.markdown("---")
    if st.session_state.pipeline_result:
        st.markdown("### 📊 Stats")
        r = st.session_state.pipeline_result
        words = len(r["transcript"].split())
        st.markdown(f"""
        <div class="stat-card" style="margin-bottom:10px">
            <div class="stat-num">{words:,}</div>
            <div class="stat-lbl">Words transcribed</div>
        </div>""", unsafe_allow_html=True)
        chats = len(st.session_state.chat_history) // 2
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-num">{chats}</div>
            <div class="stat-lbl">Chat exchanges</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<span style='color:#3B4562;font-size:0.72rem'>MeetMind · powered by Mohet Kumar Sahu</span>",
                unsafe_allow_html=True)


# ── Main area ──────────────────────────────────────────────────────────────────
render_header()

# ── Pipeline trigger ────────────────────────────────────────────────────────────
if run_btn:
    if not source.strip():
        st.warning("Please enter a YouTube URL or file path in the sidebar.")
    else:
        st.session_state.step = 1
        render_steps(1)
        with st.spinner(""):
            try:
                result = run_pipeline_ui(source.strip(), language)
                st.session_state.pipeline_result = result
                st.session_state.chat_history = []
                st.session_state.step = 3
                st.rerun()
            except Exception as e:
                st.error(f"Pipeline failed: {e}")
                st.session_state.step = 0

# ── Idle / empty state ──────────────────────────────────────────────────────────
if not st.session_state.pipeline_result:
    render_steps(0)
    st.markdown("""
    <div class="insight-card" style="border-style:dashed; text-align:center; padding:48px 24px;">
        <div style="font-size:2.4rem; margin-bottom:16px">🎙️</div>
        <div class="card-title" style="margin-bottom:10px">Ready to analyse your meeting</div>
        <p>Paste a YouTube link or local audio/video path in the sidebar,<br>choose a language, and hit <strong style="color:#4F8EF7">Run Pipeline</strong>.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Results ─────────────────────────────────────────────────────────────────────
render_steps(3)
result = st.session_state.pipeline_result

# Title card
st.markdown(f"""
<div class="insight-card">
    <div class="card-label">Meeting title</div>
    <div class="card-title">{result['title']}</div>
</div>
""", unsafe_allow_html=True)

# Tabs
tab_summary, tab_actions, tab_decisions, tab_questions, tab_transcript, tab_chat = st.tabs(
    ["📋 Summary", "✅ Actions", "🔑 Decisions", "❓ Questions", "📜 Transcript", "💬 Chat"]
)

# ---- Summary ----
with tab_summary:
    st.markdown(f"""
    <div class="insight-card">
        <div class="card-label">TL;DR</div>
        <p>{result['summary']}</p>
    </div>
    """, unsafe_allow_html=True)

# ---- Action Items ----
with tab_actions:
    st.markdown('<div class="insight-card"><div class="card-label">Action Items</div>', unsafe_allow_html=True)
    render_items(result["action_items"], "blue")
    st.markdown("</div>", unsafe_allow_html=True)

# ---- Key Decisions ----
with tab_decisions:
    st.markdown('<div class="insight-card"><div class="card-label">Key Decisions</div>', unsafe_allow_html=True)
    render_items(result["key_decisions"], "purple")
    st.markdown("</div>", unsafe_allow_html=True)

# ---- Open Questions ----
with tab_questions:
    st.markdown('<div class="insight-card"><div class="card-label">Open Questions</div>', unsafe_allow_html=True)
    render_items(result["open_questions"], "orange")
    st.markdown("</div>", unsafe_allow_html=True)

# ---- Transcript ----
with tab_transcript:
    st.markdown('<div class="card-label" style="font-size:0.7rem;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:#6B7A99;margin-bottom:10px">Raw Transcript</div>',
                unsafe_allow_html=True)
    st.markdown(f'<div class="transcript-box">{result["transcript"]}</div>',
                unsafe_allow_html=True)
    st.download_button(
        "⬇  Download transcript",
        data=result["transcript"],
        file_name="transcript.txt",
        mime="text/plain",
    )

# ---- Chat ----
with tab_chat:
    from core.rag_engine import ask_question

    st.markdown('<div class="card-label" style="font-size:0.7rem;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:#6B7A99;margin-bottom:16px">Chat with your meeting</div>',
                unsafe_allow_html=True)

    # Render history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-label" style="text-align:right">You</div>
            <div class="chat-bubble-user">{msg['content']}</div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-label">MeetMind</div>
            <div class="chat-bubble-ai">{msg['content']}</div>
            """, unsafe_allow_html=True)

    # Input row
    col_q, col_btn = st.columns([5, 1])
    with col_q:
        question = st.text_input(
            "question",
            placeholder="Ask anything about the meeting…",
            label_visibility="collapsed",
            key="chat_input",
        )
    with col_btn:
        ask_btn = st.button("Ask →", use_container_width=True)

    if ask_btn and question.strip():
        with st.spinner("Thinking…"):
            answer = ask_question(result["rag_chain"], question.strip())
        st.session_state.chat_history.append({"role": "user",    "content": question.strip()})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    if not st.session_state.chat_history:
        st.markdown("""
        <p style="color:#3B4562; font-size:0.82rem; margin-top:12px">
        💡 Try: "What were the main decisions?" · "Who owns the next steps?" · "Summarise in 3 bullets."
        </p>""", unsafe_allow_html=True)