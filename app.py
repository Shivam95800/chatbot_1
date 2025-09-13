import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

# Load .env file
load_dotenv()

endpoint = "https://models.inference.ai.azure.com"
model_name = "mistral-small-2503"
token = os.getenv("GITHUB_TOKEN")

# Setup client
client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

# Initial system message
messages = [SystemMessage("You are a helpful assistant.")]

print("🤖 Nyyai Astra: Hello! Ask me anything. Type 'exit' to stop.")

# Loop for real-time chat
while True:
    user_input = input("👤 You: ")
    
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("🤖 Nyyai Astra: Bye! Take care 🐧")
        break

    messages.append(UserMessage(user_input))

    response = client.complete(
        messages=messages,
        temperature=1.0,
        top_p=1.0,
        max_tokens=1000,
        model=model_name
    )

    reply = response.choices[0].message.content
    print(f"🤖 Nyyai Astra: {reply}")

    messages.append(AssistantMessage(reply))  # Add bot reply to history

    import json


