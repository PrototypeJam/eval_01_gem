import streamlit as st

from modules.api_config import render_api_key_tab
from modules.model_config import render_model_config_tab
from modules.script1_chat import render_chat_tab
from modules.script2_placeholder import render_script2_tab
from modules.scriptN_placeholder import render_scriptN_tab

# --- Page Configuration ---
st.set_page_config(
    page_title="Modular Multi-Tab Streamlit App",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Main Application ---
st.title("🧩 Modular Multi-Tab AI Application")
st.caption(
    "A starter project for building Streamlit apps with multiple, independent Python scripts."
)

# --- Initialize Session State ---
# We do this at the top level if certain states are shared or need to be checked globally
# Individual modules also manage their own session states as needed.
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = st.secrets.get("OPENAI_API_KEY", "")

# --- Tab Creation ---
tab_titles = [
    "1. API Key",
    "2. Model Config",
    "3. Python Script 1 (Chat)",
    "4. Python Script 2",
    "5. Python Script N",
]

tab1, tab2, tab3, tab4, tab5 = st.tabs(tab_titles)

with tab1:
    render_api_key_tab()

with tab2:
    render_model_config_tab()

with tab3:
    render_chat_tab()

with tab4:
    render_script2_tab()

with tab5:
    render_scriptN_tab()

# --- Footer or Common Elements (Optional) ---
st.sidebar.markdown("---")
st.sidebar.info(
    "This is a starter app demonstrating modular design with tabs. "
    "Each tab can host a distinct Python script or functionality."
)
st.sidebar.markdown(
    """
    **How to Expand:**
    1. Create a new `.py` file in the `modules/` directory.
    2. Define a `render_yourscript_tab()` function in it.
    3. Import it in `app.py`.
    4. Add a new tab in `app.py` and call your render function.
    """
)
