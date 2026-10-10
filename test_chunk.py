import re

text = "Hi everyone, and welcome back to the show. Today we're talking about thinking directly in English, which can feel really challenging."

def chunk_turn_text(text):
    # Split text into natural, punchy sentences / phrases
    # Target: 5 to 9 words per subtitle (exactly 1 line or 2 short lines)
    raw_sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    chunks = []
    
    for s in raw_sentences:
        words = s.split()
        if len(words) <= 9:
            chunks.append(s)
        else:
            # Split at comma / semicolon or mid-point
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
                # Split roughly in half
                mid = len(words) // 2
                chunks.append(" ".join(words[:mid]))
                chunks.append(" ".join(words[mid:]))
                
    return chunks

chunks = chunk_turn_text(text)
for i, c in enumerate(chunks):
    print(f"Chunk {i+1} ({len(c.split())} words): '{c}'")
