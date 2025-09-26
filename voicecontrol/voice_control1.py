import serial
import time
from resemblyzer import preprocess_wav, VoiceEncoder
from scipy.io.wavfile import write
import sounddevice as sd
import numpy as np

# === 1. Connect to Arduino ===
arduino = serial.Serial('COM9', 9600)  # Replace COM9 with your actual port
time.sleep(2)

# === 2. Load voice profiles ===
encoder = VoiceEncoder()
profiles = {
    "nija": encoder.embed_utterance(preprocess_wav("voices/nija.wav")),
    "saif": encoder.embed_utterance(preprocess_wav("voices/saif.wav")),
    "aisha": encoder.embed_utterance(preprocess_wav("voices/aisha.wav")),
    "nusrat": encoder.embed_utterance(preprocess_wav("voices/nusrat.wav"))
}

# === 3. Record live voice ===
def record_live_audio(path="live.wav", duration=3):
    fs = 16000
    print("🎙️ Listening... speak now!")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(path, fs, audio)

# === 4. Identify who spoke ===
def identify_user(path="live.wav"):
    live_embed = encoder.embed_utterance(preprocess_wav(path))
    scores = {
        name: np.dot(live_embed, profile) / (np.linalg.norm(live_embed) * np.linalg.norm(profile))
        for name, profile in profiles.items()
    }
    best_match = max(scores, key=scores.get)
    print(f"🧠 Detected: {best_match} (score: {scores[best_match]:.2f})")
    return best_match

# === 5. Continuous loop ===
try:
    while True:
        record_live_audio("live.wav", duration=3)
        user = identify_user("live.wav")

        # Send command to Arduino
        arduino.write((user + '\n').encode())
        print(f"💡 LED ON for: {user}")

        # Optional auto turn-off after 5 seconds
        time.sleep(100)
        arduino.write(b'off\n')
        print("🔌 LED turned OFF\n")

        # Wait before next round
        time.sleep(1)

except KeyboardInterrupt:
    print("🛑 Stopped by user.")
    arduino.write(b'off\n')
    arduino.close()
