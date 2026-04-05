# 🎙️ yt-transcript-extractor

> **Drop a YouTube URL. Get every word.**

A lightweight Streamlit app that extracts clean, timestamped transcripts from any YouTube video, no YouTube API key needed, no account required. Powered by [OpenAI Whisper](https://github.com/openai/whisper).

---

## ✨ Features

- 🔗 Paste any public YouTube URL and extract a full transcript
- 🕐 Timestamped segments — know exactly when every word was said
- 📦 Batch mode — process multiple videos in one run
- ⬇️ Download individual or combined transcripts as `.md` files

---

## ⚠️ Current model status

**Only the `tiny` Whisper model (~39 MB) is available in this version.**

| Model  | Size     | Status |
|--------|----------|--------|
| tiny   | ~39 MB   | ✅ Available now |
| base   | ~140 MB  | 🔜 Planned (via Git LFS) |
| small  | ~244 MB  | 🔜 Planned (via Git LFS) |
| medium | ~769 MB  | 🔜 Planned (via Git LFS) |
| large  | ~1.55 GB | 🔜 Planned (via Git LFS) |

---

## 🗺️ Roadmap

- [ ] **More Whisper models** — add `base` and `small` via Git LFS so users can trade speed for accuracy
- [ ] **Gemini integration** — connect Google Gemini to automatically summarise transcripts, extract key points, and answer questions about the video content
- [ ] **Language support** — extend beyond English to Whisper's full 99-language support

---

## 📄 License

MIT © 2026 — see [LICENSE](LICENSE) for details.
