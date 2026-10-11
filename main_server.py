import struct
import threading
import asyncio

# Apne teammates ke code ko import kar rahe hain
from network_socket import setup_server
from ai_prompt_engine import initialize_chat
from audio_to_text import convert_audio_to_text
from text_to_speech_engine import generate_and_send_audio

# 1. AI Chat Session chalu karna
chat_session = initialize_chat()
ai_busy = False

# 2. Main Processing Thread
def process_audio(raw_audio_bytes, conn):
    global ai_busy
    print("\n🧠 AI Soch rahi hai...")
    
    text = convert_audio_to_text(raw_audio_bytes)
    
    if text:
        print(f"🗣️ YOU SAID: {text}")
        response = chat_session.send_message(text)
        ai_reply = response.text.replace("*", "").replace("#", "")
        print(f"🤖 AI REPLY: {ai_reply}")
        
        asyncio.run(generate_and_send_audio(ai_reply, conn))
    else:
        print("❌ Aawaz theek se nahi aayi, wapas try karo.")
        
    ai_busy = False
    print("\n🎧 Next question ke liye ready hu!")

# 3. Server Setup aur Listen Loop
server_socket = setup_server()

while True:
    conn, addr = server_socket.accept()
    print(f"📡 ESP8266 CONNECTED from {addr}!")

    while True:
        audio_data = bytearray()
        
        silence_threshold = 1500  
        silence_chunks = 0
        max_silence_chunks = 250   
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

                if max_amp > silence_threshold:
                    if not has_started_speaking:
                        print(f"🎙️ Sun rahi hu... (Amp: {max_amp})")
                    has_started_speaking = True
                    silence_chunks = 0
                    audio_data.extend(packet)
                elif has_started_speaking:
                    silence_chunks += 1
                    audio_data.extend(packet)

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
