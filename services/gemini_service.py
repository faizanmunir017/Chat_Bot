import google.generativeai as genai

class GeminiService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)

    def generate_response(self, prompt: str) -> str:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Failed to generate response: {str(e)}")
