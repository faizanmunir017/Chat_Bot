import openai
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client=OpenAI()


def chat_with_gpt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": "."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = chat_with_gpt(user_input)
        print(f"GPT: {response}") 