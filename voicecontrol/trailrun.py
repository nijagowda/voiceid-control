import serial
import time
import threading
import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr

# Setup serial connection to Arduino
try:
    arduino = serial.Serial('COM8', 9600)
    time.sleep(2)
except Exception as e:
    messagebox.showerror("Connection Error", f"Arduino not connected: {e}")
    exit()

recognizer = sr.Recognizer()
listening = False

# Voice recognition function in a thread
def listen_for_commands():
    global listening
    while listening:
        try:
            with sr.Microphone() as source:
                status_label.config(text="🎤 Listening...")
                audio = recognizer.listen(source, timeout=5)

            command = recognizer.recognize_google(audio).lower()
            status_label.config(text=f"✅ Heard: {command}")
            handle_command(command)

            if "exit" in command or "stop program" in command:
                listening = False
                status_label.config(text="🛑 Voice control stopped")
                break

        except sr.WaitTimeoutError:
            status_label.config(text="⏱️ No voice detected")
        except sr.UnknownValueError:
            status_label.config(text="❌ Could not understand")
        except Exception as e:
            status_label.config(text=f"❗ Error: {e}")
            break

# Handle command and send to Arduino
def handle_command(command):
    if "turn on" in command:
        arduino.write(b'on\n')
    elif "turn off" in command:
        arduino.write(b'off\n')
    elif "blink" in command:
        arduino.write(b'blink\n')
    elif "fan on" in command:
        arduino.write(b'fan_on\n')
    elif "fan off" in command:
        arduino.write(b'fan_off\n')
    # You can add more here

# Start/stop voice control
def start_listening():
    global listening
    listening = True
    threading.Thread(target=listen_for_commands).start()

def stop_listening():
    global listening
    listening = False
    status_label.config(text="🛑 Voice control stopped")

# Manual control from GUI buttons
def manual_send(cmd):
    arduino.write((cmd + '\n').encode())
    status_label.config(text=f"📤 Sent: {cmd}")

# GUI Setup
root = tk.Tk()
root.title("Voice-Controlled Home Automation")
root.geometry("400x300")
root.resizable(False, False)

title = tk.Label(root, text="🎙️ Voice Control Panel", font=("Arial", 16, "bold"))
title.pack(pady=10)

status_label = tk.Label(root, text="🔘 Idle", font=("Arial", 12))
status_label.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="🎤 Start Listening", command=start_listening, width=18).grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="⛔ Stop Listening", command=stop_listening, width=18).grid(row=0, column=1, padx=5, pady=5)

# Optional manual controls
tk.Label(root, text="🧪 Manual Controls:", font=("Arial", 12, "bold")).pack()
manual_frame = tk.Frame(root)
manual_frame.pack(pady=5)

tk.Button(manual_frame, text="Turn ON", command=lambda: manual_send("on")).grid(row=0, column=0, padx=5, pady=5)
tk.Button(manual_frame, text="Turn OFF", command=lambda: manual_send("off")).grid(row=0, column=1, padx=5, pady=5)
tk.Button(manual_frame, text="Blink", command=lambda: manual_send("blink")).grid(row=1, column=0, padx=5, pady=5)
tk.Button(manual_frame, text="Fan ON", command=lambda: manual_send("fan_on")).grid(row=1, column=1, padx=5, pady=5)
tk.Button(manual_frame, text="Fan OFF", command=lambda: manual_send("fan_off")).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
