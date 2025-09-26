import serial
import time
import os
import numpy as np
import sounddevice as sd
from resemblyzer import preprocess_wav, VoiceEncoder
import soundfile as sf
import speech_recognition as sr
import pyttsx3

# === 1. Setup Serial and TTS ===
arduino = serial.Serial('COM9', 9600)
time.sleep(2)

engine = pyttsx3.init()
engine.setProperty('rate', 160)

# === 2. Load Voice Profiles Safely ===
encoder = VoiceEncoder()
profiles = {}

def load_profiles():
    for name in ["saif", "aisha"]:
        path = f"voicecontrol/voices/{name}.wav"
        if not os.path.isfile(path):
            print(f"❌ Missing profile: {path}")
            continue
        try:
            profiles[name] = encoder.embed_utterance(preprocess_wav(path))
            print(f"✅ Loaded profile for {name}")
        except Exception as e:
            print(f"❌ Error loading {name}.wav:", e)

load_profiles()
if len(profiles) < 2:
    print("⚠️ Not all profiles loaded. Exiting.")
    exit()

recognizer = sr.Recognizer()

# === 3. Record Audio ===
def record_audio(filename="live.wav", duration=3):
    fs = 16000
    print("🎙️ Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    audio = audio.flatten()
    sf.write(filename, audio, fs, format='WAV', subtype='PCM_16')

# === 4. Identify Speaker ===
def identify_user(filename="live.wav"):
    try:
        live_embed = encoder.embed_utterance(preprocess_wav(filename))
        scores = {
            name: np.dot(live_embed, profile) / (np.linalg.norm(live_embed) * np.linalg.norm(profile))
            for name, profile in profiles.items()
        }
        best_match = max(scores, key=scores.get)
        print(f"🧠 Detected speaker: {best_match}")
        return best_match
    except Exception as e:
        print("❌ Speaker identification failed:", e)
        return None

# === 5. Recognize Command ===
def recognize_command(filename="live.wav"):
    try:
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio).lower()
            print(f"🗣️ Recognized: {text}")
            if "turn on" in text:
                return "on"
            elif "turn off" in text:
                return "off"
            elif "exit" in text:
                return "exit"
    except sr.UnknownValueError:
        print("❌ Could not understand the speech.")
    except Exception as e:
        print("❌ Command recognition error:", e)
    return None

# === 6. Send to Arduino ===
def send_command(user, action):
    cmd = f"turn{action}_{user}"
    arduino.write((cmd + "\n").encode())
    print(f"📤 Sent to Arduino: {cmd}")
    engine.say(f"{user.capitalize()}, your lights are turned {action}")
    engine.runAndWait()

# === 7. Loop ===
try:
    while True:
        record_audio()
        user = identify_user()
        action = recognize_command()

        if action == "exit":
            print("👋 Exit command received. Closing program.")
            engine.say("Exiting the system.")
            engine.runAndWait()
            break
        elif user and action in ["on", "off"]:
            send_command(user, action)
        else:
            print("⚠️ No valid action or speaker.")

        time.sleep(1)

except KeyboardInterrupt:
    print("🛑 Interrupted by user.")

finally:
    arduino.close()
    print("🔌 Serial connection closed.")
