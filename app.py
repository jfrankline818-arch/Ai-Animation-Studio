
import streamlit as st
import json
import uuid
from datetime import datetime, timezone

# ==========================================================
# AI ANIMATION STUDIO
# Version 1.0 - Deployable Streamlit application
# AI rendering backend will be connected separately.
# ==========================================================

st.set_page_config(
    page_title="AI Animation Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------- DESIGN --------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: Inter, sans-serif;
}

.stApp {
    background:
      radial-gradient(circle at 10% 5%, rgba(112,80,255,.17), transparent 28%),
      radial-gradient(circle at 90% 15%, rgba(0,210,190,.10), transparent 25%),
      #090d19;
    color: #f5f7ff;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #101729;
    border-right: 1px solid #293754;
}

.hero {
    padding: 38px;
    border-radius: 24px;
    background: linear-gradient(120deg, #392c91, #1a577c, #123b54);
    border: 1px solid rgba(255,255,255,.13);
    margin-bottom: 25px;
}

.hero h1 {
    font-size: clamp(30px, 5vw, 46px);
    font-weight: 800;
    color: white;
    margin-bottom: 8px;
}

.hero p {
    color: #e1e9ff;
    font-size: 16px;
}

.feature-card {
    background: rgba(22,31,52,.9);
    border: 1px solid #293754;
    border-radius: 18px;
    padding: 22px;
    min-height: 130px;
}

.feature-card h3 {
    color: white;
    margin-top: 0;
}

.muted {
    color: #aab7d1;
    font-size: 13px;
}

.status-card {
    background: #17233a;
    border: 1px solid #344361;
    border-radius: 14px;
    padding: 16px;
}

div.stButton > button,
div.stDownloadButton > button {
    width: 100%;
    border: 0;
    border-radius: 12px;
    padding: 12px 16px;
    font-weight: 700;
    color: white;
    background: linear-gradient(100deg, #7657ff, #277bdc);
    transition: .2s ease;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {
    transform: translateY(-2px);
    color: white;
    box-shadow: 0 8px 24px rgba(89,91,255,.28);
}

.stTextArea textarea,
.stTextInput input,
.stNumberInput input,
[data-baseweb="select"] {
    background-color: #111b30 !important;
    color: white !important;
}

div[data-testid="stFileUploader"] {
    background: #111b30;
    padding: 15px;
    border-radius: 14px;
    border: 1px dashed #52658c;
}

h1, h2, h3 {
    color: #f5f7ff;
}

hr {
    border-color: #293754;
}

</style>
""", unsafe_allow_html=True)


# ------------------------- CONSTANTS ------------------------

STYLES_3D = [
    "Barbi 3D",
    "Cartoon 3D",
    "Thriller 3D",
    "Horror 3D",
    "Korean 3D",
    "Japan 3D",
    "Chinese 3D",
    "American 3D",
    "African 3D"
]

STYLES_2D = [
    "Barbi 2D",
    "Cartoon 2D",
    "Thriller 2D",
    "Horror 2D",
    "Korean 2D",
    "Japan 2D",
    "Chinese 2D",
    "American 2D",
    "African 2D"
]

STYLE_DESCRIPTIONS = {
    "Barbi": (
        "Original elegant doll-like characters, expressive eyes, "
        "beautiful fashion, fantasy settings and polished colourful "
        "visuals. Designs will be original, not copies of existing characters."
    ),
    "Cartoon": (
        "Expressive original characters, playful movements, imaginative "
        "environments and colourful family-friendly animation."
    ),
    "Thriller": (
        "Suspenseful cinematic atmosphere, dramatic lighting, mysterious "
        "environments and tension."
    ),
    "Horror": (
        "Original frightening creatures, eerie environments, atmospheric "
        "lighting and suspense."
    ),
    "Korean": (
        "Korean-inspired fashion, hairstyles, city environments and "
        "romance, drama or fantasy aesthetics."
    ),
    "Japan": (
        "Japanese anime-inspired visuals, expressive characters, landscapes, "
        "temples, action and fantasy."
    ),
    "Chinese": (
        "Chinese animation-inspired visuals, traditional clothing, palaces, "
        "martial arts and fantasy environments."
    ),
    "American": (
        "Polished Western animation aesthetics, detailed expressions and "
        "cinematic adventure, comedy or action."
    ),
    "African": (
        "Original African-inspired characters, distinctive hairstyles, "
        "clothing, architecture, landscapes and rich cultural details."
    )
}

PRESERVATION_OPTIONS = [
    "Original people and objects",
    "Actions and movements",
    "Facial expressions",
    "Background and environment",
    "Camera movements",
    "Scene sequence and transitions",
    "Original video duration"
]


# ------------------------ SESSION DATA ----------------------

if "jobs" not in st.session_state:
    st.session_state.jobs = []


# ------------------------ HELPER FUNCTIONS -------------------

def get_style_description(style):
    for name, description in STYLE_DESCRIPTIONS.items():
        if style.startswith(name):
            return description
    return ""


def create_duration(hours, minutes):
    total_seconds = hours * 3600 + minutes * 60

    if total_seconds <= 0:
        return None

    return {
        "hours": int(hours),
        "minutes": int(minutes),
        "total_seconds": int(total_seconds),
        "display": f"{hours} hour(s), {minutes} minute(s)"
    }


def create_job(job_type, prompt, style, duration,
               filename=None, extra_settings=None):

    job = {
        "job_id": str(uuid.uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "project_name": "AI Animation Studio",
        "job_type": job_type,
        "prompt": prompt,
        "style": style,
        "duration": duration,
        "uploaded_video": filename,
        "status": "Prepared - AI generation engine not connected",
        "engine": None,
        "settings": extra_settings or {}
    }

    st.session_state.jobs.insert(0, job)
    return job


def show_job(job):
    st.success("Your project has been prepared successfully.")

    st.write("**Project ID:**", job["job_id"])
    st.write("**Project type:**", job["job_type"])
    st.write("**Selected style:**", job["style"])
    st.write("**Status:**", job["status"])

    st.warning(
        "This is a prepared project configuration, not a rendered video. "
        "The AI generation engine must be connected before video rendering."
    )

    st.download_button(
        "⬇️ Download project configuration",
        data=json.dumps(job, indent=4),
        file_name=f"animation_project_{job['job_id'][:8]}.json",
        mime="application/json",
        key=f"download_{job['job_id']}"
    )


def duration_inputs(prefix):
    col1, col2 = st.columns(2)

    with col1:
        hours = st.number_input(
            "Hours",
            min_value=0,
            value=0,
            step=1,
            key=f"{prefix}_hours"
        )

    with col2:
        minutes = st.number_input(
            "Minutes",
            min_value=0,
            max_value=59,
            value=2,
            step=1,
            key=f"{prefix}_minutes"
        )

    duration = create_duration(int(hours), int(minutes))

    if duration:
        st.caption(f"Requested duration: {duration['display']}")
    else:
        st.info("Choose a duration greater than zero.")

    return duration


def style_selector(label, styles, key):
    style = st.selectbox(label, styles, key=key)
    st.info(get_style_description(style))
    return style


# ----------------------------- SIDEBAR -----------------------

with st.sidebar:
    st.markdown("## 🎬 AI Animation Studio")
    st.caption("Your creative animation workspace")

    st.divider()

    st.markdown("### System status")

    st.markdown("""
    <div class="status-card">
      <strong>Website</strong><br>
      <span style="color:#4ade80">● Running</span><br><br>
      <strong>Hosting</strong><br>
      <span class="muted">Render</span><br><br>
      <strong>AI video engine</strong><br>
      <span style="color:#fbbf24">● Not connected yet</span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Studio modules")
    st.write("✍️ Text to 3D")
    st.write("🎥 Video to 3D")
    st.write("🎨 Video to 2D")
    st.write("📁 My Projects")

    st.divider()
    st.caption("AI Animation Studio • Version 1.0")


# ----------------------------- HEADER ------------------------

st.markdown("""
<div class="hero">
    <h1>🎬 AI Animation Studio</h1>
    <p>Transform your ideas and videos into original animated worlds.</p>
    <p>Create stories, select visual styles and prepare animation projects.</p>
</div>
""", unsafe_allow_html=True)


# ----------------------------- DASHBOARD ---------------------

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="feature-card">
      <h3>✍️ Text to 3D</h3>
      <p class="muted">Prepare 3D animation projects from written prompts.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="feature-card">
      <h3>🎥 Video to 3D</h3>
      <p class="muted">Prepare real videos for 3D-style transformation.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="feature-card">
      <h3>🎨 Video to 2D</h3>
      <p class="muted">Prepare real videos for 2D animation transformation.</p>
    </div>
    """, unsafe_allow_html=True)


# -------------------------------- TABS ------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "✍️ Text to 3D",
    "🎥 Video to 3D",
    "🎨 Video to 2D",
    "📁 My Projects"
])


# ============================================================
# TAB 1 - TEXT TO 3D
# ============================================================

with tab1:
    st.header("Create a 3D animation from text")

    st.write(
        "Describe your story, characters, setting, actions and "
        "the events you want to see in your animation."
    )

    prompt = st.text_area(
        "Your animation prompt",
        placeholder=(
            "Example: A young African princess discovers a magical "
            "crystal in an ancient forest..."
        ),
        height=170,
        key="text3d_prompt"
    )

    style = style_selector(
        "Choose your 3D animation style",
        STYLES_3D,
        "text3d_style"
    )

    st.subheader("Video duration")
    duration = duration_inputs("text3d")

    st.subheader("Video settings")

    col1, col2 = st.columns(2)

    with col1:
        resolution = st.selectbox(
            "Target resolution",
            ["480p", "720p", "1080p", "4K"],
            index=1,
            key="text3d_resolution"
        )

    with col2:
        aspect_ratio = st.selectbox(
            "Aspect ratio",
            ["16:9 Landscape", "9:16 Portrait", "1:1 Square"],
            key="text3d_ratio"
        )

    consistency = st.select_slider(
        "Character and scene consistency",
        options=["Standard", "High", "Maximum"],
        value="High",
        key="text3d_consistency"
    )

    if st.button("🚀 Prepare 3D animation project", key="create_text3d"):
        if not prompt.strip():
            st.error("Please enter your animation prompt.")
        elif not duration:
            st.error("Please choose a valid duration.")
        else:
            job = create_job(
                "Text to 3D",
                prompt.strip(),
                style,
                duration,
                extra_settings={
                    "resolution": resolution,
                    "aspect_ratio": aspect_ratio,
                    "consistency": consistency
                }
            )
            show_job(job)


# ============================================================
# TAB 2 - VIDEO TO 3D
# ============================================================

with tab2:
    st.header("Transform a real video into 3D animation")

    st.write(
        "Upload a video and choose the 3D visual style. "
        "The future AI engine will attempt to preserve its original content."
    )

    video_3d = st.file_uploader(
        "Upload your original video",
        type=["mp4", "mov", "avi", "mkv", "webm"],
        key="video3d_upload"
    )

    if video_3d:
        st.video(video_3d)
        st.caption(f"Selected file: {video_3d.name}")

    style_3d = style_selector(
        "Choose your 3D animation style",
        STYLES_3D,
        "video3d_style"
    )

    preserve_3d = st.multiselect(
        "What should the transformation preserve?",
        PRESERVATION_OPTIONS,
        default=PRESERVATION_OPTIONS,
        key="video3d_preserve"
    )

    if st.button("🚀 Prepare 3D video transformation", key="create_video3d"):
        if video_3d is None:
            st.error("Please upload a video first.")
        else:
            job = create_job(
                "Real Video to 3D",
                (
                    "Transform the uploaded video into the selected "
                    "3D animation style. Preserve the original content "
                    "as closely as the generation model allows."
                ),
                style_3d,
                {
                    "display": "Original uploaded video duration",
                    "duration_detection": "Pending video engine"
                },
                filename=video_3d.name,
                extra_settings={
                    "preservation_requirements": preserve_3d
                }
            )
            show_job(job)


# ============================================================
# TAB 3 - VIDEO TO 2D
# ============================================================

with tab3:
    st.header("Transform a real video into 2D animation")

    st.write(
        "Upload a real video and select the 2D animation style "
        "you want to use."
    )

    video_2d = st.file_uploader(
        "Upload your original video",
        type=["mp4", "mov", "avi", "mkv", "webm"],
        key="video2d_upload"
    )

    if video_2d:
        st.video(video_2d)
        st.caption(f"Selected file: {video_2d.name}")

    style_2d = style_selector(
        "Choose your 2D animation style",
        STYLES_2D,
        "video2d_style"
    )

    preserve_2d = st.multiselect(
        "What should the transformation preserve?",
        PRESERVATION_OPTIONS,
        default=PRESERVATION_OPTIONS,
        key="video2d_preserve"
    )

    if st.button("🚀 Prepare 2D video transformation", key="create_video2d"):
        if video_2d is None:
            st.error("Please upload a video first.")
        else:
            job = create_job(
                "Real Video to 2D",
                (
                    "Transform the uploaded video into the selected "
                    "2D animation style. Preserve the original content "
                    "as closely as the generation model allows."
                ),
                style_2d,
                {
                    "display": "Original uploaded video duration",
                    "duration_detection": "Pending video engine"
                },
                filename=video_2d.name,
                extra_settings={
                    "preservation_requirements": preserve_2d
                }
            )
            show_job(job)


# ============================================================
# TAB 4 - PROJECT MANAGER
# ============================================================

with tab4:
    st.header("My animation projects")

    jobs = st.session_state.jobs

    if not jobs:
        st.info("You have not prepared any projects yet.")
    else:
        st.write(f"Prepared projects: **{len(jobs)}**")

        for index, job in enumerate(jobs):
            title = (
                f"{job['job_type']} | {job['style']} | "
                f"{job['job_id'][:8]}"
            )

            with st.expander(title):
                st.write("**Project ID:**", job["job_id"])
                st.write("**Created:**", job["created_at"])
                st.write("**Status:**", job["status"])
                st.write("**Prompt:**", job["prompt"])

                if job.get("uploaded_video"):
                    st.write("**Original video:**", job["uploaded_video"])

                st.download_button(
                    "Download project configuration",
                    data=json.dumps(job, indent=4),
                    file_name=f"project_{job['job_id'][:8]}.json",
                    mime="application/json",
                    key=f"project_download_{index}"
                )

        st.divider()

        if st.button("🗑️ Clear current session projects"):
            st.session_state.jobs = []
            st.rerun()


# ------------------------------- FOOTER -----------------------

st.divider()

st.markdown("""
<div style="text-align:center; padding:20px; color:#9aa9c5;">
    <strong>🎬 AI Animation Studio</strong><br>
    Create original animated worlds from your imagination.<br>
    <span style="font-size:12px;">
        Version 1.0 • AI rendering backend integration pending
    </span>
</div>
""", unsafe_allow_html=True)
