import legal_assistant as st
import requests
from pathlib import Path
import speech_recognition as sr
import time
from threading import Thread
import queue

st.set_page_config(page_title="Nyyai Astra - Legal AI", layout="centered")

# Initialize session state for voice recording
if 'voice_recording' not in st.session_state:
    st.session_state.voice_recording = False
if 'voice_text' not in st.session_state:
    st.session_state.voice_text = ""

def query_indian_kanoon(search_query):
    # Placeholder function for API integration (modify when you get API access)
    return f"Results for: {search_query}\n\n(Sample response from Indian Kanoon)"

def handle_login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Add your login logic here
        st.session_state.is_logged_in = True
        st.session_state.username = username
        st.rerun()

def handle_signup():
    st.subheader("Sign Up")
    new_username = st.text_input("Choose Username")
    new_password = st.text_input("Choose Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Sign Up"):
        if new_password == confirm_password:
            # Add your signup logic here
            st.success("Account created successfully! Please login.")
        else:
            st.error("Passwords don't match!")

def show_profile_modal():
    if not st.session_state.get('is_logged_in', False):
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            handle_login()
        with tab2:
            handle_signup()
    else:
        st.subheader(f"Welcome, {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.is_logged_in = False
            st.session_state.username = None
            st.rerun()

def handle_file_upload():
    st.subheader("Upload Legal Documents")
    uploaded_files = st.file_uploader(
        "Choose your files", 
        accept_multiple_files=True,
        type=['pdf', 'docx', 'txt']
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Create uploads directory if it doesn't exist
            Path("uploads").mkdir(exist_ok=True)
            
            # Save the file
            bytes_data = uploaded_file.read()
            file_path = f"uploads/{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(bytes_data)
            
            st.success(f"File '{uploaded_file.name}' uploaded successfully!")
            
            # Display file info
            file_stats = {
                "Filename": uploaded_file.name,
                "File type": uploaded_file.type,
                "File size": f"{round(len(bytes_data)/1024, 2)} KB"
            }
            
            st.json(file_stats)

def listen_for_speech(result_queue):
    """Background thread function for voice recognition"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            result_queue.put(("success", text))
        except sr.UnknownValueError:
            result_queue.put(("error", "Could not understand audio"))
        except sr.RequestError:
            result_queue.put(("error", "Could not request results from speech recognition service"))

def show_voice_search_modal():
    """Modal for voice search with better UI"""
    st.subheader("Voice Search 🎤")
    
    col1, col2 = st.columns([3,1])
    
    with col1:
        st.markdown("""
            <div style="padding: 20px; border-radius: 10px; background-color: #f0f2f6;">
                <p>🎙️ Speak your legal query...</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Show recognized text
        if st.session_state.voice_text:
            st.text_area("Recognized Text:", st.session_state.voice_text, height=100)
    
    with col2:
        if not st.session_state.voice_recording:
            if st.button("Start", type="primary"):
                st.session_state.voice_recording = True
                st.session_state.voice_text = ""
                st.rerun()
        else:
            if st.button("Stop", type="secondary"):
                st.session_state.voice_recording = False
                st.rerun()

    # Handle voice recording
    if st.session_state.voice_recording:
        result_queue = queue.Queue()
        thread = Thread(target=listen_for_speech, args=(result_queue,))
        thread.start()
        
        with st.spinner("Listening..."):
            thread.join()
            try:
                result_type, result_value = result_queue.get_nowait()
                if result_type == "success":
                    st.session_state.voice_text = result_value
                    st.session_state.voice_recording = False
                    # Update the search input with the voice text
                    st.session_state.search_input = result_value
                    st.rerun()
                else:
                    st.error(result_value)
                    st.session_state.voice_recording = False
            except queue.Empty:
                st.error("No speech detected")
                st.session_state.voice_recording = False

def search_legal_query(query):
    """Function to handle the search operation"""
    with st.spinner('Searching...'):
        # Simulate search delay
        time.sleep(2)
        # Add your actual search logic here
        return f"Search results for: {query}"

def main():
    # Add custom CSS for search box and buttons
    st.markdown("""
        <style>
        .stButton button:hover {
            background-color: #0f5132 !important;
            border-color: #0f5132 !important;
            color: white !important;
        }
        /* Hide the default label */
        .search-label {
            display: none !important;
        }
        /* Style for search buttons container */
        .search-buttons {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 10px;
        }
        .voice-modal {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 1000;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session states
    if 'show_main_content' not in st.session_state:
        st.session_state.show_main_content = True
    if 'show_voice_modal' not in st.session_state:
        st.session_state.show_voice_modal = False
    if 'search_input' not in st.session_state:
        st.session_state.search_input = ""

    # Add sidebar
    with st.sidebar:
        st.title("Legal Resources")
        st.markdown("---")
        
        if st.button("Indian Constitution", use_container_width=True):
            st.session_state.current_page = "constitution"
            
        if st.button("Today's Supreme Court Hearings", use_container_width=True):
            st.session_state.current_page = "sc_hearings"
            
        if st.button("Amendments", use_container_width=True):
            st.session_state.current_page = "amendments"
            
        if st.button("History", use_container_width=True):
            st.session_state.current_page = "history"
    
    # Add profile button in top right
    col_space, col_profile = st.columns([4, 1])
    with col_profile:
        if st.button("👤 Profile"):
            st.session_state.show_profile = True
            st.session_state.show_main_content = False
            st.rerun()
    
    # Show either profile modal or main content
    if st.session_state.get('show_profile', False):
        with st.container():
            show_profile_modal()
            if st.button("Close"):
                st.session_state.show_profile = False
                st.session_state.show_main_content = True
                st.rerun()
    
    # Main content
    elif st.session_state.show_main_content:
        st.markdown("""
            <div style="text-align: center;">
                <h1>⚖️</h1>
                <h1>Nyyai Astra</h1>
                <h3>An AI-powered assistant for Indian legal queries.</h3>
            </div>
        """, unsafe_allow_html=True)

        # Create search container
        with st.container():
            # Search input with placeholder text
            user_input = st.text_input(
                label="Search",  # This will be hidden by CSS
                placeholder="Enter your legal query here...",
                key="search_input",
                value=st.session_state.search_input,
                label_visibility="collapsed"  # This hides the label
            )
            
            # Search buttons centered below the input
            col1, col2, col3 = st.columns([4, 1, 1])
            with col2:
                if st.button("🔍 Search"):
                    if user_input:
                        search_results = search_legal_query(user_input)
                        st.write(search_results)
            with col3:
                if st.button("🎤 Voice"):
                    st.session_state.show_voice_modal = True
                    st.rerun()

        # Show voice search modal
        if st.session_state.show_voice_modal:
            show_voice_search_modal()
            if st.button("Close Voice Search"):
                st.session_state.show_voice_modal = False
                st.session_state.voice_recording = False
                st.rerun()

        # Show search results
        if user_input:
            st.markdown("---")
            st.subheader("Search Results")
            with st.spinner("Searching..."):
                # Add your search results display logic here
                st.write(f"Showing results for: {user_input}")

if __name__ == "__main__":
    main()
