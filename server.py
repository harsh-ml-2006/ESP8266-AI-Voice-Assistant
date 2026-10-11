import socket
import struct
import threading
import speech_recognition as sr
import google.generativeai as genai
import edge_tts
import asyncio
import os
from pydub import AudioSegment

# ============================================================
# API SETUP & CHAT MEMORY 🧠
# ============================================================
API_KEY = "AQ.Ab8RN6KAT2_dfHOvvhOhw8Zg0RyqMOfTObp7pubMLxhL1QBesQ" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-flash-lite-latest")

system_prompt = """
You are a highly intelligent AI voice assistant developed by a 5-member engineering team:
Harsh, Sagnik, Shayan, Shristi, and Santanu.
Keep answers concise, conversational, and suitable for speaking (1-2 lines max).
"""

chat_session = model.start_chat(history=[
    {"role": "user", "parts": [f"System Instructions: {system_prompt}"]},
    {"role": "model", "parts": ["I understand. I am ready to help as the team's AI assistant."]}
])

ai_busy = False

# ============================================================
# TTS - SEND RAW AUDIO TO ESP8266 DAC
# ============================================================
async def play_on_esp8266(text, conn):
    global ai_busy
    output_file = "response.mp3"
    try:
        print("🔊 AI ki aawaz generate ho rahi hai...")
        communicate = edge_tts.Communicate(text, "en-IN-NeerjaNeural")
        await communicate.save(output_file)
        
        audio = AudioSegment.from_mp3(output_file)
        audio = audio + 15  # Volume Boost
        
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        raw_pcm_data = audio.raw_data
        
        print(f"📤 ESP8266 ke Speaker par bhej rahi hu ({len(raw_pcm_data)} bytes)...")
        
        # 👇 FIX: Sleep hata diya. TCP aur ESP8266 apne aap flow control karenge.
        chunk_size = 2048  
        for i in range(0, len(raw_pcm_data), chunk_size):
            conn.sendall(raw_pcm_data[i:i+chunk_size])
            
        print("✅ Speaker par play ho gaya!")
        os.remove(output_file)
    except Exception as e:
        print(f"❌ TTS Error: {e}")
    finally:
        ai_busy = False
        print("\n🎧 Next question ke liye ready hu!")

# ============================================================
# STT & AI LOGIC
# ============================================================
def process_audio(raw_audio_bytes, conn):
    global ai_busy
    print("\n🧠 AI Soch rahi hai...")

    recognizer = sr.Recognizer()
    audio_obj = sr.AudioData(raw_audio_bytes, 16000, 2)

    try:
        text = recognizer.recognize_google(audio_obj, language="en-IN").strip()
        print(f"🗣️ YOU SAID: {text}")
        
        response = chat_session.send_message(text)
        ai_reply = response.text.replace("*", "").replace("#", "")
        print(f"🤖 AI REPLY: {ai_reply}")
        
        asyncio.run(play_on_esp8266(ai_reply, conn))

    except sr.UnknownValueError:
        print("❌ Aawaz theek se samajh nahi aayi, wapas bolo.")
        ai_busy = False
    except Exception as e:
        print(f"❌ Error: {e}")
        ai_busy = False

# ============================================================
# MAIN SERVER (TCP LISTENER)
# ============================================================
HOST = "0.0.0.0"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"\n🚀 FINAL AI SERVER WITH MEMORY STARTED ON PORT {PORT}")

while True:
    conn, addr = server_socket.accept()
    print(f"📡 ESP8266 CONNECTED from {addr}!")

    while True:
        audio_data = bytearray()
        pre_speech_buffer = []  # 👇 FIX: Pehla word cut na ho isliye ye buffer lagaya
        
        silence_threshold = 800  
        silence_chunks = 0
        max_silence_chunks = 50   
        has_started_speaking = False

        while len(audio_data) < (160000 * 4): 
            try:
                packet = conn.recv(2048)
                if not packet: break 
                
                if len(packet) % 2 != 0: packet = packet[:-1]
                if len(packet) == 0: continue

                samples = struct.unpack(f"<{len(packet)//2}h", packet)
                max_amp = max(abs(sample) for sample in samples)

                if ai_busy:
                    continue 

                # 👇 FIX: Recording Logic with Pre-Buffer
                if max_amp > silence_threshold:
                    if not has_started_speaking:
                        print(f"🎙️ Sun rahi hu... (Amp: {max_amp})")
                        has_started_speaking = True
                        # Purana quiet data add kar do taaki shuruati aawaz na kate
                        for p in pre_speech_buffer:
                            audio_data.extend(p)
                    
                    silence_chunks = 0
                    audio_data.extend(packet)
                elif has_started_speaking:
                    silence_chunks += 1
                    audio_data.extend(packet)
                else:
                    # Agar chup ho, toh aakhri ke kuch packets sambhal ke rakho
                    pre_speech_buffer.append(packet)
                    if len(pre_speech_buffer) > 10:
                        pre_speech_buffer.pop(0)

                if has_started_speaking and silence_chunks > max_silence_chunks:
                    print("🛑 Recording khatam. Bhej rahi hu...")
                    break 

            except Exception as e:
                break

        if not packet:
            print("⚠️ Disconnected!")
            break 

        if len(audio_data) > 0 and not ai_busy:
            ai_busy = True 
            threading.Thread(target=process_audio, args=(bytes(audio_data), conn), daemon=True).start()
