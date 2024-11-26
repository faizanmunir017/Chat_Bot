

#Assistant API:
from dotenv import load_dotenv
from openai import OpenAI


print("Assistant API testing: ")

load_dotenv()
client = OpenAI()


try:
    with open("water.pdf", "rb") as file:
        uploaded_file = client.files.create(
            file=file,
            purpose="assistants"
        )
    print(f"File uploaded successfully! File ID: {uploaded_file.id}")

except FileNotFoundError:
    print("Error: The file 'water.pdf' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

try:
    assistant = client.beta.assistants.create(
        name="Document Reader",
        description="You are given a PDF document. Answer questions based on the material in the document only.",
        model="gpt-4o-mini",
        tools=[{"type": "file_search"}], 
    )
    print(f"Assistant created successfully! Assistant ID: {assistant.id}")
except Exception as e:
    print(f"Error creating assistant: {e}")
    exit()



user_input="Write a 1 or 2 lines overview of the document given to u."

try:
    thread = client.beta.threads.create(
        messages=[{
            "role": "user",
            "content": user_input,
            "attachments": [{
                "file_id": uploaded_file.id,
                "tools": [{"type": "file_search"}] 
            }]
        }]
    )
    print(f"Thread created successfully! Thread ID: {thread.id}")
except Exception as e:
    print(f"Error creating thread and sending message: {e}")
    exit()

    

try:
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Answer the user's question based on the material in the attached PDF document."

    )

    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print("Messages retrieved successfully!")
        for message in messages.data:
            if message.role == "assistant":
                assistant_content = message.content[0].text.value
                print(f"Assistant Role: {message.role}")
                print(f"Assistant Response: {assistant_content}")
    else:
        print(f"Run status: {run.status}")

except Exception as e:
    print(f"Error running assistant: {e}")