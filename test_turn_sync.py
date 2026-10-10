import asyncio
import edge_tts
import re

async def test_dialogue_sync():
    turns = [
        {"speaker": "Host1", "text": "Welcome back everyone. Today we are exploring why thinking directly in English is the **secret** to real fluency."},
        {"speaker": "Host2", "text": "That is so true. When you translate words in your head first, you naturally hesitate and lose your **confidence**."}
    ]
    
    for i, t in enumerate(turns):
        voice = "en-US-AvaNeural" if t["speaker"] == "Host1" else "en-US-AndrewNeural"
        clean_spoken = re.sub(r'\*\*(.*?)\*\*', r'\1', t["text"])
        comm = edge_tts.Communicate(clean_spoken, voice, rate="-15%")
        
        sentences = []
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
        print(f"\nTurn {i+1} ({t['speaker']} - {voice}):")
        for s_idx, s in enumerate(sentences):
            print(f"  Sentence {s_idx+1}: [{s['start']:.2f}s - {s['end']:.2f}s | {s['duration']:.2f}s] '{s['text']}'")

if __name__ == "__main__":
    asyncio.run(test_dialogue_sync())
