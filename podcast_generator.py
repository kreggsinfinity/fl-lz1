"""
SLOW ENGLISH FLUENCY PODCAST LOUNGE - 16:9 FULL HD (1920x1080)
Format: 1920x1080 Landscape Studio Broadcast
Features:
- Photorealistic studio host setting on the left (Shure SM7B, luxury acoustic wood lounge)
- Dynamic auto-sized top pills (Channel wave indicator + Host live badge, NO text overflow)
- Bite-sized phrase & sentence subtitles with word-by-word active karaoke highlighting
- Zero clipping, zero box overflow, zero emoji/tofu glitches
- Clean podcast audio indicator and real-time progress timeline (NO club music visualizer)
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

# Colors
GOLD_ACCENT = (255, 215, 0)       # Radiant Gold (#FFD700)
WHITE = (255, 255, 255)
MUTED_GOLD = (230, 215, 175)
MUTED_WHITE = (220, 225, 235)
DARK_BAR = (16, 18, 28, 230)
LIVE_GREEN = (34, 197, 94)

CHANNEL_NAME = "SLOW ENGLISH LOUNGE"
TAGLINE = "Learn English  •  Think Better  •  Speak Confidently"

EMMA_VOICE = "en-US-AvaNeural"
ANDREW_VOICE = "en-US-AndrewNeural"
VOICE_RATE = "-15%"

TOPICS = [
    {
        "topic": "How to Think Directly in English Without Translating",
        "keyword": "THINK",
        "sub": "STOP TRANSLATING IN YOUR HEAD",
        "turns": [
            {"speaker": "Host1", "text": "Welcome back everyone. Today we are exploring why thinking directly in English is the **secret** to real fluency."},
            {"speaker": "Host2", "text": "That is so true. When you translate words in your head first, you naturally hesitate and lose your **confidence**."},
            {"speaker": "Host1", "text": "The simplest technique is to start naming objects around your room in English every single **morning**."},
            {"speaker": "Host2", "text": "Small daily habits like that train your brain to react **instantly** without any mental friction!"}
        ]
    },
    {
        "topic": "Building Confidence to Speak English Everyday",
        "keyword": "CONFIDENCE",
        "sub": "SPEAK WITHOUT FEAR",
        "turns": [
            {"speaker": "Host1", "text": "Speaking a new language can feel scary, but confidence grows with every small **conversation**."},
            {"speaker": "Host2", "text": "Remember that people care about your message and ideas, not about minor grammatical **mistakes**."},
            {"speaker": "Host1", "text": "Focus on speaking clearly and slowly rather than trying to speak too **fast**."},
            {"speaker": "Host2", "text": "Patience and steady practice will transform you into a relaxed and **natural** speaker!"}
        ]
    }
]

def load_font(size, bold=True):
    fonts_to_try = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/trebucbd.ttf" if bold else "C:/Windows/Fonts/trebuc.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
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

def chunk_turn_text(text):
    # Splits turn dialogue into punchy, bite-sized subtitle lines (5 to 9 words max)
    raw_sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    chunks = []
    for s in raw_sentences:
        words = s.split()
        if len(words) <= 9:
            chunks.append(s)
        else:
            parts = [p.strip() for p in re.split(r'(?<=[,;:])\s+', s) if p.strip()]
            if len(parts) > 1:
                cur = ""
                for p in parts:
                    if len((cur + " " + p).split()) <= 8:
                        cur = (cur + " " + p).strip()
                    else:
                        if cur: chunks.append(cur)
                        cur = p
                if cur: chunks.append(cur)
            else:
                mid = len(words) // 2
                chunks.append(" ".join(words[:mid]))
                chunks.append(" ".join(words[mid:]))
    return chunks

def generate_script_ai(topic_item, target_turns=4):
    prompt = f"""Write {target_turns} turns of a slow, clear English podcast between Emma and Andrew discussing: {topic_item['topic']}.

RULES:
- Dialogue alternating between Host1 (Emma) and Host2 (Andrew)
- Each turn MUST be 2 short, clear sentences (16-24 words)
- Natural, friendly, encouraging flow
- Wrap exactly 1 key learning word per turn in **asterisks**
- Return as clean JSON array only:
[{{"speaker":"Host1","text":"..."}},{{"speaker":"Host2","text":"..."}}]"""

    key = os.getenv("POLLINATIONS_API_KEY")
    if key:
        try:
            resp = requests.post("https://gen.pollinations.ai/v1/chat/completions", json={
                "model": "gemini-fast",
                "messages": [
                    {"role": "system", "content": "You write slow, natural English podcast dialogue. Wrap 1 key word per turn in **asterisks**."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8
            }, headers={"Authorization": f"Bearer {key}"}, timeout=20)
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
            print(f"[script] AI note: {e}, using curated fallback.")

    return topic_item.get("turns", [
        {"speaker": "Host1", "text": "Welcome back everyone. Today we are exploring why thinking directly in English is the **secret** to real fluency."},
        {"speaker": "Host2", "text": "That is so true. When you translate words in your head first, you naturally hesitate and lose your **confidence**."},
        {"speaker": "Host1", "text": "The simplest technique is to start naming objects around your room in English every single **morning**."},
        {"speaker": "Host2", "text": "Small daily habits like that train your brain to react **instantly** without any mental friction!"}
    ])[:target_turns]

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

def load_base_studio_canvas():
    studio_path = ASSETS_DIR / "host_studio.png"
    if not studio_path.exists():
        studio_path = ASSETS_DIR / "woman_base.png"
    
    if studio_path.exists():
        img = Image.open(studio_path).convert("RGBA")
        return img.resize((VIDEO_WIDTH, VIDEO_HEIGHT), Image.Resampling.LANCZOS)
    else:
        canvas = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), (16, 18, 28, 255))
        return canvas

def draw_vector_mic(draw, center_x, center_y, color=GOLD_ACCENT):
    draw.rounded_rectangle([(center_x - 6, center_y - 12), (center_x + 6, center_y + 4)], radius=4, fill=color)
    draw.arc([(center_x - 10, center_y - 4), (center_x + 10, center_y + 10)], start=0, end=180, fill=color, width=3)
    draw.line([(center_x, center_y + 10), (center_x, center_y + 16)], fill=color, width=3)
    draw.line([(center_x - 6, center_y + 16), (center_x + 6, center_y + 16)], fill=color, width=3)

def render_podcast_chunk_frame(base_canvas, speaker, chunk_text, active_w_idx, frame_anim_idx, elapsed, total_dur, out_path):
    canvas = base_canvas.copy()
    draw = ImageDraw.Draw(canvas)

    # 1. Top Left Channel Pill (Dynamic width - NEVER overflows)
    f_tab = load_font(28, bold=True)
    tb_tab = draw.textbbox((0, 0), CHANNEL_NAME, font=f_tab)
    tw_tab = tb_tab[2] - tb_tab[0]
    
    pill_l = 60
    pill_t = 40
    pill_h = 66
    pill_r = pill_l + 30 + 70 + 20 + tw_tab + 35
    pill_b = pill_t + pill_h

    draw.rounded_rectangle([(pill_l, pill_t), (pill_r, pill_b)], radius=20, fill=DARK_BAR, outline=GOLD_ACCENT, width=3)
    
    # 6 animated wave bars
    wave_x = pill_l + 30
    wave_cy = pill_t + pill_h // 2
    for b in range(6):
        bh = int(14 + 14 * abs(math.sin(frame_anim_idx * 0.45 + b * 1.15)))
        bx = wave_x + b * 11
        draw.line([(bx, wave_cy - bh // 2), (bx, wave_cy + bh // 2)], fill=GOLD_ACCENT, width=3)
    
    draw.text((wave_x + 85, wave_cy), CHANNEL_NAME, fill=WHITE, font=f_tab, anchor="lm")

    # 2. Top Right Speaker Pill (Dynamic width - NEVER overflows)
    speaker_name = "EMMA" if speaker == "Host1" else "ANDREW"
    spk_text = f"HOST: {speaker_name}"
    f_spk = load_font(28, bold=True)
    tb_s = draw.textbbox((0, 0), spk_text, font=f_spk)
    tw_s = tb_s[2] - tb_s[0]

    pill_s_w = tw_s + 130
    pill_s_r = 1860
    pill_s_l = pill_s_r - pill_s_w
    pill_s_t = 40
    pill_s_b = pill_s_t + pill_h

    draw.rounded_rectangle([(pill_s_l, pill_s_t), (pill_s_r, pill_s_b)], radius=20, fill=DARK_BAR, outline=GOLD_ACCENT, width=3)
    
    mic_x = pill_s_l + 35
    mic_y = pill_s_t + pill_h // 2
    draw_vector_mic(draw, mic_x, mic_y, color=GOLD_ACCENT)
    
    dot_x = mic_x + 22
    draw.ellipse([(dot_x - 4, mic_y - 4), (dot_x + 4, mic_y + 4)], fill=LIVE_GREEN)
    draw.text((dot_x + 18, mic_y), spk_text, fill=GOLD_ACCENT, font=f_spk, anchor="lm")

    # 3. Subtitle Chunk Rendering (Safe area: x: 920 to 1840, y: 220 to 520)
    words_raw = chunk_text.split()
    clean_words = [re.sub(r'[\*\*\.]', '', w).strip() for w in words_raw if w.strip()]
    if not clean_words: clean_words = ["Speak", "clearly"]

    f_sub = load_font(80, bold=True)
    max_sub_w = 920
    lines = []
    cur_line = []
    cur_w = 0

    for w_i, raw_w in enumerate(words_raw):
        clean_w = re.sub(r'\*\*(.*?)\*\*', r'\1', raw_w)
        wb = draw.textbbox((0, 0), clean_w + " ", font=f_sub)
        wl = wb[2] - wb[0]
        if cur_w + wl > max_sub_w and cur_line:
            lines.append(cur_line)
            cur_line = [(w_i, clean_w, wl)]
            cur_w = wl
        else:
            cur_line.append((w_i, clean_w, wl))
            cur_w += wl
    if cur_line:
        lines.append(cur_line)

    line_h = 108
    total_h = len(lines) * line_h
    center_x = 1380
    center_y = 440
    start_y = max(180, center_y - total_h // 2)

    # Soft radial dark glow behind text for 100% contrast against studio lighting
    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    glow_w = max(sum(item[2] for item in l) for l in lines) + 160
    glow_h = total_h + 100
    gdraw.rounded_rectangle([
        (center_x - glow_w // 2, start_y + total_h // 2 - glow_h // 2),
        (center_x + glow_w // 2, start_y + total_h // 2 + glow_h // 2)
    ], radius=35, fill=(0, 0, 0, 160))
    glow = glow.filter(ImageFilter.GaussianBlur(25))
    canvas.paste(glow, (0, 0), glow)

    # Deep drop shadow
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    for l_i, line in enumerate(lines):
        lw = sum(item[2] for item in line)
        lx = center_x - lw // 2
        ly = start_y + l_i * line_h
        for (w_i, clean_w, wl) in line:
            sdraw.text((lx + 4, ly + 5), clean_w, fill=(0, 0, 0, 255), font=f_sub)
            lx += wl
    shadow = shadow.filter(ImageFilter.GaussianBlur(5))
    canvas.paste(shadow, (0, 0), shadow)

    # Foreground text with active spoken word highlighted in Gold
    draw = ImageDraw.Draw(canvas)
    for l_i, line in enumerate(lines):
        lw = sum(item[2] for item in line)
        lx = center_x - lw // 2
        ly = start_y + l_i * line_h
        for (w_i, clean_w, wl) in line:
            is_active = (w_i == active_w_idx)
            col = GOLD_ACCENT if is_active else WHITE
            draw.text((lx, ly), clean_w, fill=col, font=f_sub)
            lx += wl

    # Subtitle tagline underneath
    f_tag = load_font(30, bold=False)
    draw.text((center_x, start_y + total_h + 24), TAGLINE, fill=MUTED_GOLD, font=f_tag, anchor="mt")

    # 4. Bottom Timeline & Progress Bar
    draw.line([(0, 1025), (VIDEO_WIDTH, 1025)], fill=(45, 50, 70), width=2)
    ratio = min(1.0, elapsed / max(1.0, total_dur))
    draw.line([(0, 1025), (int(VIDEO_WIDTH * ratio), 1025)], fill=GOLD_ACCENT, width=5)

    f_bot = load_font(26, bold=False)
    draw.text((70, 1052), "Slow English Fluency Lounge • Natural Everyday English", fill=MUTED_WHITE, font=f_bot, anchor="lm")
    time_str = f"{int(elapsed // 60):02d}:{int(elapsed % 60):02d} / {int(total_dur // 60):02d}:{int(total_dur % 60):02d}"
    draw.text((1850, 1052), time_str, fill=GOLD_ACCENT, font=f_bot, anchor="rm")

    canvas.convert("RGB").save(out_path, quality=95)

def assemble_video(topic_item, turns, audio_list, run_dir):
    frames_dir = run_dir / "frames"
    clips_dir = run_dir / "clips"
    frames_dir.mkdir(parents=True, exist_ok=True)
    clips_dir.mkdir(parents=True, exist_ok=True)

    base_canvas = load_base_studio_canvas()
    total_dur = sum(a["duration"] for a in audio_list)
    elapsed = 0.0
    clips = []

    for i, (turn, audio) in enumerate(zip(turns, audio_list)):
        dur = audio["duration"]
        speaker = turn["speaker"]
        chunks = chunk_turn_text(turn["text"])
        total_turn_words = sum(len(c.split()) for c in chunks)
        
        turn_frames_dir = frames_dir / f"turn_{i:03d}"
        turn_frames_dir.mkdir(parents=True, exist_ok=True)

        frame_seq = 0
        chunk_elapsed = elapsed

        for c_idx, chunk_str in enumerate(chunks):
            c_words = len(chunk_str.split())
            c_dur = dur * (c_words / max(1, total_turn_words))
            subframes_count = max(c_words, int(c_dur * 2))

            for s in range(subframes_count):
                frame_p = turn_frames_dir / f"frame_{frame_seq:04d}.png"
                active_w_idx = min(c_words - 1, int((s / max(1, subframes_count)) * c_words))
                sub_elapsed = chunk_elapsed + (s / max(1, subframes_count)) * c_dur
                
                render_podcast_chunk_frame(
                    base_canvas, speaker, chunk_str, active_w_idx,
                    frame_seq, sub_elapsed, total_dur, str(frame_p)
                )
                frame_seq += 1

            chunk_elapsed += c_dur

        fps_turn = frame_seq / max(0.5, dur)
        clip_p = clips_dir / f"clip_{i:03d}.mp4"
        input_pattern = str(turn_frames_dir / "frame_%04d.png")

        cmd = [
            "ffmpeg", "-y",
            "-framerate", str(fps_turn),
            "-i", input_pattern,
            "-i", audio["path"],
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            "-preset", "ultrafast",
            str(clip_p)
        ]
        subprocess.run(cmd, check=True, capture_output=True)

        clips.append(clip_p)
        elapsed += dur

    concat_txt = run_dir / "concat.txt"
    with open(concat_txt, "w") as f:
        for c in clips:
            f.write(f"file '{c.resolve().as_posix()}'\n")

    final_video = run_dir / "podcast_lounge_final.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(final_video)
    ], check=True, capture_output=True)

    return final_video, total_dur

async def run_podcast_generation(topic_idx=0, turns_count=4):
    topic_item = TOPICS[topic_idx % len(TOPICS)]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = OUTPUT_DIR / f"run_{ts}"
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"[Podcast Lounge] Generating 16:9 Broadcast: '{topic_item['topic']}' ({turns_count} turns)...")
    turns = generate_script_ai(topic_item, target_turns=turns_count)
    audio_list = await generate_audio_files(turns, run_dir)
    video_p, dur = assemble_video(topic_item, turns, audio_list, run_dir)

    meta = {
        "title": f"Slow English Fluency Lounge: {topic_item['topic']} 🎙️ Daily English Podcast",
        "description": f"Listen and master spoken English! Today's focus: '{topic_item['topic']}'. Follow for daily slow English practice! ☕✨",
        "topic": topic_item["topic"],
        "duration_seconds": dur
    }
    with open(run_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"[Podcast Lounge] Video ready: {video_p}")
    return video_p, meta

if __name__ == "__main__":
    asyncio.run(run_podcast_generation(topic_idx=0, turns_count=4))
