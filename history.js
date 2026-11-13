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
  },
  {
    "episode": 17,
    "topic": "The Gentle Art of 'Slow Listening': Tuning into the World Around You",
    "date": "2026-10-30T07:08:10.104581",
    "duration_sec": 1307.73,
    "duration_min": 21.8,
    "video_file": "podcast_ep17_20261030_065600.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 18,
    "topic": "The Gentle Art of 'Slow Noticing': Cultivating Deeper Awareness in English",
    "date": "2026-10-31T07:01:13.792830",
    "duration_sec": 1145.76,
    "duration_min": 19.1,
    "video_file": "podcast_ep18_20261031_065014.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 19,
    "topic": "The Gentle Art of 'Slow Reflection': Unpacking Your Day with Calm",
    "date": "2026-11-01T07:32:18.490006",
    "duration_sec": 1161.98,
    "duration_min": 19.37,
    "video_file": "podcast_ep19_20261101_071555.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 20,
    "topic": "The Gentle Art of 'Slow Dreaming': Cultivating Restful Inner Worlds",
    "date": "2026-11-02T07:48:05.827036",
    "duration_sec": 1214.83,
    "duration_min": 20.25,
    "video_file": "podcast_ep20_20261102_073055.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 21,
    "topic": "The Gentle Art of 'Slow Sketching': Capturing Moments with Calm Observation",
    "date": "2026-11-03T08:02:19.959907",
    "duration_sec": 1255.39,
    "duration_min": 20.92,
    "video_file": "podcast_ep21_20261103_074508.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 22,
    "topic": "The Gentle Art of 'Slow Appreciating': Finding English Joy in Simple Pleasures",
    "date": "2026-11-04T07:41:45.450146",
    "duration_sec": 1231.17,
    "duration_min": 20.52,
    "video_file": "podcast_ep22_20261104_072412.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 23,
    "topic": "The Gentle Art of 'Slow Questioning': Unlocking Deeper Understanding and Connection",
    "date": "2026-11-05T08:03:05.689870",
    "duration_sec": 1231.51,
    "duration_min": 20.53,
    "video_file": "podcast_ep23_20261105_074931.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 24,
    "topic": "The Gentle Art of 'Slow Exploring': Discovering New English Words with Ease",
    "date": "2026-11-06T08:06:18.376382",
    "duration_sec": 1209.26,
    "duration_min": 20.15,
    "video_file": "podcast_ep24_20261106_074945.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 25,
    "topic": "The Gentle Art of 'Slow Translation': Bridging Worlds with Thoughtful Language",
    "date": "2026-11-07T07:12:46.856957",
    "duration_sec": 1272.38,
    "duration_min": 21.21,
    "video_file": "podcast_ep25_20261107_065724.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 26,
    "topic": "The Gentle Art of 'Slow Understanding': Unpacking Nuance in English Conversation",
    "date": "2026-11-08T07:15:46.958730",
    "duration_sec": 1218.58,
    "duration_min": 20.31,
    "video_file": "podcast_ep26_20261108_070447.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 27,
    "topic": "The Gentle Art of 'Slow Journaling': Unlocking Your Inner English Voice",
    "date": "2026-11-09T07:59:42.524064",
    "duration_sec": 1147.97,
    "duration_min": 19.13,
    "video_file": "podcast_ep27_20261109_074825.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 28,
    "topic": "The Gentle Art of 'Slow Storytelling': Weaving Calm Narratives in English",
    "date": "2026-11-10T08:32:14.689477",
    "duration_sec": 1276.46,
    "duration_min": 21.27,
    "video_file": "podcast_ep28_20261110_081355.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 29,
    "topic": "How to Stop Translating in Your Head",
    "date": "2026-11-11T07:53:24.811458",
    "duration_sec": 1233.12,
    "duration_min": 20.55,
    "video_file": "podcast_ep29_20261111_073904.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 30,
    "topic": "The Gentle Art of 'Slow Observing': Seeing English Details Unfold",
    "date": "2026-11-12T08:25:31.068472",
    "duration_sec": 1283.71,
    "duration_min": 21.4,
    "video_file": "podcast_ep30_20261112_080720.mp4",
    "platform": "Facebook"
  },
  {
    "episode": 31,
    "topic": "Finding Solace in Solitude",
    "date": "2026-11-13T07:59:58.802279",
    "duration_sec": 1169.4,
    "duration_min": 19.49,
    "video_file": "podcast_ep31_20261113_074331.mp4",
    "platform": "Facebook"
  }
];
if (typeof module !== 'undefined' && module.exports) { module.exports = PODCAST_HISTORY; }
if (typeof window !== 'undefined') { window.PODCAST_HISTORY = PODCAST_HISTORY; }
