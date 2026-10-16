import os, sys
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMP_DIR = os.path.join(BASE_DIR, "temp")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

for d in [INPUT_DIR, OUTPUT_DIR, TEMP_DIR, ASSETS_DIR]:
    os.makedirs(d, exist_ok=True)

CHANNEL_NAME = "SOLACE ENGLISH LOUNGE"
TAGLINE = "Calm, Slow & Natural English Listening"
DEFAULT_IMAGE_PATH = os.path.join(ASSETS_DIR, "host_studio.png")
LOGO_PATH = os.path.join(ASSETS_DIR, "solace_logo.png")

VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
VIDEO_FPS = 30

IS_SOLO = True

SUBTITLE_CENTER_X = 1380
SUBTITLE_Y = 320
MAX_SUBTITLE_WIDTH = 750
SUBTITLE_FONT_SIZE = 44

VIS_CENTER_X = 1380
VIS_BASE_Y = 580
VIS_NUM_BARS = 16
VIS_BAR_WIDTH = 12
VIS_BAR_SPACING = 12
VIS_MIN_HEIGHT = 4
VIS_MAX_HEIGHT = 56
VIS_COLOR = (255, 215, 0, 240)  # Radiant Gold

VOICE_HOST1 = "en-US-AvaNeural"
VOICE_HOST2 = "en-US-AvaNeural"
HOST1_NAME = "Emma"
HOST2_NAME = "Emma"
HOST1_SPEAKER = "female"
HOST2_SPEAKER = "female"
HOST1_PITCH = "+0Hz"
HOST2_PITCH = "+0Hz"
TTS_RATE = "-15%"
PAUSE_BETWEEN_TURNS = 0.50

MAX_WORDS_PER_LINE = 4
MAX_CHARS_PER_LINE = 32

POLLINATIONS_API_KEY = os.environ.get("POLLINATIONS_API_KEY", "")
POLLINATIONS_ENDPOINT = "https://gen.pollinations.ai/v1/chat/completions"
POLLINATIONS_MODEL = "gemini-fast"
NICHE_PROMPT = "slow, reflective, peaceful English solo host podcast speaking gently and soothingly directly to the listener about daily mindfulness, unhurried listening, and calm thinking"

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\segoeuib.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
FONT_PATH = next((p for p in FONT_CANDIDATES if os.path.exists(p)), "arial.ttf")
FALLBACK_FONT_PATH = FONT_PATH
