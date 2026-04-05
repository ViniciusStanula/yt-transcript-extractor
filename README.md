# 🎙️ yt-transcript-extractor

> **Drop a YouTube URL. Get every word.**

A lightweight Streamlit app that extracts clean, timestamped transcripts from any YouTube video — no YouTube API key needed, no account required. Powered by [OpenAI Whisper](https://github.com/openai/whisper) and built with Streamlit.

---

## ⚠️ Deployment status

**This app currently runs locally only.**

YouTube actively blocks audio download requests coming from cloud server IP addresses (AWS, GCP, Azure, and others), which is what Streamlit Community Cloud runs on. Attempting to run it there will result in HTTP 403 errors on every video.

The plan is to solve this and bring it to a live Streamlit dashboard.

---

## Features

- 🔗 Paste any public YouTube URL and extract a full transcript
- 🕐 Timestamped segments — know exactly when every word was said
- 📦 Batch mode — process multiple videos in one run
- ⬇️ Download individual or combined transcripts as `.md` files

---

## Current model status

**Only the `tiny` Whisper model (~39 MB) is available in this version.**

GitHub enforces a hard 100 MB per-file limit, and the next model up (`base`) exceeds that on disk. The `tiny` model handles transcription well for most use cases, though accuracy on complex audio may be limited.

| Model  | Size     | Status |
|--------|----------|--------|
| tiny   | ~39 MB   | ✅ Available now |
| base   | ~140 MB  | 🔜 Planned (via Git LFS) |
| small  | ~244 MB  | 🔜 Planned (via Git LFS) |
| medium | ~769 MB  | 🔜 Planned (via Git LFS) |
| large  | ~1.55 GB | 🔜 Planned (via Git LFS) |

---

## 🗺️ Roadmap

- [ ] **Fix cloud deployment** — bypass YouTube's cloud IP blocks
- [ ] **Live Streamlit dashboard** — once the download issue is resolved, deploy publicly on Streamlit Community Cloud
- [ ] **More Whisper models** — add `base` and `small` via Git LFS so users can trade speed for accuracy
- [ ] **Gemini integration** — connect Google Gemini to automatically summarise transcripts, extract key points, and answer questions about the video content
- [ ] **Language support** — extend beyond English

---

## 🛠️ Running locally

**1. Clone the repo**
```bash
git clone https://github.com/ViniciusStanula/yt-transcript-extractor.git
cd yt-transcript-extractor
```

**2. Install dependencies**
```bash
pip install streamlit yt-dlp openai-whisper moviepy scipy numpy
```

**3. Run the app**
```bash
streamlit run app.py
```

The `tiny.pt` model is already in `.whisper_cache/` — no extra download needed.

---

## 📄 License

MIT © 2026 — see [LICENSE](LICENSE) for details.
