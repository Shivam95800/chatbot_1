import legal_assistant as st
import requests
from pathlib import Path
import speech_recognition as sr
import time
from threading import Thread
import queue
import json
from datetime import datetime
import streamlit.components.v1 as components


st.set_page_config(page_title="Nyyai Astra - Legal AI", layout="wide", initial_sidebar_state="collapsed")



# Initialize session state variables if they are not already set
if "show_main_content" not in st.session_state:
    st.session_state.show_main_content = True  # Main content is visible by default

if "show_profile" not in st.session_state:
    st.session_state.show_profile = False  # Profile page is hidden by default

# # Step 1: Initialize session state for profile modal
# if "show_profile" not in st.session_state:
#     st.session_state.show_profile = False  # Initially hidden

# # Step 2: Define a function to toggle profile modal
# def toggle_profile():
#     st.session_state.show_profile = not st.session_state.show_profile

# # Step 3: Create the Profile Button
# if st.button("Profile"):
#     toggle_profile()

# # Step 4: Show the login form (from login.html) only when profile is toggled ON
# if st.session_state.show_profile:
#     try:
#         # Render the HTML content (login form) only once
#         with open("login.html", "r") as f:
#             login_html = f.read()

#         components.html(login_html, height=1000, scrolling=True)
#     except Exception as e:
#         st.error(f"Error loading login form: {e}")



import legal_assistant as st
import streamlit.components.v1 as components

# Step 1: Initialize session state for profile modal
if "show_profile" not in st.session_state:
    st.session_state.show_profile = False  # Initially hidden

# Step 2: Define a function to toggle profile modal
def toggle_profile():
    st.session_state.show_profile = not st.session_state.show_profile

# Step 3: Create the Profile Button
if st.button("Profile"):
    toggle_profile()

# Step 4: Load the login form in a responsive popup/modal
if st.session_state.show_profile:
    try:
        # Read the HTML file
        with open("login.html", "r", encoding="utf-8") as f:
            login_html = f.read()

        # Apply CSS styles in Streamlit for responsiveness
        modal_style = """
            <style>
                .login-container {
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    width: 90%;
                    max-width: 400px;
                    height: auto;
                    background-color: white;
                    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
                    padding: 20px;
                    border-radius: 10px;
                    z-index: 1000;
                }
                .overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-color: rgba(0, 0, 0, 0.5);
                    z-index: 999;
                }
            </style>
        """
        
        # Wrap the login form inside a modal
        modal_html = f"""
            {modal_style}
            <div class="overlay" onclick="hideModal()"></div>
            <div class="login-container">
                {login_html}
            </div>
            <script>
                function hideModal() {{
                    const modal = document.querySelector('.overlay');
                    if (modal) modal.style.display = 'none';
                }}
            </script>
        """

        # Render the modal inside Streamlit
        components.html(modal_html, height=600, scrolling=False)

    except Exception as e:
        st.error(f"Error loading login form: {e}")

#  def load_auth_css():
#     return """
#     <style>
#     .auth-background {
#         width: 430px;
#         height: 520px;
#         position: relative;
#         margin: 0 auto;
#     }
    
#     .auth-shape {
#         height: 200px;
#         width: 200px;
#         position: absolute;
#         border-radius: 50%;
#     }
    
#     .auth-shape-1 {
#         background: linear-gradient(#1845ad, #23a2f6);
#         left: -80px;
#         top: -80px;
#     }
    
#     .auth-shape-2 {
#         background: linear-gradient(to right, #ff512f, #f09819);
#         right: -30px;
#         bottom: -80px;
#     }
    
#     .auth-form {
#         height: 520px;
#         width: 400px;
#         background-color: rgba(255,255,255,0.13);
#         position: relative;
#         margin: 0 auto;
#         border-radius: 10px;
#         backdrop-filter: blur(10px);
#         border: 2px solid rgba(255,255,255,0.1);
#         box-shadow: 0 0 40px rgba(8,7,16,0.6);
#         padding: 50px 35px;
#     }
    
#     .auth-form * {
#         font-family: 'Poppins',sans-serif;
#         color: #ffffff;
#         letter-spacing: 0.5px;
#         outline: none;
#         border: none;
#     }
    
#     .auth-form h3 {
#         font-size: 32px;
#         font-weight: 500;
#         line-height: 42px;
#         text-align: center;
#         margin-bottom: 30px;
#     }
    
#     .auth-label {
#         display: block;
#         margin-top: 30px;
#         font-size: 16px;
#         font-weight: 500;
#     }
    
#     .auth-input {
#         display: block;
#         height: 50px;
#         width: 100%;
#         background-color: rgba(255,255,255,0.07);
#         border-radius: 3px;
#         padding: 0 10px;
#         margin-top: 8px;
#         font-size: 14px;
#         font-weight: 300;
#         color: #e5e5e5;
#     }
    
#     .auth-button {
#         margin-top: 50px;
#         width: 100%;
#         background-color: #ffffff;
#         color: #080710;
#         padding: 15px 0;
#         font-size: 18px;
#         font-weight: 600;
#         border-radius: 5px;
#         cursor: pointer;
#     }
    
#     .social-login {
#         margin-top: 30px;
#         display: flex;
#         justify-content: center;
#         gap: 25px;
#     }
    
#     .social-btn {
#         width: 150px;
#         border-radius: 3px;
#         padding: 5px 10px 10px 5px;
#         background-color: rgba(255,255,255,0.27);
#         color: #eaf0fb;
#         text-align: center;
#         cursor: pointer;
#         transition: background-color 0.3s;
#     }
    
#     .social-btn:hover {
#         background-color: rgba(255,255,255,0.47);
#     }
    
#     /* Dark overlay for the background */
#     .auth-container {
#         position: fixed;
#         top: 0;
#         left: 0;
#         right: 0;
#         bottom: 0;
#         background-color: rgba(8,7,16,0.9);
#         z-index: 1000;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#     }
#     </style>
#     """

# def show_profile_modal():
#     st.markdown(load_auth_css(), unsafe_allow_html=True)
    
#     if not st.session_state.get('is_logged_in', False):
#         st.markdown("""
#             <div class="auth-container">
#                 <div class="auth-background">
#                     <div class="auth-shape auth-shape-1"></div>
#                     <div class="auth-shape auth-shape-2"></div>
#                     <div class="auth-form">
#                         <h3>Login Here</h3>
#                         <div>
#                             <label class="auth-label">Username</label>
#                             <input type="text" class="auth-input" placeholder="Email or Phone" id="username">
#                         </div>
#                         <div>
#                             <label class="auth-label">Password</label>
#                             <input type="password" class="auth-input" placeholder="Password" id="password">
#                         </div>
#                         <button class="auth-button">Log In</button>
#                         <div class="social-login">
#                             <div class="social-btn">
#                                 <i class="fab fa-google"></i> Google
#                             </div>
#                             <div class="social-btn">
#                                 <i class="fab fa-facebook"></i> Facebook
#                             </div>
#                         </div>
#                     </div>
#                 </div>
#             </div>
#         """, unsafe_allow_html=True)
        
#         # Handle form submission using Streamlit components (hidden)
#         username = st.text_input("", key="username", label_visibility="collapsed")
#         password = st.text_input("", type="password", key="password", label_visibility="collapsed")
        
#         # Add Font Awesome CDN
#         st.markdown("""
#             <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
#             <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;600&display=swap" rel="stylesheet">
#         """, unsafe_allow_html=True)
        
#         if st.button("Submit", key="auth_submit"):
#             # Add your login logic here
#             st.session_state.is_logged_in = True
#             st.session_state.username = username
#             st.rerun()
#     else:
#         st.markdown("""
#             <div class="auth-container">
#                 <div class="auth-form">
#                     <h3>Welcome, {}!</h3>
#                     <button class="auth-button">Logout</button>
#                 </div>
#             </div>
#         """.format(st.session_state.username), unsafe_allow_html=True)
        
#         if st.button("Logout", key="logout"):
#             st.session_state.is_logged_in = False
#             st.session_state.username = None
#             st.rerun()



# def show_profile_modal():
#     # st.markdown(load_auth_css(), unsafe_allow_html=True)  # Load CSS if needed
    
#     if not st.session_state.get('is_logged_in', False):
#         # Embed the external login.html file
#         with st.container():
#             components.html(open("login.html", "r").read(), height=500, scrolling=True)

#         # Capture user input with hidden fields (optional)
#         username = st.text_input("", key="username", label_visibility="collapsed")
#         password = st.text_input("", type="password", key="password", label_visibility="collapsed")

#         # Submit Button (Optional)
#         if st.button("Submit", key="auth_submit"):
#             # Add authentication logic here
#             st.session_state.is_logged_in = True
#             st.session_state.username = username
#             st.rerun()

#     else:
#         st.markdown(f"""
#             <div class="auth-container">
#                 <div class="auth-form">
#                     <h3>Welcome, {st.session_state.username}!</h3>
#                     <button class="auth-button" onclick="logout()">Logout</button>
#                 </div>
#             </div>
#         """, unsafe_allow_html=True)

#         if st.button("Logout", key="logout"):
#             st.session_state.is_logged_in = False
#             st.session_state.username = None
#             st.rerun()


# def show_profile_modal():
#     # Ensure session state exists
#     if "is_logged_in" not in st.session_state:
#         st.session_state.is_logged_in = False

#     if not st.session_state.is_logged_in:
#         # Show the login form (external file)
#         with st.container():
#             st.markdown("<h3>Login</h3>", unsafe_allow_html=True)
#             components.html(open("login.html", "r").read(), height=800, scrolling=True)  

#         # # Hidden input fields for username and password
#         # username = st.text_input("Username", key="username")
#         # password = st.text_input("Password", type="password", key="password")

#         # Submit button for login
#         if st.button("Login"):  
#             # Dummy authentication logic (Replace with actual logic)
#             if username and password:
#                 st.session_state.is_logged_in = True
#                 st.session_state.username = username
#                 st.session_state.show_profile = False  # Hide profile modal after login
#                 st.rerun()
#             else:
#                 st.warning("Please enter both username and password.")
#     else:
#         # Show profile info after login
#         st.markdown(f"""
#             <div style="text-align: center;">
#                 <h3>Welcome, {st.session_state.username}!</h3>
#                 <button class="auth-button" onclick="logout()">Logout</button>
#             </div>
#         """, unsafe_allow_html=True)

#         # Logout button
#         if st.button("Logout"):  # Line 290 (approx)
#             st.session_state.is_logged_in = False
#             st.session_state.username = None
#             st.session_state.show_profile = False  # Hide profile modal
#             st.session_state.show_main_content = True  # Restore main content
#             st.rerun()


# # Show profile modal when "Profile" button is clicked
# if "show_profile_modal" not in st.session_state:
#     st.session_state.show_profile_modal = True

# if st.button("👤 Profile"):
#     st.session_state.show_profile_modal = True

# if st.session_state.show_profile_modal:
#     show_profile_modal()

# Show either profile modal or main content
if st.session_state.show_profile:
 pass
#     # show_profile_modal()
#     pass
# elif st.session_state.show_main_content:
#     # # Your main window content (Ask Legal Query, etc.)
#     # st.markdown("<h2>Ask Legal Query</h2>", unsafe_allow_html=True)  # Line 305 (approx)
#     # user_query = st.text_area("Enter your legal query here:")
#     # if st.button("Submit Query"):
#     #     st.success("Your query has been submitted.")



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
            # Add a button to use the recognized text
            if st.button("Use this text"):
                # Store the text in a temporary session state variable
                st.session_state.temp_search_text = st.session_state.voice_text
                st.session_state.show_voice_modal = False
                st.rerun()
    
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

# Custom CSS with theme support
def load_css():
    return """
    <style>
    /* Dark mode styles */
    [data-theme="dark"] {
        --bg-color: #1E1E1E;
        --text-color: #FFFFFF;
        --card-bg: #2D2D2D;
        --hover-color: #3D3D3D;
    }
    
    /* Light mode styles */
    [data-theme="light"] {
        --bg-color: #FFFFFF;
        --text-color: #1E1E1E;
        --card-bg: #F0F2F6;
        --hover-color: #E6E6E6;
    }
    
    /* Common styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .search-container {
        position: relative;
        margin: 20px auto;
        max-width: 600px;
    }
    
    .search-input {
        width: 100%;
        padding: 12px 45px 12px 15px;
        border: 2px solid var(--card-bg);
        border-radius: 10px;
        font-size: 16px;
        transition: all 0.3s ease;
        background: var(--bg-color);
        color: var(--text-color);
    }
    
    .search-input:focus {
        border-color: #0f5132;
        box-shadow: 0 0 0 3px rgba(15, 81, 50, 0.2);
    }
    
    .voice-button {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        background: none;
        border: none;
        cursor: pointer;
        font-size: 20px;
        color: var(--text-color);
    }
    
    .search-button {
        display: block;
        margin: 15px auto;
        padding: 12px 30px;
        background-color: #0f5132;
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .search-button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(15, 81, 50, 0.2);
    }
    
    .result-card {
        background: var(--card-bg);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(15, 81, 50, 0.3);
        border-radius: 50%;
        border-top-color: #0f5132;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Feedback buttons */
    .feedback-buttons {
        display: flex;
        gap: 10px;
        justify-content: flex-end;
        margin-top: 10px;
    }
    
    .feedback-button {
        padding: 5px 10px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .feedback-button:hover {
        transform: scale(1.1);
    }
    </style>
    """

def initialize_autocomplete():
    """Initialize autocomplete suggestions"""
    return [
        "Indian Constitution Article",
        "Supreme Court judgments",
        "Legal rights in India",
        "Criminal procedure code",
        "Civil procedure code",
        "Legal documentation",
        # Add more suggestions
    ]

def show_search_interface():
    """Main search interface with autocomplete"""
    st.markdown(load_css(), unsafe_allow_html=True)
    
    # Theme toggle
    col1, col2 = st.columns([6, 1])
    
    with col2:
        if st.button("Dark Mode"):
                
            if st.toggle("🌗 Dark Mode", value=st.session_state.dark_mode):
                st.session_state.dark_mode = True
            else:
                st.session_state.dark_mode = False
        
    # Search container
    search_container = st.container()
    with search_container:
        # Autocomplete search
        query = st.text_input(
            "",
            placeholder="Enter your legal query here...",
            key="search_input"
        )
        
        # Show autocomplete suggestions
        if query:
            suggestions = [s for s in initialize_autocomplete() if query.lower() in s.lower()]
            if suggestions:
                selected_suggestion = st.selectbox("Suggestions:", suggestions)
                if selected_suggestion != query:
                    st.session_state.search_input = selected_suggestion
                    st.rerun()
        
        # Search button with animation
        if st.button("Search", key="search_button"):
            with st.spinner("Fetching results..."):
                time.sleep(1)  # Simulate search delay
                show_search_results(query)

def show_search_results(query):
    """Display search results in tabs"""
    # Add to search history
    if query:
        st.session_state.search_history.append({
            "query": query,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # Create tabs for different result categories
    tab1, tab2, tab3 = st.tabs(["Case Laws", "Acts", "Amendments"])
    
    with tab1:
        show_result_card(
            "Case Law Result",
            "Sample case law content...",
            "case_law_1"
        )
    
    with tab2:
        show_result_card(
            "Act Result",
            "Sample act content...",
            "act_1"
        )
    
    with tab3:
        show_result_card(
            "Amendment Result",
            "Sample amendment content...",
            "amendment_1"
        )

def show_result_card(title, content, result_id):
    """Display a single result card with feedback buttons"""
    with st.container():
        st.markdown(f"""
            <div class="result-card">
                <h3>{title}</h3>
                <p>{content}</p>
                <div class="feedback-buttons">
                    <button class="feedback-button" onclick="feedback('{result_id}', 'up')">👍</button>
                    <button class="feedback-button" onclick="feedback('{result_id}', 'down')">👎</button>
                </div>
            </div>
        """, unsafe_allow_html=True)

def show_bookmarks():
    """Display bookmarked searches"""
    st.subheader("📌 Bookmarks")
    for bookmark in st.session_state.bookmarks:
        with st.expander(bookmark["query"]):
            st.write(f"Saved on: {bookmark['timestamp']}")
            if st.button("Remove", key=f"remove_{bookmark['timestamp']}"):
                st.session_state.bookmarks.remove(bookmark)
                st.rerun()

def show_history():
    """Display search history"""
    st.subheader("📜 Search History")
    for item in reversed(st.session_state.search_history[-10:]):
        with st.expander(item["query"]):
            st.write(f"Searched on: {item['timestamp']}")
            if st.button("Bookmark", key=f"bookmark_{item['timestamp']}"):
                st.session_state.bookmarks.append(item)
                st.rerun()

def main():
    # # Apply theme
    # theme = "dark" if st.session_state.dark_mode else "light"
    # st.markdown(f'<div data-theme="{theme}">', unsafe_allow_html=True)
    
    # Initialize session states
    if 'show_main_content' not in st.session_state:
        st.session_state.show_main_content = True
    if 'show_voice_modal' not in st.session_state:
        st.session_state.show_voice_modal = False
    if 'voice_text' not in st.session_state:
        st.session_state.voice_text = ""
    if 'temp_search_text' not in st.session_state:
        st.session_state.temp_search_text = ""

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
    # with col_profile:
    #     if st.button(" 👤 Profile ",key="duplicate"):
    #         st.session_state.show_profile = True
    #         st.session_state.show_main_content = False
    #         st.rerun()
    
    # Show either profile modal or main content
    if st.session_state.get('show_profile', False):
        # with st.container():
        #     show_profile_modal()
        #     if st.button("Close"):
        #         st.session_state.show_profile = False
        #         st.session_state.show_main_content = True
        #         st.rerun()
        pass
    
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
            # Use the temporary search text if available
            initial_value = st.session_state.temp_search_text if st.session_state.temp_search_text else ""
            if initial_value:
                st.session_state.temp_search_text = ""  # Clear the temporary text
                
            user_input = st.text_input(
                label="Search",
                placeholder="Enter your legal query here...",
                key="search_input",
                value=initial_value,
                label_visibility="collapsed"
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
