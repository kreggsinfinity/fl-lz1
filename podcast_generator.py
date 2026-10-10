"""
SLOW ENGLISH PODCAST LOUNGE - 16:9 FULL HD (1920x1080)
UI Style: Classic Warm Acoustic Studio Lounge
- Host & broadcast mic on left (woman_base.png)
- Active pulsing sound equalizer reacting to spoken turns
- Single-line modern glass subtitles with glowing yellow keyword highlight
"""
import os, sys, json, math, subprocess, random, requests, re, asyncio
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from dotenv import load_dotenv
import edge_tts

if sys.platform == 'win32':
    try: sys.stdout.reconfigure(encoding='utf-8')
    except Exception: pass

load_dotenv()

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
FPS = 30

YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
MUTED_WHITE = (210, 215, 230)
DARK_BG = (12, 16, 26)
DARK_BAR = (20, 26, 42)
CHANNEL_NAME = "SLOW ENGLISH LOUNGE"

EMMA_VOICE = "en-US-AvaNeural"
ANDREW_VOICE = "en-US-AndrewNeural"
VOICE_RATE = "-15%"

TOPICS = [
    {"topic": "How to Think Directly in English Without Translating", "keyword": "THINK", "sub": "STOP TRANSLATING IN YOUR HEAD"},
    {"topic": "Building Confidence to Speak English Everyday", "keyword": "CONFIDENCE", "sub": "SPEAK WITHOUT FEAR"},
    {"topic": "The Power of Daily English Listening Habits", "keyword": "HABITS", "sub": "IMPROVE YOUR LISTENING FAST"},
    {"topic": "The Secret to Fluency: Consistency Over Perfection", "keyword": "FLUENCY", "sub": "THE PATH TO REAL FLUENCY"}
]

def load_font(size, bold=True):
    fonts_to_try = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/trebucbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in fonts_to_try:
        if Path(p).exists():
            try: return ImageFont.truetype(p, size)
            except: continue
    return ImageFont.load_default()

def clean_text(text):
    text = re.sub(r'\b(mm+|um+|uh+|ah+)\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def generate_script_ai(topic_item, target_turns=4):
    prompt = f"""Write {target_turns} turns of a natural, slow, friendly English learning podcast dialogue between Emma and Andrew.
Topic: {topic_item['topic']}
RULES:
- Dialogue alternating between Host1 (Emma) and Host2 (Andrew)
- Each turn MUST be 1-2 concise, clear sentences (14-22 words) so it fits in a clean single-line subtitle
- Wrap exactly 1 key learning word per turn in **asterisks**
- Return as clean JSON array only:
[{{"speaker":"Host1","text":"Welcome to the podcast! Today we will learn how to **think** directly in English."}},
 {{"speaker":"Host2","text":"Translating in your head slows you down, but you can build this **skill** daily."}}]"""

    key = os.getenv("POLLINATIONS_API_KEY")
    if key:
        try:
            resp = requests.post("https://gen.pollinations.ai/v1/chat/completions", json={
                "model": "gemini-fast",
                "messages": [
                    {"role": "system", "content": "Output clean JSON array of podcast turns with 1 **keyword** per turn."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8
            }, headers={"Authorization": f"Bearer {key}"}, timeout=60)
            if resp.status_code == 200:
                raw = resp.json()["choices"][0]["message"]["content"].strip()
                if "```json" in raw: raw = raw.split("```json")[1].split("```")[0].strip()
                elif "```" in raw: raw = raw.split("```")[1].split("```")[0].strip()
                script = json.loads(raw)
                if isinstance(script, list) and len(script) > 0:
                    for i, turn in enumerate(script):
                        turn["speaker"] = "Host1" if i % 2 == 0 else "Host2"
                        turn["text"] = clean_text(turn["text"])
                        if "**" not in turn["text"]:
                            words = turn["text"].split()
                            if len(words) > 2:
                                idx = len(words) // 2
                                words[idx] = f"**{words[idx]}**"
                                turn["text"] = " ".join(words)
                    return script[:target_turns]
        except Exception as e:
            pass

    return [
        {"speaker": "Host1", "text": f"Welcome back! Today we are discussing how to **think** directly in English."},
        {"speaker": "Host2", "text": f"The biggest secret is practicing daily with **patience** and clear listening."},
        {"speaker": "Host1", "text": f"When you listen repeatedly, your brain absorbs the natural **rhythm** effortlessly."},
        {"speaker": "Host2", "text": f"So relax, repeat the words out loud, and build your speaking **confidence**!"}
    ][:target_turns]

async def generate_audio_files(turns, run_dir):
    audio_dir = run_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    audio_list = []
    for i, turn in enumerate(turns):
        mp3_p = audio_dir / f"turn_{i:03d}.mp3"
        spoken = re.sub(r'\*\*(.*?)\*\*', r'\1', turn["text"])
        voice = EMMA_VOICE if turn["speaker"] == "Host1" else ANDREW_VOICE
        comm = edge_tts.Communicate(spoken, voice, rate=VOICE_RATE)
        await comm.save(str(mp3_p))

        try:
            r = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(mp3_p)],
                capture_output=True, text=True, check=True
            )
            duration = float(r.stdout.strip())
        except:
            duration = 5.0
        audio_list.append({"path": str(mp3_p), "duration": duration, "speaker": turn["speaker"]})
    return audio_list

def draw_animated_sound_equalizer(draw, center_x, center_y, frame_phase=0):
    """Prominent animated 16-bar sound spectrum visualizer showing voice activity"""
    num_bars = 16
    bar_w = 6
    gap = 8
    total_w = num_bars * bar_w + (num_bars - 1) * gap
    start_x = center_x - total_w // 2

    for i in range(num_bars):
        # Organic wave height reacting to voice phase
        h = int(14 + 48 * abs(math.sin(frame_phase * 0.7 + i * 0.55)))
        x = start_x + i * (bar_w + gap)
        y_top = center_y - h // 2
        y_bot = center_y + h // 2
        # Color gradient: Gold core with bright tip
        col = (255, 230, 80) if i in [7, 8, 9] else YELLOW
        draw.rounded_rectangle([(x, y_top), (x + bar_w, y_bot)], radius=3, fill=col)

def render_frame_ui1(topic_item, turn, frame_phase, elapsed, total_dur, out_path):
    woman_path = ASSETS_DIR / "woman_base.png"
    if woman_path.exists():
        canvas = Image.open(woman_path).convert("RGBA").resize((VIDEO_WIDTH, VIDEO_HEIGHT), Image.Resampling.LANCZOS)
    else:
        canvas = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), DARK_BG)

    draw = ImageDraw.Draw(canvas)

    # 1. Top Left Channel Badge with Equalizer Bars
    font_tab = load_font(30, bold=True)
    draw.rounded_rectangle([(60, 40), (580, 110)], radius=18, fill=DARK_BAR, outline=YELLOW, width=3)
    # Mini equalizer in badge
    for b in range(6):
        bh = int(12 + 18 * abs(math.sin(frame_phase * 0.8 + b * 0.7)))
        draw.rounded_rectangle([(95 + b * 11, 75 - bh//2), (101 + b * 11, 75 + bh//2)], radius=2, fill=YELLOW)
    draw.text((180, 75), CHANNEL_NAME, fill=WHITE, font=font_tab, anchor="lm")

    # 2. Top Right Speaker Pill
    speaker_name = "EMMA" if turn["speaker"] == "Host1" else "ANDREW"
    font_spk = load_font(28, bold=True)
    draw.rounded_rectangle([(1520, 40), (1860, 110)], radius=18, fill=DARK_BAR, outline=YELLOW, width=3)
    draw.text((1690, 75), f"🎙️ HOST: {speaker_name}", fill=YELLOW, font=font_spk, anchor="mm")

    # 3. PROMINENT SOUND EQUALIZER CONSOLE (Active voice indicator)
    eq_center_x = 1300
    eq_center_y = 420
    draw.rounded_rectangle([(eq_center_x - 170, eq_center_y - 45), (eq_center_x + 170, eq_center_y + 45)], radius=16, fill=(18, 24, 40), outline=YELLOW, width=2)
    draw_animated_sound_equalizer(draw, eq_center_x, eq_center_y, frame_phase=frame_phase)

    # Voice Active Label
    font_active = load_font(20, bold=True)
    draw.text((eq_center_x, eq_center_y + 65), f"● LIVE VOICE AUDIO ({speaker_name})", fill=YELLOW, font=font_active, anchor="mm")

    # 4. SLEEK SINGLE-LINE SUBTITLE DISPLAY (Center-Bottom container)
    text = turn["text"]
    parts = re.split(r'(\*\*.*?\*\*)', text)
    words_list = []
    for p in parts:
        if p.startswith('**') and p.endswith('**'):
            words_list.append((p[2:-2], True))
        elif p:
            for w in p.split(' '):
                if w: words_list.append((w, False))

    sub_font = load_font(56, bold=True)
    # Calculate single-line width
    word_widths = []
    for w, is_y in words_list:
        bb = draw.textbbox((0, 0), w, font=sub_font)
        word_widths.append((w, is_y, bb[2] - bb[0] + 14))

    total_sub_w = sum(ww[2] for ww in word_widths)
    sub_center_x = 1300
    sub_y = 660

    # Draw modern frosted glass container for single line
    card_left = max(720, sub_center_x - total_sub_w // 2 - 40)
    card_right = min(1860, sub_center_x + total_sub_w // 2 + 40)
    card_top = sub_y - 50
    card_bot = sub_y + 50
    draw.rounded_rectangle([(card_left, card_top), (card_right, card_bot)], radius=25, fill=(15, 20, 35), outline=(60, 75, 115), width=2)

    # Render single-line text with glowing keyword
    cur_x = (card_left + card_right) // 2 - total_sub_w // 2
    for word, is_yellow, ww in word_widths:
        if is_yellow:
            # Subtle glow around keyword
            draw.text((cur_x, sub_y), word, fill=YELLOW, font=sub_font, anchor="lm")
        else:
            draw.text((cur_x, sub_y), word, fill=WHITE, font=sub_font, anchor="lm")
        cur_x += ww

    # 5. Bottom Progress Bar & Time
    draw.line([(0, 1020), (VIDEO_WIDTH, 1020)], fill=(30, 40, 60), width=3)
    ratio = min(1.0, elapsed / max(1.0, total_dur))
    draw.line([(0, 1020), (int(VIDEO_WIDTH * ratio), 1020)], fill=YELLOW, width=6)

    font_sub = load_font(26, bold=False)
    draw.text((70, 1050), "Classic Acoustic Studio • Slow English Lounge", fill=MUTED_WHITE, font=font_sub, anchor="lm")
    time_str = f"{int(elapsed // 60):02d}:{int(elapsed % 60):02d} / {int(total_dur // 60):02d}:{int(total_dur % 60):02d}"
    draw.text((1850, 1050), time_str, fill=YELLOW, font=font_sub, anchor="rm")

    canvas.convert("RGB").save(out_path, quality=92)

def assemble_video_ui1(topic_item, turns, audio_list, run_dir):
    frames_dir = run_dir / "frames"
    clips_dir = run_dir / "clips"
    frames_dir.mkdir(parents=True, exist_ok=True)
    clips_dir.mkdir(parents=True, exist_ok=True)

    total_dur = sum(a["duration"] for a in audio_list)
    elapsed = 0.0
    clips = []

    for i, (turn, audio) in enumerate(zip(turns, audio_list)):
        dur = audio["duration"]
        clip_p = clips_dir / f"clip_{i:03d}.mp4"

        # Render 6 animated frames for active equalizer movement
        turn_frames = []
        num_subframes = max(4, int(dur * 2))  # 2 frames per sec
        for f_idx in range(num_subframes):
            frame_p = frames_dir / f"frame_{i:03d}_{f_idx:02d}.png"
            render_frame_ui1(topic_item, turn, frame_phase=f_idx, elapsed=elapsed, total_dur=total_dur, out_path=str(frame_p))
            turn_frames.append(frame_p)

        # Encode animated subclip with audio
        subprocess.run([
            "ffmpeg", "-y", "-framerate", "2", "-i", str(frames_dir / f"frame_{i:03d}_%02d.png"),
            "-i", audio["path"], "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p", "-preset", "fast", "-t", f"{dur:.3f}", str(clip_p)
        ], check=True, capture_output=True)

        clips.append(clip_p)
        elapsed += dur

    concat_txt = run_dir / "concat.txt"
    with open(concat_txt, "w") as f:
        for c in clips: f.write(f"file '{c.resolve().as_posix()}'\n")

    final_video = run_dir / "podcast_lounge_final.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(final_video)], check=True, capture_output=True)
    return final_video, total_dur

async def run_podcast_generation(topic_idx=0, turns_count=4):
    topic_item = TOPICS[topic_idx % len(TOPICS)]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = OUTPUT_DIR / f"run_{ts}"
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"[Podcast Lounge] Generating 16:9 Classic Acoustic Studio: '{topic_item['topic']}'...")
    turns = generate_script_ai(topic_item, target_turns=turns_count)
    audio_list = await generate_audio_files(turns, run_dir)
    video_p, dur = assemble_video_ui1(topic_item, turns, audio_list, run_dir)

    meta = {
        "title": f"Slow English Podcast: {topic_item['topic']} | Classic Studio",
        "description": f"Improve your English fluency and listening skills in our classic studio lounge podcast with Emma & Andrew! 🎙️🌟",
        "duration_seconds": dur
    }
    with open(run_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    return video_p, meta
