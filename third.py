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

# Add this CSS at the beginning of your main function or after st.set_page_config
st.markdown("""
    <style>
        /* Custom styling for the text input */
        div[data-baseweb="textarea"] textarea {
            min-height: 110px !important;  /* Initial height */
            max-height: 200px !important;  /* Maximum height (about 4 lines) */
            width: 100% !important;
            font-size: 16px !important;
            padding: 10px 15px !important;
            border-radius: 25px !important;
            background-color: #2D2D2D !important;
            color: white !important;
            border: 1px solid #3D3D3D !important;
            transition: all 0.3s ease !important;
            overflow-y: auto !important;  /* Enable vertical scrolling */
            resize: none !important;  /* Disable manual resizing */
            line-height: 1.5 !important;
        }
        
        /* Container styling */
        div[data-baseweb="textarea"] {
            width: 100% !important;
            margin: 10px 0 !important;
            background-color: #2D2D2D !important;
            border-radius: 25px !important;
        }
        
        /* Rainbow border effect on focus */
        div[data-baseweb="textarea"] textarea:focus {
            border: 2px solid transparent !important;
            background-image: linear-gradient(#2D2D2D, #2D2D2D),
                            linear-gradient(90deg, 
                                #ff0000, #ff8000, 
                                #ffff00, #00ff00, 
                                #00ffff, #0000ff, 
                                #8000ff, #ff0080) !important;
            background-origin: border-box !important;
            background-clip: padding-box, border-box !important;
            animation: rainbow 3s linear infinite !important;
        }
        
        /* Scrollbar styling */
        div[data-baseweb="textarea"] textarea::-webkit-scrollbar {
            width: 8px !important;
        }
        
        div[data-baseweb="textarea"] textarea::-webkit-scrollbar-track {
            background: #2D2D2D !important;
            border-radius: 4px !important;
        }
        
        div[data-baseweb="textarea"] textarea::-webkit-scrollbar-thumb {
            background: #4D4D4D !important;
            border-radius: 4px !important;
        }
        
        /* Placeholder text color */
        div[data-baseweb="textarea"] textarea::placeholder {
            color: #808080 !important;
        }
        
        @keyframes rainbow {
            0% { filter: hue-rotate(0deg); }
            100% { filter: hue-rotate(360deg); }
        }

        /* Profile button positioning */
        .stButton.profile-button {
            position: absolute;
            top: 20px;  /* Adjust this value to move up/down */
            right: 20px;  /* Distance from right edge */
            z-index: 1000;
        }

        /* Results section positioning */
        .results-section {
            margin-top: 0 !important;  /* Remove top margin */
            padding-top: 20px !important;  /* Add some padding at top */
            border-top: 1px solid #333;  /* Optional: adds a line at top */
        }

        /* Fixed search bar at bottom */
        .fixed-bottom {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: #0E1117;
            padding: 20px;
            border-top: 1px solid #333;
            z-index: 1000;
        }

        /* Main content spacing */
        .main-content {
            margin-bottom: 180px;  /* Space for fixed search bar */
            margin-top: 0;  /* Remove top margin */
        }
    </style>
""", unsafe_allow_html=True)




def handle_file_upload():
    st.markdown("<h2 style='text-align: center;'>File Upload</h2>", unsafe_allow_html=True)
    
    # Create three columns for different file types
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("##### Documents")
        docs = st.file_uploader("Upload Documents", 
            type=['pdf', 'doc', 'docx', 'txt'],
            accept_multiple_files=True,
            key='doc_uploader'
        )
        if docs:
            for doc in docs:
                st.success(f"Uploaded: {doc.name}")
    
    with col2:
        st.markdown("##### Images")
        images = st.file_uploader("Upload Images",
            type=['png', 'jpg', 'jpeg', 'gif'],
            accept_multiple_files=True,
            key='image_uploader'
        )
        if images:
            for img in images:
                st.success(f"Uploaded: {img.name}")
    
    with col3:
        st.markdown("##### Other Files")
        other_files = st.file_uploader("Upload Other Files",
            type=['csv', 'xlsx', 'zip', 'rar'],
            accept_multiple_files=True,
            key='other_uploader'
        )
        if other_files:
            for file in other_files:
                st.success(f"Uploaded: {file.name}")

    # Add some styling for the upload sections
    st.markdown("""
        <style>
        .uploadedFile {
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 10px;
            margin: 5px 0;
            background-color: #f8f9fa;
        }
        .stButton>button {
            width: 100%;
        }
        .upload-header {
            text-align: center;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Add a divider
    st.markdown("---")

    # Display upload instructions
    st.markdown("""
        #### Upload Instructions:
        1. Select the appropriate category for your file
        2. Click 'Browse files' or drag and drop files
        3. Multiple files can be uploaded at once
        4. Maximum file size: 200MB per file
    """)

# Initialize session states
def init_session_states():
    defaults = {
        'show_main_content': True,
        'show_profile': False,
        'show_voice_modal': False,
        'voice_text': "",
        'temp_search_text': "",
        'search_history': [],
        'bookmarks': [],
        'is_search_active': False,
        'current_query': ""
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
    st.set_page_config(page_title="Nyyai Astra", layout="wide")

    apply_custom_css()
    initialize_session_state()

    with st.sidebar:
        st.title("🔍 Nyyai Astra")
        st.markdown("---")
        show_user_profile()
        st.markdown("---")
        show_search_history()

    is_search_active = st.session_state.is_search_active

    with st.container():
        # Split layout into sections
        header_area = st.empty()
        results_area = st.empty()
        search_area = st.container()

        # When there's no search yet, show welcome text
        if not is_search_active:
            with header_area:
                st.markdown("<h1 style='text-align: center;'>🧠 Nyyai Astra</h1>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center;'>Your AI Legal Assistant</p>", unsafe_allow_html=True)

        # Search input at the bottom
        with search_area:
            st.markdown('<div class="fixed-bottom">', unsafe_allow_html=True)
            search_input = st.text_area(
                "Ask your legal question",
                key="search_textarea",
                on_change=handle_key_press,
                placeholder="Eg. What is Article 21?"
            )
            st.markdown('</div>', unsafe_allow_html=True)

        # When search is active, display results
        if st.session_state.is_search_active:
            with results_area:
                st.markdown('<div class="results-section">', unsafe_allow_html=True)
                response = search_legal_query(st.session_state.temp_search_text)
                show_search_results(response)
                st.markdown('</div>', unsafe_allow_html=True)
