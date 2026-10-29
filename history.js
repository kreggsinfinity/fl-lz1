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
  },
  {
    "episode": 3,
    "topic": "Savoring Small Moments: The Gentle Power of Noticing",
    "date": "2026-10-16T05:55:51.126058",
    "duration_sec": 1205.57,
    "duration_min": 20.09,
    "video_file": "podcast_ep3_20261016_054126.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 4,
    "topic": "Whispers of Calm: Listening to Your Inner Landscape",
    "date": "2026-10-17T05:44:00.302434",
    "duration_sec": 1194.48,
    "duration_min": 19.91,
    "video_file": "podcast_ep4_20261017_052652.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 5,
    "topic": "The Gentle Art of Letting Go: Finding Peace in Imperfection",
    "date": "2026-10-18T05:52:57.969825",
    "duration_sec": 1217.88,
    "duration_min": 20.3,
    "video_file": "podcast_ep5_20261018_053805.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 6,
    "topic": "The Gentle Rhythm of Rest: Finding Stillness in Busy Lives",
    "date": "2026-10-19T06:12:36.043584",
    "duration_sec": 1226.33,
    "duration_min": 20.44,
    "video_file": "podcast_ep6_20261019_055600.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 7,
    "topic": "The Gentle Architecture of Thought: Building Calm Mental Spaces",
    "date": "2026-10-20T06:02:48.221454",
    "duration_sec": 1207.94,
    "duration_min": 20.13,
    "video_file": "podcast_ep7_20261020_054839.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 8,
    "topic": "The Quiet Language of Your Breath: A Pathway to Present Moment Awareness",
    "date": "2026-10-21T06:04:59.563680",
    "duration_sec": 1112.97,
    "duration_min": 18.55,
    "video_file": "podcast_ep8_20261021_055121.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 9,
    "topic": "The Gentle Practice of Mindful Wandering: Exploring Inner Worlds with Ease",
    "date": "2026-10-22T06:12:44.286383",
    "duration_sec": 1203.0,
    "duration_min": 20.05,
    "video_file": "podcast_ep9_20261022_055509.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 10,
    "topic": "The Gentle Echo: Listening to Your Own Wisdom",
    "date": "2026-10-23T06:34:28.207653",
    "duration_sec": 1258.22,
    "duration_min": 20.97,
    "video_file": "podcast_ep10_20261023_061754.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 11,
    "topic": "The Gentle Art of Pausing: Finding Clarity in the Space Between Thoughts",
    "date": "2026-10-24T06:00:46.528830",
    "duration_sec": 1300.56,
    "duration_min": 21.68,
    "video_file": "podcast_ep11_20261024_053613.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 12,
    "topic": "The Gentle Flow of Words: Cultivating Mindful Expression",
    "date": "2026-10-25T06:07:48.724675",
    "duration_sec": 1244.23,
    "duration_min": 20.74,
    "video_file": "podcast_ep12_20261025_055105.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 13,
    "topic": "The Gentle Embrace of Solitude: Finding Joy in Your Own Company",
    "date": "2026-10-26T06:28:42.151868",
    "duration_sec": 1196.9,
    "duration_min": 19.95,
    "video_file": "podcast_ep13_20261026_060841.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 14,
    "topic": "The Gentle Practice of 'Slow Seeing': Discovering Beauty in the Ordinary",
    "date": "2026-10-27T06:28:48.686517",
    "duration_sec": 1342.46,
    "duration_min": 22.37,
    "video_file": "podcast_ep14_20261027_060706.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 15,
    "topic": "The Gentle Art of 'Slow Reading': Unlocking Deeper Meaning and Calm",
    "date": "2026-10-28T07:07:51.502510",
    "duration_sec": 1171.73,
    "duration_min": 19.53,
    "video_file": "podcast_ep15_20261028_064522.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 16,
    "topic": "The Gentle Art of 'Slow Speaking': Finding Your Calm Voice in Conversation",
    "date": "2026-10-29T07:10:33.118396",
    "duration_sec": 1203.45,
    "duration_min": 20.06,
    "video_file": "podcast_ep16_20261029_065245.mp4",
    "platform": "Facebook"
  }
];
if (typeof module !== 'undefined' && module.exports) { module.exports = PODCAST_HISTORY; }
if (typeof window !== 'undefined') { window.PODCAST_HISTORY = PODCAST_HISTORY; }
