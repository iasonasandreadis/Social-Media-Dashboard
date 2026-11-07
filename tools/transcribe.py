#!/usr/bin/env python3
"""Transcribe a TikTok, Instagram Reel or YouTube video from its link.

Downloads the audio with yt-dlp and transcribes it locally with faster-whisper,
then prints a timestamped transcript you can paste into the Recreate tab of
Creator Control Room.

Setup (once):
    pip install -r tools/requirements.txt
    # ffmpeg must be installed: `brew install ffmpeg` / `apt install ffmpeg` / `winget install ffmpeg`

Usage:
    python tools/transcribe.py https://www.tiktok.com/@someone/video/123
    python tools/transcribe.py <link> --model small --plain
    python tools/transcribe.py <link> --cookies-from-browser chrome   # Instagram often needs this
"""
import argparse
import os
import sys
import tempfile


def fmt(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    return f"{m}:{s:02d}"


def download_audio(url: str, out_dir: str, cookies_browser: str | None) -> str:
    try:
        import yt_dlp
    except ImportError:
        sys.exit("yt-dlp is not installed. Run: pip install -r tools/requirements.txt")
    opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(out_dir, "audio.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
    }
    if cookies_browser:
        opts["cookiesfrombrowser"] = (cookies_browser,)
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
    path = os.path.join(out_dir, "audio.mp3")
    if not os.path.exists(path):
        sys.exit("Download finished but no audio file was produced. Is ffmpeg installed?")
    title = info.get("title") or ""
    uploader = info.get("uploader") or info.get("channel") or ""
    print(f"# {title}" + (f"  ({uploader})" if uploader else ""), file=sys.stderr)
    return path


def transcribe(path: str, model_name: str, language: str | None):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("faster-whisper is not installed. Run: pip install -r tools/requirements.txt")
    model = WhisperModel(model_name, device="auto", compute_type="auto")
    segments, info = model.transcribe(path, language=language, vad_filter=True)
    print(f"# language: {info.language}", file=sys.stderr)
    return list(segments)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", help="Video link (TikTok, Instagram, YouTube, or a local file path)")
    ap.add_argument("--model", default="base", help="Whisper model: tiny, base, small, medium, large-v3 (default: base)")
    ap.add_argument("--language", default=None, help="Force a language code, e.g. en")
    ap.add_argument("--plain", action="store_true", help="No timestamps")
    ap.add_argument("--cookies-from-browser", dest="cookies", default=None,
                    help="Use your browser's login cookies (chrome, firefox, safari, edge) for Instagram/private videos")
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        audio = args.url if os.path.exists(args.url) else download_audio(args.url, tmp, args.cookies)
        segments = transcribe(audio, args.model, args.language)

    for seg in segments:
        text = seg.text.strip()
        print(text if args.plain else f"[{fmt(seg.start)}] {text}")


if __name__ == "__main__":
    main()
