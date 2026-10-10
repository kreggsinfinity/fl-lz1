import asyncio
import edge_tts
import json
import wave
import numpy as np

async def test_word_boundaries():
    text = "Welcome back to the show. Today we are learning English."
    comm = edge_tts.Communicate(text, "en-US-AvaNeural", rate="-15%")
    
    words = []
    audio_bytes = bytearray()
    
    async for chunk in comm.stream():
        if chunk["type"] == "word_boundary":
            start_s = chunk["offset"] / 10_000_000.0  # converted from 100ns to seconds
            dur_s = chunk["duration"] / 10_000_000.0
            words.append({
                "text": chunk["text"],
                "start": start_s,
                "end": start_s + dur_s,
                "duration": dur_s
            })
        elif chunk["type"] == "audio":
            audio_bytes.extend(chunk["data"])
            
    print(f"Captured {len(words)} word boundaries:")
    for w in words:
        print(f"  [{w['start']:.2f}s - {w['end']:.2f}s] {w['text']}")
        
    with open("test_voice.mp3", "wb") as f:
        f.write(audio_bytes)
    print("Saved test_voice.mp3")

if __name__ == "__main__":
    asyncio.run(test_word_boundaries())
