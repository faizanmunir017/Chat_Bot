import openai

class ChatService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key

    def chat_with_gpt(self, prompt: str) -> str:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "I am a helpful AI chatbot."},
                    {"role": "user", "content": prompt},
                ],
            )
            print("hello there: ",response)
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {e}")
