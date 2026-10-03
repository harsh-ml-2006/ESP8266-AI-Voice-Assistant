import google.generativeai as genai

API_KEY = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-3.6-flash")

system_prompt = """
You are an AI voice assistant developed by: Harsh, Sagnik, Shayan, Shristi, and Santanu.
Greet 'CN Sir' if asked for an introduction. Keep responses concise.
"""



def get_ai_response(user_query):
    print("Sending query to Gemini API...")
    final_prompt = system_prompt + "\nUser: " + user_query
    
    try:
        response = model.generate_content(final_prompt)
        print("AI Output:", response.text)
        return response.text
    except Exception as e:
        print(f"Error fetching response: {e}")
        return ""
