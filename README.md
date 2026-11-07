# Creator Control Room

One dashboard for a short-form creator posting the same videos to **TikTok, Instagram Reels and YouTube Shorts**, built around startup, AI, news and skit content.

**Live dashboard (private to you):** https://claude.ai/artifact/APDiceiirp1b9CA7biT1DG

`index.html` is the source of that artifact. Its data (videos, posts, ideas, challenge days, brand kit) lives in the artifact's private database, and only you can read or change it. The AI features call Claude from inside the page using your own Claude account.

## What's in it

Kept lean on purpose. More features get added later as needed.

- **90-day challenge** (always at the top): day counter, streak, and three buttons to tick where you posted today. A day counts when you post on at least one platform.
- **Recreate:** paste a video link plus its transcript, or upload the video file. You get back one prompt to paste into your AI editor chat with your footage. It covers why the original works, your version of the script, edit instructions and captions for each platform.
- **Ideas:** one button gives you 8 ideas, each with the first line to say on camera. You can paste news first for timely ideas.
- **Stats:** log each post (video, platform, views, likes), see this week's numbers, and ask Claude what's working.

## Getting transcripts

The page can't download videos from TikTok, Instagram or YouTube itself (the artifact sandbox blocks outside network access). Three ways in:

1. **YouTube:** open *…more*, then *Show transcript*, and copy it into the Recreate form.
2. **Upload the video file:** Claude reads burned-in captions from the frames. This works well for most short-form videos.
3. **Word-for-word audio transcript:** run the local script:

```bash
pip install -r tools/requirements.txt     # also needs ffmpeg installed
python tools/transcribe.py "https://www.tiktok.com/@someone/video/123"
python tools/transcribe.py "<instagram link>" --cookies-from-browser chrome
```

It prints a timestamped transcript. Paste it into the Recreate tab.

## Workflow

1. Start the challenge.
2. Every day: recreate a video or pick an idea, film it, paste the editor prompt plus your footage into your editor chat, post it.
3. Log the post in Stats. Once a week, press **Analyze my stats**.
