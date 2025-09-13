import legal_assistant as st
import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

# Load environment variables
load_dotenv()
endpoint = "https://models.inference.ai.azure.com"
model_name = "mistral-small-2503"
token = os.getenv("GITHUB_TOKEN")

# Initialize chat client
client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(token))

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage("You are a helpful assistant.")]

# Page title
st.set_page_config(page_title="Nyyai Astra", page_icon="⚖️")
st.title("🤖 Nyyai Astra - Ask me anything about Indian Law")

# Input box
user_input = st.text_input("Type your question here 👇", placeholder="e.g. explain Article 19 of Indian Constitution")

# On input submit
if st.button("Ask"):
    if user_input.strip():
        st.session_state.messages.append(UserMessage(user_input))

        with st.spinner("Thinking..."):
            response = client.complete(
                messages=st.session_state.messages,
                temperature=1.0,
                top_p=1.0,
                max_tokens=1000,
                model=model_name
            )

        reply = response.choices[0].message.content
        st.session_state.messages.append(AssistantMessage(reply))

# Display conversation
st.markdown("### 🧠 Chat History")
for msg in st.session_state.messages[1:]:  # Skip system message
    if isinstance(msg, UserMessage):
        st.markdown(f"**👤 You:** {msg.content}")
    elif isinstance(msg, AssistantMessage):
        st.markdown(f"**🤖 Nyyai Astra:** {msg.content}")
