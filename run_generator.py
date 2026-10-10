import sys
import asyncio
from podcast_generator import run_podcast_generation

def main():
    turns = 4
    if "--test" in sys.argv:
        turns = 2
    elif "--full" in sys.argv:
        turns = 16
    print(f"Starting Slow English Podcast Lounge generator (turns={turns})...")
    video_path, meta = asyncio.run(run_podcast_generation(topic_idx=0, turns_count=turns))
    print(f"Done! Final video generated: {video_path}")

if __name__ == "__main__":
    main()
