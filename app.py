import gc
import shutil
import tempfile
import time
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="YT Transcript Extractor",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Fira+Sans:wght@300;400;500&display=swap');
    :root {
        --bg:      #282a36;
        --surface: #1e1f29;
        --border:  #44475a;
        --cyan:    #8be9fd;
        --orange:  #ffb86c;
        --green:   #50fa7b;
        --pink:    #ff79c6;
        --purple:  #bd93f9;
        --text:    #f8f8f2;
        --muted:   #6272a4;
        --red:     #ff5555;
    }
    html, body, [class*="css"] {
        font-family: 'Fira Sans', sans-serif;
        background-color: var(--bg) !important;
        color: var(--text) !important;
    }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 2rem 2.5rem 3rem !important; }
    .app-header h1 {
        font-family: 'Fira Code', monospace;
        font-size: 1.65rem;
        font-weight: 600;
        color: var(--text) !important;
        margin: 0;
        line-height: 1.2;
    }
    .app-header .byline {
        font-size: 0.82rem;
        color: var(--muted);
        margin-top: 0.15rem;
    }
    .app-header .byline a { color: var(--cyan); text-decoration: none; }
    .section-divider {
        font-size: 0.7rem;
        font-weight: 600;
        color: rgba(98, 114, 164, 0.85);
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin: 0.75rem 0 0.4rem;
        padding-bottom: 0.25rem;
        border-bottom: 1px solid rgba(68, 71, 90, 0.6);
    }
    .stTextInput > div > div > input {
        background-color: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 4px !important;
        color: var(--text) !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 0.83rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--cyan) !important;
        box-shadow: 0 0 0 2px rgba(139,233,253,0.18) !important;
    }
    .stSelectbox > div > div {
        background-color: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 4px !important;
        color: var(--text) !important;
    }
    .stRadio label { font-size: 0.85rem !important; color: var(--text) !important; }
    .stRadio [data-baseweb="radio"] > div:first-child { border-color: var(--cyan) !important; }
    .stCheckbox label { font-size: 0.85rem !important; color: var(--text) !important; }
    .stCheckbox [data-baseweb="checkbox"] > div:first-child {
        border-color: var(--cyan) !important;
        background-color: var(--surface) !important;
    }
    .stButton > button {
        background-color: var(--cyan) !important;
        color: var(--bg) !important;
        border: none !important;
        border-radius: 4px !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 0.83rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.03em !important;
        transition: opacity 0.15s ease !important;
        width: 100% !important;
    }
    .stButton > button:hover { opacity: 0.82 !important; }
    .remove-btn > button {
        background-color: transparent !important;
        color: var(--red) !important;
        border: 1px solid rgba(255,85,85,0.4) !important;
        width: auto !important;
        font-size: 0.75rem !important;
        padding: 0.25rem 0.5rem !important;
    }
    .remove-btn > button:hover {
        background-color: rgba(255,85,85,0.1) !important;
        opacity: 1 !important;
    }
    .stDownloadButton > button {
        background-color: var(--surface) !important;
        color: var(--cyan) !important;
        border: 1px solid var(--cyan) !important;
        border-radius: 4px !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
    }
    .stDownloadButton > button:hover {
        background-color: rgba(139,233,253,0.12) !important;
    }
    .streamlit-expanderHeader {
        background-color: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 4px !important;
        color: var(--text) !important;
        font-size: 0.85rem !important;
    }
    .streamlit-expanderContent {
        border: 1px solid var(--border) !important;
        border-top: none !important;
        background-color: var(--surface) !important;
        border-radius: 0 0 4px 4px !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--surface) !important;
        border-radius: 6px 6px 0 0 !important;
        gap: 2px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: var(--muted) !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 0.82rem !important;
        padding: 0.4rem 1rem !important;
        border-radius: 4px 4px 0 0 !important;
    }
    .stTabs [aria-selected="true"] {
        color: var(--cyan) !important;
        background-color: rgba(139,233,253,0.08) !important;
        border-bottom: 2px solid var(--cyan) !important;
    }
    [data-testid="metric-container"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 0.6rem 0.9rem !important;
    }
    [data-testid="metric-container"] label {
        color: var(--muted) !important;
        font-size: 0.72rem !important;
        font-family: 'Fira Code', monospace !important;
        letter-spacing: 0.04em;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: var(--cyan) !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 1.3rem !important;
    }
    .stProgress > div > div { background-color: var(--cyan) !important; }
    .transcript-block {
        font-family: 'Fira Code', monospace;
        font-size: 0.78rem;
        line-height: 1.75;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 0.9rem 1.1rem;
        max-height: 340px;
        overflow-y: auto;
        white-space: pre-wrap;
        word-break: break-word;
        color: var(--text);
    }
    .ts { color: var(--cyan); font-weight: 500; }
    .error-block {
        font-family: 'Fira Code', monospace;
        font-size: 0.82rem;
        color: var(--red);
        background: rgba(255,85,85,0.08);
        border: 1px solid rgba(255,85,85,0.35);
        border-radius: 4px;
        padding: 0.6rem 1rem;
    }
    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 4rem 2rem;
        color: var(--muted);
        font-family: 'Fira Code', monospace;
        font-size: 0.82rem;
        border: 1px dashed var(--border);
        border-radius: 8px;
        text-align: center;
        gap: 0.5rem;
    }
    .empty-state .empty-icon { font-size: 2rem; margin-bottom: 0.5rem; }
    .empty-state strong { color: var(--text); font-size: 0.9rem; }
    hr { border-color: var(--border) !important; margin: 1rem 0 !important; }
    [data-testid="stSidebar"] {
        background-color: var(--surface) !important;
        border-right: 1px solid var(--border) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# GitHub-compatible model catalogue
# ---------------------------------------------------------------------------
# Currently only tiny (~39 MB) is committed to the repository — safely under
# GitHub's 100 MB per-file hard limit.
# base exceeded the limit on disk and is excluded for now.

GITHUB_SAFE_MODELS: dict[str, dict] = {
    "tiny": {
        "label": "tiny",
        "size_mb": 39,
        "params": "39 M",
        "speed_hint": "⚡ Only available model — more coming soon",
        "color": "var(--green)",
    },
}

# Cache directory used by the pre-download script and by Whisper at runtime.
# This folder is listed in .gitignore — it stores downloaded weights locally
# without polluting the Git history.
WHISPER_CACHE_DIR = Path(__file__).parent / ".whisper_cache"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _section_divider(label: str) -> None:
    st.markdown(f'<p class="section-divider">{label}</p>', unsafe_allow_html=True)


def format_timestamp(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


# ---------------------------------------------------------------------------
# Dependency installation — cached so it runs at most once per process
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def _ensure_dependencies() -> None:
    import subprocess
    import sys

    packages = [
        ("yt-dlp", "yt_dlp"),
        ("openai-whisper", "whisper"),
        ("numpy", "numpy"),
        ("moviepy", "moviepy"),
        ("scipy", "scipy"),
    ]
    for pkg_name, import_name in packages:
        try:
            __import__(import_name)
        except ImportError:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pkg_name,
                 "-q", "--break-system-packages"]
            )


# ---------------------------------------------------------------------------
# Whisper model — cached so weights are loaded once per (model_size, process)
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def _load_whisper_model(model_size: str):
    import whisper

    # Prefer the local cache directory so we never re-download at inference
    # time; fall back to Whisper's default location if not found there.
    local_path = WHISPER_CACHE_DIR / f"{model_size}.pt"
    if local_path.exists():
        return whisper.load_model(model_size, download_root=str(WHISPER_CACHE_DIR))
    return whisper.load_model(model_size)


# ---------------------------------------------------------------------------
# Core pipeline
# ---------------------------------------------------------------------------
def download_video(url: str, output_path: Path, status) -> str:
    import yt_dlp

    primary_opts = {
        "format": "best[ext=mp4][protocol!=m3u8_native]/best[ext=mp4]/best",
        "outtmpl": str(output_path),
        "quiet": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"],
                "skip": ["hls", "dash"],
            }
        },
        "retries": 10,
        "fragment_retries": 10,
        "source_address": "0.0.0.0",
    }
    try:
        with yt_dlp.YoutubeDL(primary_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "Unknown")
            status.write(f"📥 Downloaded: **{title}**")
            return title
    except Exception:
        status.write("⚠️ Primary download failed — retrying with fallback client…")
        fallback_opts = {
            "format": "best",
            "outtmpl": str(output_path),
            "quiet": True,
            "extractor_args": {
                "youtube": {"player_client": ["android_embedded", "tv_embedded"]}
            },
        }
        with yt_dlp.YoutubeDL(fallback_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "Unknown")
            status.write(f"📥 Downloaded (fallback): **{title}**")
            return title


def extract_audio(video_path: Path, audio_path: Path, status) -> None:
    try:
        from moviepy import VideoFileClip
    except ImportError:
        from moviepy.editor import VideoFileClip

    status.write("🎵 Extracting audio track…")
    with VideoFileClip(str(video_path)) as video:
        video.audio.write_audiofile(
            str(audio_path),
            fps=16000,
            nbytes=2,
            codec="pcm_s16le",
            logger=None,
        )
    status.write("🎵 Audio saved as 16 kHz mono WAV")


def transcribe_audio(audio_path: Path, model_size: str, status, progress_bar) -> dict:
    import numpy as np
    from scipy.io import wavfile

    status.write(f"🤖 Loading Whisper **{model_size}** model…")
    progress_bar.progress(0.25, text="Loading model weights…")
    model = _load_whisper_model(model_size)

    status.write("📂 Reading audio into memory…")
    progress_bar.progress(0.50, text="Reading audio…")
    sample_rate, audio_data = wavfile.read(str(audio_path))

    if audio_data.dtype == np.int16:
        audio_data = audio_data.astype("float32") / 32768.0
    elif audio_data.dtype == np.int32:
        audio_data = audio_data.astype("float32") / 2147483648.0
    elif audio_data.dtype == np.float64:
        audio_data = audio_data.astype("float32")

    if audio_data.ndim > 1:
        audio_data = audio_data.mean(axis=1)

    if sample_rate != 16000:
        from scipy import signal
        num_samples = int(len(audio_data) * 16000 / sample_rate)
        audio_data = signal.resample(audio_data, num_samples)
        status.write(f"🔄 Resampled {sample_rate} Hz → 16 000 Hz")

    status.write("✍️ Transcribing — this may take several minutes…")
    progress_bar.progress(0.75, text="Transcribing audio…")
    result = model.transcribe(audio_data, language="en", verbose=False, fp16=False)

    n_segments = len(result.get("segments", []))
    status.write(f"✅ Done — **{n_segments}** segments")
    progress_bar.progress(1.0, text="Complete!")
    return result


def process_video(url: str, model_size: str, status, progress_bar) -> dict:
    """Download → extract → transcribe one URL. Always cleans up temp files."""
    temp_dir = Path(tempfile.mkdtemp())
    video_path = temp_dir / "video.mp4"
    audio_path = temp_dir / "audio.wav"

    result = {
        "url": url,
        "title": "Unknown",
        "segments": [],
        "full_text": "",
        "error": None,
    }

    try:
        status.write(f"🔗 Fetching: `{url}`")

        try:
            result["title"] = download_video(url, video_path, status)
        except Exception as exc:
            result["error"] = f"Download failed: {exc}"
            return result

        if not video_path.exists() or video_path.stat().st_size < 1_000:
            result["error"] = "Download produced an empty or missing file."
            return result

        size_mb = video_path.stat().st_size / 1_048_576
        status.write(f"📦 File size: **{size_mb:.1f} MB**")

        try:
            extract_audio(video_path, audio_path, status)
        except Exception as exc:
            result["error"] = f"Audio extraction failed: {exc}"
            return result

        try:
            transcription = transcribe_audio(audio_path, model_size, status, progress_bar)
        except Exception as exc:
            result["error"] = f"Transcription failed: {exc}"
            return result

        result["segments"] = transcription.get("segments", [])
        result["full_text"] = transcription.get("text", "")
    finally:
        gc.collect()
        time.sleep(0.3)
        shutil.rmtree(temp_dir, ignore_errors=True)

    return result


# ---------------------------------------------------------------------------
# Transcript formatting
# ---------------------------------------------------------------------------
def _format_segments(segments: list) -> str:
    lines = []
    for seg in segments:
        start = format_timestamp(seg["start"])
        end = format_timestamp(seg["end"])
        lines.append(f"[{start} → {end}]  {seg['text'].strip()}")
    return "\n".join(lines)


def build_transcript_text(result: dict) -> str:
    lines = [
        f"# {result['title']}",
        f"URL: {result['url']}",
        "",
        "## Timestamped Transcript",
        "",
        _format_segments(result.get("segments", [])),
        "",
        "## Full Transcript",
        "",
        result.get("full_text", ""),
    ]
    return "\n".join(lines)


def build_combined_text(results: list) -> str:
    parts = ["# Combined Transcripts\n"]
    for i, r in enumerate(results, 1):
        parts.append(f"---\n\n## Video {i}: {r['title']}")
        if r.get("error"):
            parts.append(f"**Error:** {r['error']}\n")
        else:
            parts.append(build_transcript_text(r))
        parts.append("")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Result display
# ---------------------------------------------------------------------------
def _display_metric_cards(results: list) -> None:
    successful = [r for r in results if not r.get("error")]
    if not successful:
        return

    n_segments = sum(len(r.get("segments", [])) for r in successful)
    n_words = sum(len(r.get("full_text", "").split()) for r in successful)
    last_ends = [r["segments"][-1]["end"] for r in successful if r.get("segments")]
    avg_duration = sum(last_ends) / len(last_ends) if last_ends else 0.0

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Videos", str(len(successful)))
    with m2:
        st.metric("Segments", f"{n_segments:,}")
    with m3:
        st.metric("Words", f"{n_words:,}")
    with m4:
        st.metric("Avg Duration", format_timestamp(avg_duration))


def _render_transcript_tab(results: list) -> None:
    for i, result in enumerate(results, 1):
        _section_divider(f"Video {i} — {result['title']}")
        st.caption(result["url"])

        if result.get("error"):
            st.markdown(
                f'<div class="error-block">⚠ {result["error"]}</div>',
                unsafe_allow_html=True,
            )
            continue

        parts = []
        for seg in result.get("segments", []):
            start = format_timestamp(seg["start"])
            end = format_timestamp(seg["end"])
            parts.append(f'<span class="ts">[{start} → {end}]</span>  {seg["text"].strip()}')

        block = "\n".join(parts) or result.get("full_text", "—")
        st.markdown(
            f'<div class="transcript-block">{block}</div>',
            unsafe_allow_html=True,
        )

        safe_title = "".join(
            c if c.isalnum() or c in " _-" else "_" for c in result["title"]
        )[:60]
        st.download_button(
            label="⬇ Download .md",
            data=build_transcript_text(result).encode("utf-8"),
            file_name=f"{safe_title}.md",
            mime="text/markdown",
            key=f"dl_ts_{i}",
        )


def _render_fulltext_tab(results: list) -> None:
    for i, result in enumerate(results, 1):
        _section_divider(f"Video {i} — {result['title']}")
        st.caption(result["url"])

        if result.get("error"):
            st.markdown(
                f'<div class="error-block">⚠ {result["error"]}</div>',
                unsafe_allow_html=True,
            )
            continue

        st.markdown(
            f'<div class="transcript-block">{result.get("full_text", "—")}</div>',
            unsafe_allow_html=True,
        )

        safe_title = "".join(
            c if c.isalnum() or c in " _-" else "_" for c in result["title"]
        )[:60]
        st.download_button(
            label="⬇ Download .md",
            data=build_transcript_text(result).encode("utf-8"),
            file_name=f"{safe_title}.md",
            mime="text/markdown",
            key=f"dl_full_{i}",
        )


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
def _init_session_state() -> None:
    defaults = {
        "results": None,
        "url_list": [""],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    _init_session_state()

    # Ensure pip packages are installed before anything else.
    _ensure_dependencies()

    # ── Header ────────────────────────────────────────────────────────────────
    col_icon, col_title = st.columns([0.05, 0.95])
    with col_icon:
        st.markdown("🎙️")
    with col_title:
        st.markdown(
            '<div class="app-header">'
            "<h1>YouTube Transcript Extractor</h1>"
            '<p class="byline">By '
            '<a href="https://www.linkedin.com/in/vinicius-stanula/?locale=en-US">Vinicius Stanula</a>'
            " · built with Streamlit 🎈</p>"
            "</div>",
            unsafe_allow_html=True,
        )
    st.markdown("----")

    # ── Sidebar — settings ────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(
            '<div class="app-header"><h1 style="font-size:1rem">⚙️ Settings</h1></div>',
            unsafe_allow_html=True,
        )

        _section_divider("Whisper model")

        # Only tiny is available right now — a selectbox requires 2+ options,
        # so we hard-code the model and show a simple info label instead.
        model_size = "tiny"
        meta = GITHUB_SAFE_MODELS[model_size]
        st.markdown(
            f'<p style="font-size:0.85rem;color:{meta["color"]}">'
            f'🤖 Model: <strong>{model_size}</strong> &nbsp;·&nbsp; ~{meta["size_mb"]} MB'
            f'&nbsp;·&nbsp; {meta["params"]} params</p>'
            f'<p style="font-size:0.72rem;color:var(--muted);margin-top:-0.3rem">'
            f"More models coming soon via Git LFS.</p>",
            unsafe_allow_html=True,
        )

        _section_divider("Options")
        combine_download = st.checkbox(
            "Combined download (batch)",
            value=True,
            help="Show a single-file download for all transcripts in batch mode.",
        )

        if st.session_state.results:
            st.markdown("---")
            if st.button("🗑 Clear results"):
                st.session_state.results = None
                st.rerun()

    # ── Main layout ────────────────────────────────────────────────────────────
    c1, c2 = st.columns([1.4, 4])

    # ── Left panel ─────────────────────────────────────────────────────────────
    with c1:
        _section_divider("Source")
        mode = st.radio(
            "Input mode:",
            ["Single video", "Multiple videos"],
            horizontal=True,
            help=(
                "**Single video** — one URL input field.\n\n"
                "**Multiple videos** — add as many URLs as you like; "
                "all are processed sequentially in one run."
            ),
        )

        urls: list[str] = []

        if mode == "Single video":
            url_input = st.text_input(
                "YouTube URL:",
                placeholder="https://www.youtube.com/watch?v=...",
                help="Paste any public YouTube URL.",
            )
            if url_input.strip():
                urls = [url_input.strip()]
        else:
            for i, existing in enumerate(st.session_state.url_list):
                col_inp, col_rm = st.columns([9, 1])
                with col_inp:
                    st.session_state.url_list[i] = st.text_input(
                        f"URL {i + 1}:",
                        value=existing,
                        placeholder="https://www.youtube.com/watch?v=...",
                        key=f"url_{i}",
                    )
                with col_rm:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if len(st.session_state.url_list) > 1:
                        st.markdown('<div class="remove-btn">', unsafe_allow_html=True)
                        if st.button("✕", key=f"rm_{i}", help="Remove this URL"):
                            st.session_state.url_list.pop(i)
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)

            if st.button("＋ Add URL"):
                st.session_state.url_list.append("")
                st.rerun()

            urls = [u.strip() for u in st.session_state.url_list if u.strip()]

        _section_divider("Run")

        if mode == "Multiple videos" and urls:
            st.caption(f"{len(urls)} URL{'s' if len(urls) != 1 else ''} queued")

        fetch = st.button(
            "Extract Transcript ✨" if mode == "Single video" else "Extract All Transcripts ✨",
            disabled=not urls,
            help="Start downloading and transcribing the video(s) above.",
        )

        if not urls:
            st.info("Enter at least one URL to begin.", icon="ℹ️")

    # ── Right panel ─────────────────────────────────────────────────────────────
    with c2:
        if fetch and urls:
            new_results: list = []
            for idx, url in enumerate(urls):
                label = f"Video {idx + 1} of {len(urls)}"
                progress_bar = st.progress(0.0, text=f"⏳ {label} — starting…")
                with st.status(f"Processing {label}…", expanded=True) as status_ctx:
                    result = process_video(url, model_size, status_ctx, progress_bar)
                    if result.get("error"):
                        status_ctx.update(
                            label=f"❌ {label} failed",
                            state="error",
                            expanded=False,
                        )
                    else:
                        status_ctx.update(
                            label=f"✅ {label} — {result['title']}",
                            state="complete",
                            expanded=False,
                        )
                time.sleep(1.2)
                progress_bar.empty()
                new_results.append(result)

            st.session_state.results = new_results

        if st.session_state.results:
            results = st.session_state.results
            successful = [r for r in results if not r.get("error")]
            failed = [r for r in results if r.get("error")]

            if successful and not failed:
                st.success(
                    f"✅ {len(successful)} video{'s' if len(successful) != 1 else ''} "
                    "transcribed successfully.",
                    icon="🎉",
                )
            elif successful and failed:
                st.warning(
                    f"⚠️ {len(successful)} succeeded, {len(failed)} failed. "
                    "See details below.",
                )
            else:
                st.error("All videos failed to process. Check the error details below.")

            if successful:
                _display_metric_cards(results)
                st.markdown("")

            if len(results) > 1 and combine_download and successful:
                st.download_button(
                    label="⬇ Download all transcripts (.md)",
                    data=build_combined_text(results).encode("utf-8"),
                    file_name="transcripts_combined.md",
                    mime="text/markdown",
                    key="dl_combined",
                )

            tab_ts, tab_full = st.tabs(["📅 Timestamped", "📃 Full Text"])
            with tab_ts:
                _render_transcript_tab(results)
            with tab_full:
                _render_fulltext_tab(results)
        else:
            st.markdown(
                """
                <div class="empty-state">
                    <div class="empty-icon">🎙️</div>
                    <strong>No transcripts yet</strong>
                    <span>Paste a YouTube URL on the left and hit <em>Extract Transcript</em>.</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
