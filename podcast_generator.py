"""
Slow English Podcast Lounge - Video Generator
Generates conversational slow English listening videos with dual hosts (Emma & Andrew).
Features:
- Dual Edge TTS Neural voices (en-US-AvaNeural & en-US-AndrewNeural)
- Automated animated audio equalizer
- High-contrast typography with yellow keyword highlighting
- Progress bar and time stamps
- AI script generation via Pollinations API (gemini-fast) with reliable fallbacks
"""
import os, sys, json, math, subprocess, random, requests, re, asyncio
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from dotenv import load_dotenv
import edge_tts

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
MUTED_WHITE = (220, 225, 235)
DARK_BG = (12, 16, 26)
DARK_BAR = (22, 28, 44)
GOLD_ACCENT = (255, 193, 7)
CHANNEL_NAME = "SLOW ENGLISH LOUNGE"

EMMA_VOICE = "en-US-AvaNeural"
ANDREW_VOICE = "en-US-AndrewNeural"
VOICE_RATE = "-15%"

TOPICS = [
    {"topic": "How to Think Directly in English Without Translating", "keyword": "THINK", "sub": "STOP TRANSLATING IN YOUR HEAD"},
    {"topic": "Building Confidence to Speak English Everyday", "keyword": "CONFIDENCE", "sub": "SPEAK WITHOUT FEAR"},
    {"topic": "The Power of Daily English Listening Habits", "keyword": "HABITS", "sub": "IMPROVE YOUR LISTENING FAST"},
    {"topic": "Overcoming the Fear of Making Mistakes in English", "keyword": "MISTAKES", "sub": "LEARN FROM EVERY MISTAKE"},
    {"topic": "How to Learn English Vocabulary Naturally", "keyword": "VOCABULARY", "sub": "REMEMBER WORDS EASILY"},
    {"topic": "Small Talk and Everyday English Conversations", "keyword": "CONVERSATIONS", "sub": "SPEAK NATURALLY IN ANY SITUATION"},
    {"topic": "Mastering American Accent Pronunciation and Rhythm", "keyword": "PRONUNCIATION", "sub": "SOUND MORE NATURAL"},
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
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
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

def generate_script_ai(topic_item, target_turns=6):
    topic_str = topic_item["topic"]
    prompt = f"""Write {target_turns} turns of a natural, slow, friendly English learning podcast dialogue between Emma and Andrew.
Topic: {topic_str}

RULES:
- Exactly {target_turns} dialogue turns alternating between Host1 (Emma) and Host2 (Andrew)
- Each turn MUST be 2-3 short, clear sentences (18-28 words)
- Wrap exactly 1 key learning word or phrase per turn in **asterisks**
- Return as clean JSON array only:
[{{"speaker":"Host1","text":"Welcome to the podcast! Today we will learn how to **think** directly in English."}},
 {{"speaker":"Host2","text":"That is right Emma. Translating in your head slows down your speech, but you can build this **skill** daily."}}]"""

    key = os.getenv("POLLINATIONS_API_KEY")
    if key:
        try:
            resp = requests.post("https://gen.pollinations.ai/v1/chat/completions", json={
                "model": "gemini-fast",
                "messages": [
                    {"role": "system", "content": "You are an expert English teacher. Output clean JSON array of podcast turns."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8
            }, headers={"Authorization": f"Bearer {key}"}, timeout=60)
            if resp.status_code == 200:
                raw = resp.json()["choices"][0]["message"]["content"].strip()
                if "```json" in raw:
                    raw = raw.split("```json")[1].split("```")[0].strip()
                elif "```" in raw:
                    raw = raw.split("```")[1].split("```")[0].strip()
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
            print(f"[script] Pollinations AI note: {e}, falling back to curated script.")

    # High quality fallback
    return [
        {"speaker": "Host1", "text": f"Welcome back to the Slow English Lounge! Today we are discussing how to **master** {topic_str}."},
        {"speaker": "Host2", "text": f"I am so excited for this topic. The biggest secret is to practice with **patience** every single day."},
        {"speaker": "Host1", "text": f"Exactly Andrew. When you listen to clear English repeatedly, your brain absorbs the natural **rhythm** effortlessly."},
        {"speaker": "Host2", "text": f"So relax, listen carefully, and repeat the phrases out loud to build your speaking **confidence**!"}
    ][:target_turns]

async def generate_audio_files(turns, run_dir):
    audio_dir = run_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    audio_list = []

    for i, turn in enumerate(turns):
        mp3_path = audio_dir / f"turn_{i:03d}.mp3"
        spoken = re.sub(r'\*\*(.*?)\*\*', r'\1', turn["text"])
        voice = EMMA_VOICE if turn["speaker"] == "Host1" else ANDREW_VOICE
        comm = edge_tts.Communicate(spoken, voice, rate=VOICE_RATE)
        await comm.save(str(mp3_path))

        # Probe duration
        try:
            r = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(mp3_path)],
                capture_output=True, text=True, check=True
            )
            duration = float(r.stdout.strip())
        except:
            duration = 5.0

        audio_list.append({"path": str(mp3_path), "duration": duration, "speaker": turn["speaker"]})
    return audio_list

def draw_equalizer_waves(draw, start_x, start_y, frame_idx=0):
    num_bars = 8
    bar_w = 5
    gap = 6
    for i in range(num_bars):
        h = int(16 + 14 * abs(math.sin(frame_idx * 0.5 + i * 1.2)))
        x = start_x + i * (bar_w + gap)
        y_top = start_y - h // 2
        y_bot = start_y + h // 2
        draw.rounded_rectangle([(x, y_top), (x + bar_w, y_bot)], radius=2, fill=YELLOW)

def render_podcast_frame(turn, idx, total_turns, elapsed, total_dur, out_path):
    woman_path = ASSETS_DIR / "woman_base.png"
    if woman_path.exists():
        canvas = Image.open(woman_path).convert("RGBA").resize((VIDEO_WIDTH, VIDEO_HEIGHT), Image.Resampling.LANCZOS)
    else:
        canvas = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), DARK_BG)
        # Gradient effect
        gdraw = ImageDraw.Draw(canvas)
        for y in range(VIDEO_HEIGHT):
            shade = int(14 + (y / VIDEO_HEIGHT) * 20)
            gdraw.line([(0, y), (VIDEO_WIDTH, y)], fill=(shade, shade + 4, shade + 14, 255))

    draw = ImageDraw.Draw(canvas)

    # Top Left Channel Tab
    font_tab = load_font(30, bold=True)
    draw.rounded_rectangle([(60, 40), (560, 110)], radius=18, fill=DARK_BAR, outline=YELLOW, width=3)
    draw_equalizer_waves(draw, 90, 75, frame_idx=idx)
    draw.text((190, 75), CHANNEL_NAME, fill=WHITE, font=font_tab, anchor="lm")

    # Top Right Host Badge
    speaker_name = "EMMA" if turn["speaker"] == "Host1" else "ANDREW"
    font_spk = load_font(28, bold=True)
    draw.rounded_rectangle([(1520, 40), (1860, 110)], radius=18, fill=DARK_BAR, outline=YELLOW, width=3)
    draw.text((1690, 75), f"🎙️ HOST: {speaker_name}", fill=YELLOW, font=font_spk, anchor="mm")

    # Center Text Rendering
    text = turn["text"]
    parts = re.split(r'(\*\*.*?\*\*)', text)
    words_list = []
    for p in parts:
        if p.startswith('**') and p.endswith('**'):
            words_list.append((p[2:-2], True))
        elif p:
            for w in p.split(' '):
                if w: words_list.append((w, False))

    text_left = 780
    text_right = 1820
    max_w = text_right - text_left
    center_x = (text_left + text_right) // 2

    font_size = 85
    lines = None
    while font_size >= 45:
        curr_font = load_font(font_size, bold=True)
        curr_lines = []
        curr_line = []
        curr_w = 0
        for word, is_y in words_list:
            wb = draw.textbbox((0, 0), word, font=curr_font)
            wl = wb[2] - wb[0] + 12
            if curr_w + wl > max_w and curr_line:
                curr_lines.append((curr_line, curr_w))
                curr_line = [(word, is_y, wl)]
                curr_w = wl
            else:
                curr_line.append((word, is_y, wl))
                curr_w += wl
        if curr_line:
            curr_lines.append((curr_line, curr_w))
        if len(curr_lines) <= 3 and all(w <= max_w for _, w in curr_lines):
            lines = curr_lines
            main_font = curr_font
            break
        font_size -= 5

    if lines is None:
        main_font = load_font(45, bold=True)
        lines = curr_lines

    line_h = int(font_size * 1.35)
    total_h = len(lines) * line_h
    start_y = 520 - total_h // 2

    # Draw blurred shadow
    shadow_img = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_img)
    for l_idx, (line_words, line_w) in enumerate(lines):
        cx = center_x - line_w // 2
        cy = start_y + l_idx * line_h
        for word, _, wl in line_words:
            sdraw.text((cx + 4, cy + 4), word, fill=(0, 0, 0, 220), font=main_font)
            cx += wl
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(5))
    canvas.paste(shadow_img, (0, 0), shadow_img)

    # Draw text
    draw = ImageDraw.Draw(canvas)
    for l_idx, (line_words, line_w) in enumerate(lines):
        cx = center_x - line_w // 2
        cy = start_y + l_idx * line_h
        for word, is_y, wl in line_words:
            color = YELLOW if is_y else WHITE
            draw.text((cx, cy), word, fill=color, font=main_font)
            cx += wl

    # Bottom Progress Bar
    draw.line([(0, 1020), (VIDEO_WIDTH, 1020)], fill=(35, 45, 65), width=3)
    ratio = min(1.0, elapsed / max(1.0, total_dur))
    draw.line([(0, 1020), (int(VIDEO_WIDTH * ratio), 1020)], fill=YELLOW, width=6)

    font_sub = load_font(26, bold=False)
    draw.text((70, 1050), "Learn English • Think Naturally • Speak With Confidence", fill=MUTED_WHITE, font=font_sub, anchor="lm")
    time_str = f"{int(elapsed // 60):02d}:{int(elapsed % 60):02d} / {int(total_dur // 60):02d}:{int(total_dur % 60):02d}"
    draw.text((1850, 1050), time_str, fill=YELLOW, font=font_sub, anchor="rm")

    canvas.convert("RGB").save(out_path, quality=92)

def assemble_video(turns, audio_list, run_dir):
    frames_dir = run_dir / "frames"
    clips_dir = run_dir / "clips"
    frames_dir.mkdir(parents=True, exist_ok=True)
    clips_dir.mkdir(parents=True, exist_ok=True)

    total_dur = sum(a["duration"] for a in audio_list)
    elapsed = 0.0
    clips = []

    for i, (turn, audio) in enumerate(zip(turns, audio_list)):
        img_p = frames_dir / f"frame_{i:03d}.png"
        clip_p = clips_dir / f"clip_{i:03d}.mp4"

        render_podcast_frame(turn, i, len(turns), elapsed, total_dur, str(img_p))

        dur_str = f"{audio['duration']:.3f}"
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", str(img_p), "-i", audio["path"],
            "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT},fps={FPS}",
            "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p", "-preset", "fast", "-t", dur_str, str(clip_p)
        ], check=True, capture_output=True)

        clips.append(clip_p)
        elapsed += audio["duration"]

    concat_txt = run_dir / "concat.txt"
    with open(concat_txt, "w") as f:
        for c in clips:
            f.write(f"file '{c.resolve().as_posix()}'\n")

    final_video = run_dir / "podcast_lounge_final.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(final_video)], check=True, capture_output=True)
    return final_video, total_dur

async def run_podcast_generation(topic_idx=0, turns_count=4):
    topic_item = TOPICS[topic_idx % len(TOPICS)]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = OUTPUT_DIR / f"run_{ts}"
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"[Podcast Lounge] Generating: '{topic_item['topic']}' ({turns_count} turns)...")
    turns = generate_script_ai(topic_item, target_turns=turns_count)
    audio_list = await generate_audio_files(turns, run_dir)
    video_p, dur = assemble_video(turns, audio_list, run_dir)

    meta = {
        "title": f"Slow English Podcast: {topic_item['topic']} | Easy Listening Practice",
        "description": f"Improve your English fluency and listening comprehension with our slow conversational podcast on '{topic_item['topic']}'. Follow for daily lessons! 🎙️📚",
        "topic": topic_item["topic"],
        "duration_seconds": dur,
        "turns": len(turns)
    }
    with open(run_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"[Podcast Lounge] Complete! Video saved to: {video_p}")
    return video_p, meta
