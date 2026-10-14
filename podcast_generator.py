"""
SLOW ENGLISH FLUENCY PODCAST LOUNGE - 16:9 FULL HD (1920x1080)
Format: 1920x1080 Landscape Studio Broadcast
Features:
- Photorealistic studio host setting on the left (Shure SM7B, luxury acoustic wood lounge)
- Dynamic auto-sized top pills (Channel name + Host live badge, NO text overflow, NO tofu emojis)
- Frame-perfect subtitle synchronization using Microsoft Edge TTS SentenceBoundary timestamps
- Bite-sized phrase & sentence subtitles with active word karaoke highlighting
- Physically synchronized 16-band audio equalizer reactive to real voice speech frequencies
- Fixed bottom branding tagline (NO jumping captions, NO time numbers)
"""
import os, sys, json, math, subprocess, random, requests, re, asyncio
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from dotenv import load_dotenv
import edge_tts
import numpy as np
from pydub import AudioSegment

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
MUTED_GOLD = (235, 225, 200)
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


def configure_edge_tts():
    """Ensure edge_tts connects to Microsoft's active Cognitive Services endpoint to avoid 403 Forbidden."""
    try:
        import edge_tts.constants
        import edge_tts.communicate
        token = getattr(edge_tts.constants, "TRUSTED_CLIENT_TOKEN", "6A5AA1D4EAFF4E9FB37E23D68491D6F4")
        new_url = (
            "wss://api.msedgeservices.com/tts/cognitiveservices/websocket/v1"
            f"?Ocp-Apim-Subscription-Key={token}"
        )
        edge_tts.constants.WSS_URL = new_url
        edge_tts.communicate.WSS_URL = new_url
    except Exception as e:
        print(f"[edge_tts] configure warning: {e}")

async def synthesize_turn_speech(spoken, voice, rate, pitch=None, max_retries=3):
    """Synthesizes speech with active endpoint, 3x self-healing retries, and gTTS fallback."""
    configure_edge_tts()
    for attempt in range(max_retries):
        try:
            kwargs = {"rate": rate}
            if pitch:
                kwargs["pitch"] = pitch
            comm = edge_tts.Communicate(spoken, voice, **kwargs)
            sentences = []
            audio_bytes = bytearray()
            async for chunk in comm.stream():
                if chunk.get("type") == "SentenceBoundary":
                    start_s = chunk["offset"] / 10_000_000.0
                    dur_s = chunk["duration"] / 10_000_000.0
                    sentences.append({
                        "text": chunk["text"],
                        "start": start_s,
                        "duration": dur_s,
                        "end": start_s + dur_s
                    })
                elif chunk.get("type") == "audio":
                    audio_bytes.extend(chunk["data"])
            
            if len(audio_bytes) > 500:
                return audio_bytes, sentences
            else:
                print(f"    [TTS] Attempt {attempt+1}: bytes too small ({len(audio_bytes)}), retrying...")
        except Exception as e:
            print(f"    [TTS] Attempt {attempt+1} error: {e}")
        await asyncio.sleep(2 * (attempt + 1))
    
    # Fallback to gTTS if Edge TTS drops out
    try:
        from gtts import gTTS
        import io
        print(f"    [TTS] Active endpoint exhausted. Using gTTS fallback...")
        tts = gTTS(text=spoken, lang="en")
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        return bytearray(buf.getvalue()), []
    except Exception as fb_err:
        print(f"    [TTS] Fallback error: {fb_err}")
        return None, []

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
        audio_bytes, sentences = await synthesize_turn_speech(spoken, voice, rate=VOICE_RATE)
        if audio_bytes is None:
            audio_bytes = bytearray()
        with open(mp3_p, "wb") as f:
            f.write(audio_bytes)

        # Measure audio duration via ffprobe
        try:
            r = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(mp3_p)],
                capture_output=True, text=True, check=True
            )
            duration = float(r.stdout.strip())
        except:
            duration = sentences[-1]["end"] if sentences else 5.0

        # Subdivide long sentences into short bite-sized clauses (max 8 words) for single-line subtitles
        timed_phrases = []
        for s in sentences:
            s_text = s["text"]
            s_start = s["start"]
            s_dur = s["duration"]
            words = s_text.split()
            
            if len(words) <= 8:
                timed_phrases.append({
                    "text": s_text,
                    "start": s_start,
                    "end": s_start + s_dur,
                    "duration": s_dur
                })
            else:
                # Split at comma / semicolon or midpoint
                parts = [p.strip() for p in re.split(r'(?<=[,;:])\s+', s_text) if p.strip()]
                if len(parts) > 1:
                    total_w = sum(len(p.split()) for p in parts)
                    cur_t = s_start
                    for p in parts:
                        p_w = len(p.split())
                        p_dur = s_dur * (p_w / max(1, total_w))
                        timed_phrases.append({
                            "text": p,
                            "start": cur_t,
                            "end": cur_t + p_dur,
                            "duration": p_dur
                        })
                        cur_t += p_dur
                else:
                    mid = len(words) // 2
                    p1 = " ".join(words[:mid])
                    p2 = " ".join(words[mid:])
                    dur1 = s_dur * (len(p1.split()) / len(words))
                    dur2 = s_dur - dur1
                    timed_phrases.append({"text": p1, "start": s_start, "end": s_start + dur1, "duration": dur1})
                    timed_phrases.append({"text": p2, "start": s_start + dur1, "end": s_start + s_dur, "duration": dur2})

        # Load raw audio samples for 100% physical FFT frequency equalizer calculation
        audio_seg = AudioSegment.from_file(str(mp3_p))
        sample_rate = audio_seg.frame_rate
        raw_samples = np.array(audio_seg.get_array_of_samples(), dtype=float)
        if audio_seg.channels > 1:
            raw_samples = raw_samples.reshape((-1, audio_seg.channels)).mean(axis=1)

        audio_list.append({
            "path": str(mp3_p),
            "duration": duration,
            "speaker": turn["speaker"],
            "turn_text": turn["text"],
            "timed_phrases": timed_phrases,
            "raw_samples": raw_samples,
            "sample_rate": sample_rate
        })
        
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

def compute_physical_equalizer_bars(raw_samples, sample_rate, t_sec, num_bars=16):
    """
    Computes 16-band physical frequency spectrum directly from voice audio samples at timestamp t_sec.
    When speaking: bars dance to actual vocal frequencies.
    When pausing/silent: smoothly drops to 4px resting floor.
    """
    win_size = int(0.06 * sample_rate) # 60ms analysis window
    center_idx = int(t_sec * sample_rate)
    start_idx = max(0, center_idx - win_size // 2)
    end_idx = min(len(raw_samples), center_idx + win_size // 2)
    chunk = raw_samples[start_idx:end_idx]

    if len(chunk) < 100:
        return [4] * num_bars

    rms = np.sqrt(np.mean(chunk**2))
    if rms < 350.0:  # Silence / breath between words
        return [4] * num_bars

    fft_vals = np.abs(np.fft.rfft(chunk))
    fft_freqs = np.fft.rfftfreq(len(chunk), 1.0 / sample_rate)

    bar_heights = []
    for b in range(num_bars):
        f_min = 100 * (1.28 ** b)
        f_max = 100 * (1.28 ** (b + 1))
        mask = (fft_freqs >= f_min) & (fft_freqs < f_max)
        if np.any(mask):
            val = np.mean(fft_vals[mask])
            h = int(min(1.0, val / 320000.0) * 44)
        else:
            h = 4
        bar_heights.append(max(4, min(48, h)))

    return bar_heights

def render_podcast_frame(base_canvas, speaker, phrase_text, active_w_idx, eq_bars, frame_idx, elapsed, total_dur, out_path):
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
    
    # 6 wave bars in channel pill
    wave_x = pill_l + 30
    wave_cy = pill_t + pill_h // 2
    for b in range(6):
        bh = int(14 + 14 * abs(math.sin(frame_idx * 0.45 + b * 1.15)))
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

    # 3. Subtitle Phrase Rendering (Safe area: x: 920 to 1840, center_y = 350)
    words_raw = phrase_text.split()
    clean_words = [re.sub(r'[\*\*\.]', '', w).strip() for w in words_raw if w.strip()]
    if not clean_words: clean_words = ["Speak", "clearly"]

    f_sub = load_font(78, bold=True)
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

    line_h = 105
    total_h = len(lines) * line_h
    center_x = 1380
    center_y = 325
    start_y = max(170, center_y - total_h // 2)

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

    # 4. Physically Synchronized Sound Equalizer Plate (Aesthetic podcast style)
    # 16 smooth rounded bars below subtitle with generous breathing gap
    eq_cx = 1380
    eq_cy = 580
    eq_w = 440
    eq_h = 58
    draw.rounded_rectangle([
        (eq_cx - eq_w // 2, eq_cy - eq_h // 2),
        (eq_cx + eq_w // 2, eq_cy + eq_h // 2)
    ], radius=16, fill=(14, 16, 26, 220), outline=(255, 215, 0, 180), width=2)

    num_b = 16
    bw = 12
    gap = 12
    total_bars_w = num_b * bw + (num_b - 1) * gap
    start_bx = eq_cx - total_bars_w // 2

    for b_i in range(num_b):
        bh = eq_bars[b_i] if b_i < len(eq_bars) else 4
        bx = start_bx + b_i * (bw + gap)
        by_top = eq_cy - bh // 2
        by_bot = eq_cy + bh // 2
        draw.rounded_rectangle([(bx, by_top), (bx + bw, by_bot)], radius=6, fill=GOLD_ACCENT)

    # 5. Fixed Bottom Footer Ribbon (NO jumping captions, NO time numbers)
    draw.line([(0, 1025), (VIDEO_WIDTH, 1025)], fill=(45, 50, 70), width=2)
    ratio = min(1.0, elapsed / max(1.0, total_dur))
    draw.line([(0, 1025), (int(VIDEO_WIDTH * ratio), 1025)], fill=GOLD_ACCENT, width=4)

    f_foot = load_font(28, bold=False)
    draw.text((center_x, 1052), TAGLINE, fill=MUTED_GOLD, font=f_foot, anchor="mm")

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

    for i, audio in enumerate(audio_list):
        dur = audio["duration"]
        speaker = audio["speaker"]
        timed_phrases = audio["timed_phrases"]
        raw_samples = audio["raw_samples"]
        sample_rate = audio["sample_rate"]

        turn_frames_dir = frames_dir / f"turn_{i:03d}"
        turn_frames_dir.mkdir(parents=True, exist_ok=True)

        # Video at 10 frames per second for ultra-fluid synchronization
        fps_turn = 10
        total_turn_frames = max(1, int(dur * fps_turn))

        for f_idx in range(total_turn_frames):
            frame_p = turn_frames_dir / f"frame_{f_idx:04d}.png"
            t_in_turn = (f_idx / total_turn_frames) * dur
            sub_elapsed = elapsed + t_in_turn

            # 1. Determine active phrase based on exact Edge TTS timestamps
            active_phrase = timed_phrases[0] if timed_phrases else {"text": "Listen carefully", "start": 0, "end": dur}
            for p in timed_phrases:
                if p["start"] <= t_in_turn <= p["end"]:
                    active_phrase = p
                    break
                elif t_in_turn > p["end"]:
                    active_phrase = p

            # 2. Determine active word inside that active phrase
            p_text = active_phrase["text"]
            p_words = p_text.split()
            p_dur = max(0.2, active_phrase["end"] - active_phrase["start"])
            rel_t = max(0.0, min(p_dur, t_in_turn - active_phrase["start"]))
            active_w_idx = min(len(p_words) - 1, int((rel_t / p_dur) * len(p_words)))

            # 3. Compute 16-band physical audio equalizer directly from real voice audio
            eq_bars = compute_physical_equalizer_bars(raw_samples, sample_rate, t_in_turn, num_bars=16)

            render_podcast_frame(
                base_canvas, speaker, p_text, active_w_idx,
                eq_bars, f_idx, sub_elapsed, total_dur, str(frame_p)
            )

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
