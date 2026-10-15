// Daily Video History Log & Topic Registry
const PODCAST_HISTORY = [
  {
    "episode": 1,
    "topic": "The Art of Unhurried Mornings",
    "date": "2026-10-15T08:09:53.953606",
    "duration_sec": 75.28,
    "duration_min": 1.25,
    "video_file": "podcast_ep1_20261015_080823.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 2,
    "topic": "Finding Quiet in the Everyday: Cultivating Inner Peace",
    "date": "2026-10-15T08:49:32.789771",
    "duration_sec": 1121.69,
    "duration_min": 18.69,
    "video_file": "podcast_ep2_20261015_083217.mp4",
    "platform": "Facebook"
  }
];
if (typeof module !== 'undefined' && module.exports) { module.exports = PODCAST_HISTORY; }
if (typeof window !== 'undefined') { window.PODCAST_HISTORY = PODCAST_HISTORY; }
