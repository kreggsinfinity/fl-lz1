import asyncio
import edge_tts
import numpy as np
from pydub import AudioSegment

async def test_audio_sync():
    text = "Thinking directly in English is the secret to real fluency."
    comm = edge_tts.Communicate(text, "en-US-AndrewNeural", rate="-15%")
    
    mp3_path = "test_sync.mp3"
    await comm.save(mp3_path)
    print("Saved test_sync.mp3")
    
    # Load audio samples using pydub
    audio = AudioSegment.from_file(mp3_path)
    sample_rate = audio.frame_rate
    samples = np.array(audio.get_array_of_samples(), dtype=float)
    if audio.channels > 1:
        samples = samples.reshape((-1, audio.channels)).mean(axis=1)
        
    duration = len(samples) / sample_rate
    print(f"Sample Rate: {sample_rate}, Samples: {len(samples)}, Duration: {duration:.2f}s")
    
    # Calculate energy across 10 sample timestamps
    num_bars = 16
    for step in range(12):
        t = (step / 11.0) * duration
        win_size = int(0.06 * sample_rate)
        center_idx = int(t * sample_rate)
        start_idx = max(0, center_idx - win_size // 2)
        end_idx = min(len(samples), center_idx + win_size // 2)
        chunk = samples[start_idx:end_idx]
        
        if len(chunk) > 100:
            rms = np.sqrt(np.mean(chunk**2))
            # Normalize to 0.0 - 1.0
            norm_rms = min(1.0, rms / 15000.0)
            
            # FFT for multi-bar frequency distribution
            fft_vals = np.abs(np.fft.rfft(chunk))
            fft_freqs = np.fft.rfftfreq(len(chunk), 1.0 / sample_rate)
            
            # 16 band heights
            bar_heights = []
            for b in range(num_bars):
                # Speech range: 100 Hz to 6000 Hz
                f_min = 100 * (1.28 ** b)
                f_max = 100 * (1.28 ** (b + 1))
                mask = (fft_freqs >= f_min) & (fft_freqs < f_max)
                if np.any(mask):
                    val = np.mean(fft_vals[mask])
                    h = int(min(1.0, val / 350000.0) * 45)
                else:
                    h = 4
                bar_heights.append(max(4, h))
        else:
            norm_rms = 0.0
            bar_heights = [4] * num_bars
            
        print(f"t={t:5.2f}s | RMS: {norm_rms:4.2f} | Bars: {bar_heights[:8]}")

if __name__ == "__main__":
    asyncio.run(test_audio_sync())
