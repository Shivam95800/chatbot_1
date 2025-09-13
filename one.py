import legal_assistant as st
import streamlit.components.v1 as components
from pathlib import Path
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Nyyai Astra - Legal AI", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        /* Custom styling for the text input */
        div[data-baseweb="input"] input {
            height: 100px !important;  /* Changed to 70px */
            width: 33.33% !important;  /* One-third of screen width */
            font-size: 16px !important;
            padding: 10px 15px !important;
            border-radius: 25px !important;
            background-color: #2D2D2D !important;
            color: white !important;
            border: 1px solid #3D3D3D !important;
        }
        
        /* Container styling */
        div[data-baseweb="input"] {
            width: 33.33% !important;  /* One-third of screen width */
            margin: 10px auto !important;  /* Added auto for horizontal centering */
            background-color: #2D2D2D !important;
            border-radius: 25px !important;
        }
        
        /* Placeholder text color */
        div[data-baseweb="input"] input::placeholder {
            color: #808080 !important;
        }
        
        /* Make sure styles are applied */
        .stTextInput > div > div > input {
            height: 100px !important;  /* Changed to 70px */
            font-size: 16px !important;
            background-color: #2D2D2D !important;
        }
    </style>
""", unsafe_allow_html=True)




# Initialize session states
def init_session_states():
    defaults = {
        'show_main_content': True,
        'show_profile': False,
        'show_voice_modal': False,
        'voice_text': "",
        'temp_search_text': "",
        'search_history': [],
        'bookmarks': []
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Profile Modal Component
def handle_profile_modal():
    try:
        with open("login.html", "r", encoding="utf-8") as f:
            login_html = f.read()

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

        components.html(modal_html, height=600, scrolling=False)

    except Exception as e:
        st.error(f"Error loading login form: {e}")

# Search functionality
def search_legal_query(query):
    """Handle search operations"""
    with st.spinner('Searching...'):
        time.sleep(1)  # Simulate search delay
        # Add actual search logic here
        return f"Search results for: {query}"

def show_search_results(query):
    """Display search results in organized tabs"""
    if query:
        st.session_state.search_history.append({
            "query": query,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    tab1, tab2, tab3 = st.tabs(["Case Laws", "Acts", "Amendments"])
    
    for tab, (title, content) in zip(
        [tab1, tab2, tab3],
        [
            ("Case Law", "Sample case law content..."),
            ("Act", "Sample act content..."),
            ("Amendment", "Sample amendment content...")
        ]
    ):
        with tab:
            with st.container():
                st.markdown(f"""
                    <div class="result-card">
                        <h3>{title}</h3>
                        <p>{content}</p>
                        <div class="feedback-buttons">
                            <button>👍</button>
                            <button>👎</button>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

# Main application
def main():
    init_session_states()
    
    # Sidebar
    with st.sidebar:
        st.title("Legal Resources")
        st.markdown("---")
        
        sidebar_options = [
            "Indian Constitution",
            "Today's Supreme Court Hearings",
            "Amendments",
            "History"
        ]
        
        for option in sidebar_options:
            if st.button(option, use_container_width=True):
                st.session_state.current_page = option.lower().replace(" ", "_")
    
    # Profile Button
    _, col_profile = st.columns([4, 1])
    with col_profile:
        if st.button("👤 Profile"):
            # Toggle between profile and main content
            st.session_state.show_profile = not st.session_state.show_profile
            st.session_state.show_main_content = not st.session_state.show_main_content
            st.rerun()
    
    # Handle Profile Modal
    if st.session_state.show_profile:
        handle_profile_modal()
    
    # Main Content
    elif st.session_state.show_main_content:
        st.markdown("""
            <div style="text-align: center;">
                <h1>⚖️</h1>
                <h1>Nyyai Astra</h1>
                <h3>An AI-powered assistant for Indian legal queries.</h3>
            </div>
        """, unsafe_allow_html=True)

        # Search Interface
        with st.container():
            search_query = st.text_input(
                label="Search",
                placeholder="Enter your legal query here...",
                value=st.session_state.temp_search_text,
                label_visibility="collapsed"
            )
            st.session_state.temp_search_text = ""
            
            col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
            with col2:
                if st.button("🔍 Search") and search_query:
                    show_search_results(search_query)
            with col3:
                if st.button("🎤 Voice"):
                    st.session_state.show_voice_modal = True
                    st.rerun()
            with col4:
                if st.button("📎 Upload"):
                    st.session_state.show_main_content = False
                    st.session_state.show_profile = False
                    st.session_state.show_upload = True
                    st.rerun()

    # Handle File Upload Section when show_upload is True
    if st.session_state.get('show_upload', False):
        handle_file_upload()
        # Add a back button to return to main content
        if st.button("← Back"):
            st.session_state.show_upload = False
            st.session_state.show_main_content = True
            st.rerun()

if __name__ == "__main__":
    main()
