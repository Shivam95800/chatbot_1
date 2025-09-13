import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Load .env file
load_dotenv()
token = os.getenv("GITHUB_TOKEN")

# Check if token is loaded
if not token:
    messagebox.showerror("Error", "GitHub token not found in environment!")
    exit()

# Azure AI setup
endpoint = "https://models.inference.ai.azure.com"
model_name = "mistral-small-2503"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

# GUI App
def send_query():
    user_input = entry_box.get("1.0", tk.END).strip()
    if not user_input:
        return

    try:
        response = client.complete(
            messages=[
                SystemMessage("You are a helpful AI assistant for Indian legal queries."),
                UserMessage(user_input)
            ],
            temperature=0.7,
            top_p=1.0,
            max_tokens=1000,
            model=model_name
        )
        answer = response.choices[0].message.content
        output_box.config(state=tk.NORMAL)
        output_box.insert(tk.END, f"\n👤 You: {user_input}\n🤖 AI: {answer}\n")
        output_box.config(state=tk.DISABLED)
        output_box.yview(tk.END)
        entry_box.delete("1.0", tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")

# Main GUI window
root = tk.Tk()
root.title("Nyyai Astra ⚖️ - Legal AI Assistant")
root.geometry("700x500")
root.resizable(False, False)

entry_box = tk.Text(root, height=4, font=("Arial", 12))
entry_box.pack(padx=10, pady=(10, 0), fill=tk.X)

send_button = tk.Button(root, text="Send", font=("Arial", 12, "bold"), bg="#2b9348", fg="white", command=send_query)
send_button.pack(pady=5)

output_box = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD, font=("Consolas", 11))
output_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
