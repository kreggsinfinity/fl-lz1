# 🎙️ Slow English Podcast Lounge (Repository 1 / Variety 1)

Automated video generator for **Slow Conversational English Podcasts** designed for Facebook Pages and YouTube channels.

## 🌟 Key Features
- **Dual Hosts**: Natural dialogues between Host 1 (Emma: `en-US-AvaNeural`) and Host 2 (Andrew: `en-US-AndrewNeural`).
- **Optimal Pace**: `-15%` speaking rate for deliberate, crystal-clear American pronunciation.
- **Dynamic Waveform**: Animated pulsing 8-bar equalizer reacting to conversation turns.
- **Studio Layout**: Modern high-definition studio backdrop with speaker badges and high-contrast yellow keyword highlights.
- **Auto Facebook Publishing**: Built-in Meta Graph API chunked resumable upload script (`publish_facebook.py`).
- **GitHub Actions Ready**: Automated daily video generation and publishing schedule.

## 🚀 How to Run
```bash
# 1. Quick test run (2 turns)
python run_generator.py --test

# 2. Standard run (4 turns)
python run_generator.py

# 3. Full broadcast run (16 turns)
python run_generator.py --full

# 4. Publish to Facebook Page
python publish_facebook.py output/run_XXXX/podcast_lounge_final.mp4 output/run_XXXX/metadata.json
```

## 📱 Recommended Facebook Page Target
- **Page Concept**: *Slow English Lounge / English Fluency Studio*
- **Target Audience**: ESL students, adult learners, commute/relaxation listeners looking for natural listening immersion.
