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

# Add CSS for profile button positioning
st.markdown("""
    <style>
        /* Profile button positioning */
        .stButton.profile-button {
            position: absolute;
            top: 20px;  /* Adjust this value to move up/down */
            right: 20px;  /* Distance from right edge */
            z-index: 1000;
        }
        
        /* Container for profile button */
        .profile-button-container {
            position: absolute;
            top: 0.5rem;
            right: 3rem;
            z-index: 1000;
        }
    </style>
""", unsafe_allow_html=True)

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
    
    # Profile Button using a container
    # This button is positioned outside the normal flow with CSS
    st.markdown('<div class="profile-button-container">', unsafe_allow_html=True)
    if st.button("👤 Profile", key="profile_btn"):
        st.session_state.show_profile = not st.session_state.show_profile
        st.session_state.show_main_content = not st.session_state.show_main_content
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content area
    if st.session_state.show_main_content:
        # Your main content here
        st.write("Main content goes here")
    
    # Profile content
    if st.session_state.show_profile:
        # Your profile page content here
        st.write("Profile content goes here")
        
        # Add a back button
        if st.button("← Back to Main"):
            st.session_state.show_profile = False
            st.session_state.show_main_content = True
            st.rerun()

if __name__ == "__main__":
    main()