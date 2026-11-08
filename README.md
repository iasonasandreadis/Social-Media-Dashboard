# Creator Control Room

One dashboard for a short-form creator posting the same videos to **TikTok, Instagram Reels and YouTube Shorts**, built around startup, AI, news and skit content.

**Live dashboard (private to you):** https://claude.ai/artifact/APDiceiirp1b9CA7biT1DG

`index.html` is the source of that artifact. Its data (videos, posts, ideas, challenge days, brand kit) lives in the artifact's private database, and only you can read or change it. The AI features call Claude from inside the page using your own Claude account.

## What's in it

Kept lean on purpose. More features get added later as needed.

- **90-day challenge** (always at the top): day counter, streak, and three buttons to tick where you posted today. A day counts when you post on at least one platform.
- **Recreate:** paste a TikTok, Reel or YouTube link. A Claude cloud routine on your own subscription downloads it, transcribes it with Whisper, gives you the original script word for word and writes an editor prompt for recreating it. They show up in the app 2 to 4 minutes later. See *How link transcription works* below.
- **Ideas:** one button gives you 8 ideas, each with the first line to say on camera. You can paste news first for timely ideas.
- **Stats:** log each post (video, platform, views, likes), see this week's numbers, and ask Claude what's working.

## How link transcription works

1. The app saves the link as a "working" entry and starts the **Creator app transcriber** routine (`trig_01PC1unX4e44jJUkkzwmephv`) through your Claude Code connector.
2. The routine runs in the `creator-transcriber` cloud environment, which has open internet access. It runs `tools/worker.py`: it downloads the audio with yt-dlp (with a backup downloader for TikTok) and transcribes it with faster-whisper.
3. Claude formats the original script (word for word, no rewriting), writes the editor prompt and saves them into the app's private data. The app updates by itself.

What works: TikTok. What usually fails: YouTube (it blocks downloads from cloud servers) and Instagram (it needs a login). These show up in the app as "Couldn't transcribe" with the reason.

You can also run `python tools/transcribe.py <link>` on your own computer for a word-for-word transcript of any link.

## Workflow

1. Start the challenge.
2. Every day: paste a link in Recreate, film the script, give your editor chat the editor prompt plus the original video and your footage, then post it.
3. Log the post in Stats. Once a week, press **Analyze my stats**.
