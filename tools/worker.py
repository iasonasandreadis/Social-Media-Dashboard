"""Download a video's audio from a link and transcribe it. Prints one JSON object.

Used by the Creator Control Room cloud transcriber routine.
Needs: python3 -m pip install yt-dlp faster-whisper, and ffmpeg.
"""
import json, os, subprocess, sys, tempfile, urllib.parse, urllib.request

url = sys.argv[1]
out = {"url": url}
d = tempfile.mkdtemp()
UA = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148"}


def via_ytdlp():
    import yt_dlp
    opts = {"format": "bestaudio/best", "outtmpl": os.path.join(d, "a.%(ext)s"), "quiet": True, "no_warnings": True,
            "noplaylist": True, "noprogress": True}
    with yt_dlp.YoutubeDL(opts) as y:
        info = y.extract_info(url, download=True)
        path = y.prepare_filename(info)
    meta = dict(title=info.get("title") or "", uploader=info.get("uploader") or info.get("channel") or "",
                description=(info.get("description") or "")[:1500], duration=info.get("duration"))
    return path, meta


def via_tikwm():
    api = "https://www.tikwm.com/api/?url=" + urllib.parse.quote(url, safe="")
    data = json.load(urllib.request.urlopen(urllib.request.Request(api, headers=UA), timeout=30))
    v = data.get("data") or {}
    media = v.get("play") or v.get("wmplay")
    if not media:
        raise RuntimeError(data.get("msg") or "no video in response")
    path = os.path.join(d, "v.mp4")
    with urllib.request.urlopen(urllib.request.Request(media, headers=UA), timeout=60) as r, open(path, "wb") as f:
        f.write(r.read())
    author = v.get("author") or {}
    return path, dict(title=v.get("title") or "", uploader=author.get("unique_id") or "", description=v.get("title") or "",
                      duration=v.get("duration"))


try:
    try:
        if os.environ.get("FORCE_FALLBACK"):
            raise RuntimeError("forced")
        path, meta = via_ytdlp()
    except Exception as first:
        if "tiktok.com" not in url:
            raise
        out["note"] = f"yt-dlp failed, used fallback ({str(first)[:80]})"
        path, meta = via_tikwm()
    out.update(meta)
    import numpy as np
    from faster_whisper import WhisperModel
    raw = subprocess.run(["ffmpeg", "-nostdin", "-i", path, "-vn", "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
    model = WhisperModel("small", device="cpu", compute_type="int8")
    segs, inf = model.transcribe(audio, vad_filter=True)
    out["language"] = inf.language
    out["transcript"] = "\n".join(f"[{int(s.start)//60}:{int(s.start)%60:02d}] {s.text.strip()}" for s in segs)
except Exception as e:
    out["error"] = f"{type(e).__name__}: {e}"[:400]
print(json.dumps(out))
