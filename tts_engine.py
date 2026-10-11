import edge_tts
import asyncio
import os
from pydub import AudioSegment

async def generate_and_send_audio(text, conn):
    output_file = "response.mp3"
    try:
        print("🔊 AI ki aawaz generate ho rahi hai...")
        communicate = edge_tts.Communicate(text, "en-IN-NeerjaNeural")
        await communicate.save(output_file)
        
        audio = AudioSegment.from_mp3(output_file)
        audio = audio + 15  # Volume Boost (15 dB)
        
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        raw_pcm_data = audio.raw_data
        
        print(f"📤 ESP8266 ke Speaker par bhej rahi hu ({len(raw_pcm_data)} bytes)...")
        
        chunk_size = 2048  
        for i in range(0, len(raw_pcm_data), chunk_size):
            conn.sendall(raw_pcm_data[i:i+chunk_size])
            await asyncio.sleep(0.06)  
            
        print("✅ Speaker par play ho gaya!")
        os.remove(output_file)
    except Exception as e:
        print(f"❌ TTS Error: {e}")
