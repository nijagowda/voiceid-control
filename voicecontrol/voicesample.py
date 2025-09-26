import sounddevice as sd
from scipy.io.wavfile import write
import os

def record_voice(filename, duration=5):
    fs = 16000  # Sample rate
    print(f"🎙️ Recording for {duration} seconds. Speak now...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, audio)
    print(f"✅ Saved as {filename}")

# === Folder to store recordings ===
os.makedirs("voices", exist_ok=True)

# === Record each user ===
record_voice("voices/nija.wav")
record_voice("voices/saif.wav")
record_voice("voices/aisha.wav")
record_voice("voices/nusrat.wav")
