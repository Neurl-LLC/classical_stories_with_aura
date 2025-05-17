import os
import re
import sys
import subprocess
from typing import List, Tuple, Dict
from deepgram import DeepgramClient, SpeakOptions

# Set up Deepgram client
deepgram = DeepgramClient()

# Constants
OUTPUT_DIR = "speech_outputs"
FINAL_AUDIO = "final_output.mp3"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_script(filepath: str) -> List[Tuple[str, str]]:
    """Parses the script and returns a list of (speaker, line) tuples."""
    pattern = re.compile(r'^\[(.*?)\]: (.*)')
    lines = []

    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            match = pattern.match(line.strip())
            if match:
                speaker, text = match.groups()
                lines.append((speaker.strip(), text.strip()))
    return lines

def extract_unique_speakers(lines: List[Tuple[str, str]]) -> List[str]:
    """Extracts a list of unique speakers from the script."""
    return sorted(set(speaker for speaker, _ in lines))

def prompt_for_voice_map(speakers: List[str]) -> Dict[str, str]:
    """Prompts the user to assign a voice to each character."""
    print("\n🎭 Assign voices to each character.")
    print("Refer to Deepgram's Aura 2 models (e.g., aura-2-orpheus-en, aura-2-saturn-en, etc.)")
    voice_map = {}
    for speaker in speakers:
        voice = input(f"🗣️  Assign a voice for '{speaker}': ").strip()
        voice_map[speaker] = voice
    return voice_map

def generate_speech(index: int, speaker: str, text: str, voice_map: Dict[str, str]) -> str:
    """Generates speech audio for the given speaker and line."""
    voice = voice_map.get(speaker)
    if not voice:
        raise ValueError(f"No voice assigned for speaker: {speaker}")

    speak_options = SpeakOptions(model=voice)
    output_file = os.path.join(OUTPUT_DIR, f"{index:03d}_{speaker.replace(' ', '_')}.mp3")
    SPEAK_TEXT = {"text": text}

    print(f"🔊 Generating speech for [{speaker}]: {text[:40]}...")
    response = deepgram.speak.rest.v("1").save(output_file, SPEAK_TEXT, speak_options)

    return output_file

def concatenate_audio_files(audio_files: List[str], output_path: str):
    """Concatenates audio files into one using ffmpeg."""
    list_file = os.path.join(OUTPUT_DIR, "file_list.txt")
    with open(list_file, "w", encoding="utf-8") as f:
        for file in audio_files:
            f.write(f"file '{os.path.abspath(file)}'\n")

    print("🎧 Concatenating audio files...")
    subprocess.run([
        "ffmpeg", "-f", "concat", "-safe", "0", "-i", list_file,
        "-c", "copy", output_path
    ], check=True)
    print(f"✅ Final audio saved as: {output_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python voice_generator.py <script_file.txt>")
        sys.exit(1)

    script_path = sys.argv[1]
    lines = parse_script(script_path)
    speakers = extract_unique_speakers(lines)
    voice_map = prompt_for_voice_map(speakers)

    audio_files = []
    for i, (speaker, text) in enumerate(lines):
        audio_path = generate_speech(i, speaker, text, voice_map)
        audio_files.append(audio_path)

    concatenate_audio_files(audio_files, FINAL_AUDIO)

if __name__ == "__main__":
    main()

