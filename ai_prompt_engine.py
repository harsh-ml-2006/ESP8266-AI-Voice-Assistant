import google.generativeai as genai

def initialize_chat():
    API_KEY = "AQ.Ab8RN6LvGAMmjHSuBooxnvIRFMZxgmMzueEVRJciAfj3Wc9G9A" 
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
    return chat_session
