from openai import OpenAI

class ChatService:
    def __init__(self, api_key: str):
       
        self.client=OpenAI()

    def chat_with_gpt(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  
                messages=[
                    {"role": "system", "content": "I am a helpful AI chatbot."},
                    {"role": "user", "content": prompt},
                ],
            )
            print("Response received: ", response)
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            raise Exception(f"OpenAI API error: {e}")
