# Creator Control Room

One dashboard for a short-form creator posting the same videos to **TikTok, Instagram Reels and YouTube Shorts**, built around startup, AI, news and skit content.

**Live dashboard (private to you):** https://claude.ai/artifact/APDiceiirp1b9CA7biT1DG

`index.html` is the source of that artifact. Its data (videos, posts, ideas, challenge days, brand kit) lives in the artifact's private database, and only you can read or change it. The AI features call Claude from inside the page using your own Claude account.

## What's in it

| Tab | What it does |
|---|---|
| **Today** | Challenge day counter, today's posting checklist, last 7 days vs the 7 before, what to film next, your best recent post. |
| **Recreate** | Paste a video link plus its transcript, or upload the video file. Claude reads frames and on-screen captions, breaks down the hook, beats, pacing and edit style, rewrites it as a script in your voice, and writes a **prompt for your AI editor chat**. Videos move through stages: To script, To film, To post, Posted. |
| **Ideas** | Claude pitches 8 ideas at a time, based on your best and worst posts and the videos you saved. Paste today's headlines for timely news angles. Save ideas, then "Script it" to get a script, a shot list and an editor prompt. |
| **Analytics** | Log posts by hand, or paste exports or screenshots and let Claude pull out the numbers. See views by platform, median views per pillar, engagement rate, and viral hits (posts at 3× or more of your typical views). "Analyze my performance" gives you what's working, your viral formula and 3 experiments for next week. |
| **90-day challenge** | A 90-square grid. A day counts when you post on 1, 2 or all 3 platforms (you choose). Posts you log tick themselves off. Shows streaks. |
| **Brand kit** | Your voice, audience, pillars, CTA and editing preferences. Every AI prompt uses it. Also builds a one-time **editor setup prompt** to paste into your editor chat. |

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

1. Fill in the **Brand kit**, copy the editor setup prompt, and paste it into your editor Claude chat once.
2. Start the **90-day challenge**.
3. Every day: pick a reference in **Recreate** or an idea in **Ideas**, film the script, paste the editor prompt plus your footage into the editor chat, post, then log the post in **Analytics**.
4. Weekly: press **Analyze my performance** and act on the 3 experiments.
