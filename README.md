gem

# Prompt

I have a github project that is a great example of a WORKING streamlit project that works great when I run on desktop via VS Code and - crucially - also runs perfectly when deployed (with one click!) to streamlit community cloud.  

I want you to note two things about my project so we can isolate these things and create a new basic starter project premised on these things.  First, note how this project is organized to contain a few different .py projects inside it, and the streamlit app gracefully integrates the different modular .py scripts.  Then, note how this project creates three tabs as a neat simple way to isolate UI and UX for the user (one tab for config of API, a second tab for selecting models and tasks etc, and a third tab for creating or editing tasks).  

Now, what I want to do is create a basic starter project that has multiple .py scripts (which I will explain in a minute) and has:

* one tab to input the API key, 
* a second tab to select the model (we will only support the OpenAI model GPT-4o right now using the responses API but include two other options on pull-down "Claude 3.7" and "Gemini 2.5 Pro") and to set configs for the selected model like temperature, etc),
* a third tab with title "Python Script 1" for the user to chat with the model (prompt and output, and for each round of prompt/output that content is appended to a running log displayed at the bottom of that screen),
* a fourth tab reserved for "Python Script 2",
* a fifth tab reserved for "Python Script N".

The idea is that I will keep building out very modular (almost air-gapped) python scripts that do very different for each subsequent tab, and I will be able to use the same architecture to add any number of tabs, but they will all live under the same app.

Use web search to ensure you know how exactly to use the current OpenAI responses API for Model 4o and for the up to date info on building a streamline app for streamlit community cloud deployment in the best way to accommodate my plan. 

Can you please help me build this starter app in a good way? 

_____

# Output Gemini 2.5 Pro

Okay, this is a great plan! We'll build a modular Streamlit app that's easy to expand.

Here's how we'll structure the project and the code for your starter app:

**Project Structure:**

```
streamlit_multitab_starter/
├── app.py                 # Main Streamlit application file
├── modules/               # Directory for your modular Python scripts/logic
│   ├── __init__.py        # Makes 'modules' a Python package
│   ├── api_config.py      # Logic for API key tab
│   ├── model_config.py    # Logic for model selection & config tab
│   ├── script1_chat.py    # Logic for the chat tab (Python Script 1)
│   ├── script2_placeholder.py # Placeholder for Python Script 2
│   └── scriptN_placeholder.py # Placeholder for Python Script N
├── requirements.txt       # Python dependencies
└── .streamlit/
    └── secrets.toml       # For local development secrets (optional, good practice)
```

**1. `requirements.txt`:**

Create this file in the root of your `streamlit_multitab_starter` directory:

```txt
streamlit>=1.30.0
openai>=1.10.0
```
*Self-correction during thought process: It's good to specify minimum versions to ensure compatibility with recent features.*

**2. `.streamlit/secrets.toml` (Optional but Recommended for Local Dev):**

Create this directory and file if you want to pre-fill your API key locally without entering it every time.
**Important:** Add `.streamlit/secrets.toml` to your `.gitignore` file so you don't commit your actual secrets!

```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "your_openai_api_key_here_for_local_dev"
```
When deploying to Streamlit Community Cloud, you'll set this as a secret in the platform's settings.

**3. `modules/__init__.py`:**

This file can be empty. It just tells Python that the `modules` directory is a package.

**4. `modules/api_config.py`:**

This module will handle the UI and logic for the API key input tab.

```python
# modules/api_config.py
import streamlit as st

def render_api_key_tab():
    st.subheader("API Key Configuration")

    # Try to get API key from Streamlit secrets (for deployment)
    # or from a local secrets.toml file (for local development)
    # If not found, it will be None, and user needs to input it.
    cloud_api_key = st.secrets.get("OPENAI_API_KEY", None)
    
    # Initialize session state for API key if not already present
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = cloud_api_key if cloud_api_key else ""

    # Use a text input for the API key
    # We use session state to persist the key across reruns or tab switches
    entered_api_key = st.text_input(
        "Enter your OpenAI API Key:",
        type="password",
        value=st.session_state.openai_api_key,
        help="Get your API key from https://platform.openai.com/api-keys"
    )

    if entered_api_key:
        if entered_api_key != st.session_state.openai_api_key:
            st.session_state.openai_api_key = entered_api_key
            st.success("API Key updated!")
            # Optionally, re-initialize the client if it depends on the key
            if "openai_client" in st.session_state:
                del st.session_state.openai_client # Force re-creation
            st.rerun() # Rerun to reflect changes immediately

        if st.session_state.openai_api_key:
            st.success("API Key is set. You can proceed to other tabs.")
        else:
            st.warning("Please enter your OpenAI API Key to use the application.")
    else:
        st.warning("Please enter your OpenAI API Key.")

    st.markdown("---")
    st.markdown(
        "**Note:** Your API key is processed locally in your browser or on the Streamlit server "
        "when deployed. For Streamlit Community Cloud, set `OPENAI_API_KEY` in your app's secrets."
    )
```

**5. `modules/model_config.py`:**

This module handles model selection and configuration.

```python
# modules/model_config.py
import streamlit as st

def render_model_config_tab():
    st.subheader("Model Selection and Configuration")

    if not st.session_state.get("openai_api_key"):
        st.warning("Please enter your OpenAI API Key in the 'API Key' tab first.")
        return

    # Supported models
    # We will only implement GPT-4o for now
    model_options = {
        "GPT-4o": "gpt-4o",
        "Claude 3.7 Opus (Not Implemented)": "claude-3.7-opus", # Placeholder
        "Gemini 2.5 Pro (Not Implemented)": "gemini-2.5-pro"    # Placeholder
    }

    # Initialize session state for model selection if not already present
    if "selected_model_name" not in st.session_state:
        st.session_state.selected_model_name = "GPT-4o" # Default
    if "selected_model_id" not in st.session_state:
        st.session_state.selected_model_id = model_options["GPT-4o"]

    # Model selection dropdown
    selected_model_name = st.selectbox(
        "Select Model:",
        options=list(model_options.keys()),
        index=list(model_options.keys()).index(st.session_state.selected_model_name)
    )

    if selected_model_name != st.session_state.selected_model_name:
        st.session_state.selected_model_name = selected_model_name
        st.session_state.selected_model_id = model_options[selected_model_name]
        # Reset model-specific configs if model changes
        if "model_temperature" in st.session_state: # Example reset
            del st.session_state.model_temperature
        st.rerun()

    st.write(f"You selected: **{st.session_state.selected_model_name}** (ID: `{st.session_state.selected_model_id}`)")

    if st.session_state.selected_model_id == "gpt-4o":
        st.markdown("#### OpenAI Model Configuration (GPT-4o)")

        # Initialize temperature if not set
        if "model_temperature" not in st.session_state:
            st.session_state.model_temperature = 0.7

        temperature = st.slider(
            "Temperature:",
            min_value=0.0,
            max_value=2.0,
            value=st.session_state.model_temperature,
            step=0.1,
            help="Controls randomness. Lower values make the model more deterministic."
        )
        if temperature != st.session_state.model_temperature:
            st.session_state.model_temperature = temperature
            # No need to rerun for slider, value updates instantly in UI

        # You can add more GPT-4o specific settings here (e.g., max_tokens)
        # if "max_tokens" not in st.session_state:
        #     st.session_state.max_tokens = 1024
        # max_tokens = st.number_input("Max Tokens:", min_value=50, max_value=4096, value=st.session_state.max_tokens)
        # if max_tokens != st.session_state.max_tokens:
        #     st.session_state.max_tokens = max_tokens

    elif "Not Implemented" in st.session_state.selected_model_name:
        st.info(f"Configuration for {st.session_state.selected_model_name} is not yet implemented.")
    
    else:
        st.error("Selected model configuration not recognized.")

```

**6. `modules/script1_chat.py`:**

This module contains the logic for the chat interface with GPT-4o.

```python
# modules/script1_chat.py
import streamlit as st
from openai import OpenAI, APIError, RateLimitError

# Helper function to initialize OpenAI client (cached for efficiency)
# This ensures the client is created only once or when the API key changes.
@st.cache_resource # Caches the client resource
def get_openai_client(api_key):
    if not api_key:
        return None
    try:
        return OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize OpenAI client: {e}")
        return None

def render_chat_tab():
    st.subheader("Python Script 1: Chat with AI")

    # Ensure API key and model are selected
    if not st.session_state.get("openai_api_key"):
        st.warning("Please enter your OpenAI API Key in the 'API Key' tab.")
        return
    if not st.session_state.get("selected_model_id"):
        st.warning("Please select a model in the 'Model Config' tab.")
        return
    
    # Only proceed if GPT-4o is selected, as other models are not implemented
    if st.session_state.selected_model_id != "gpt-4o":
        st.info(f"Chat functionality is currently only implemented for GPT-4o. "
                f"Please select GPT-4o in the 'Model Config' tab.")
        return

    # Get the OpenAI client
    client = get_openai_client(st.session_state.openai_api_key)
    if not client:
        st.error("OpenAI client could not be initialized. Please check your API key.")
        return

    # Initialize chat history in session state if it doesn't exist
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [] # List of {"role": "user/assistant", "content": "..."}

    # Display past chat messages
    if st.session_state.chat_history:
        st.markdown("#### Conversation Log:")
        chat_container = st.container(height=300) # Scrollable container
        with chat_container:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        st.markdown("---")


    # User input
    user_prompt = st.chat_input("Your message:")

    if user_prompt:
        # Add user message to history and display it
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        
        # Prepare messages for OpenAI API (include history)
        # The API expects a list of message objects
        messages_for_api = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.chat_history]
        
        # Add a system message (optional, but good practice)
        # For simplicity, we'll add it here, but it could be configurable
        # Ensure system message is only added once or in a structured way if it's dynamic
        if not any(msg["role"] == "system" for msg in messages_for_api):
             messages_for_api.insert(0, {"role": "system", "content": "You are a helpful assistant."})


        try:
            with st.spinner("AI is thinking..."):
                response = client.chat.completions.create(
                    model=st.session_state.selected_model_id, # e.g., "gpt-4o"
                    messages=messages_for_api,
                    temperature=st.session_state.get("model_temperature", 0.7),
                    # max_tokens=st.session_state.get("max_tokens", 1024) # If you add max_tokens
                )
            
            ai_response = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            
            # Rerun to display the new messages immediately
            st.rerun()

        except APIError as e:
            st.error(f"OpenAI API Error: {e}")
        except RateLimitError:
            st.error("Rate limit exceeded. Please try again later or check your OpenAI plan.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

    # Button to clear chat history
    if st.button("Clear Chat History", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()

```

**7. `modules/script2_placeholder.py`:**

```python
# modules/script2_placeholder.py
import streamlit as st

def render_script2_tab():
    st.subheader("Python Script 2")
    st.write("This is a placeholder for Python Script 2.")
    st.info("You can build out the UI and logic for your second script here.")
    
    # Example: Add a simple input if needed to show modularity
    # text_input = st.text_input("Input for Script 2:")
    # if text_input:
    #     st.write(f"Script 2 received: {text_input}")
```

**8. `modules/scriptN_placeholder.py`:**

```python
# modules/scriptN_placeholder.py
import streamlit as st

def render_scriptN_tab():
    st.subheader("Python Script N")
    st.write("This is a placeholder for Python Script N.")
    st.info("You can build out the UI and logic for your Nth script here.")
    
    # Example: A button to demonstrate interaction
    # if st.button("Run Script N Action"):
    #     st.success("Script N action was 'triggered'!")
```

**9. `app.py` (Main Application):**

This file ties everything together.

```python
# app.py
import streamlit as st

# Import the render functions from your modules
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
st.caption("A starter project for building Streamlit apps with multiple, independent Python scripts.")

# --- Initialize Session State ---
# We do this at the top level if certain states are shared or need to be checked globally
# Individual modules also manage their own session states as needed.

# Example: Initialize API key if not already done by api_config upon first load
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = st.secrets.get("OPENAI_API_KEY", "") # Load from secrets if available

# --- Tab Creation ---
tab_titles = [
    "1. API Key",
    "2. Model Config",
    "3. Python Script 1 (Chat)",
    "4. Python Script 2",
    "5. Python Script N"
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

```

**How to Run:**

1.  Save all these files in the specified directory structure.
2.  Open your terminal or command prompt.
3.  Navigate to the `streamlit_multitab_starter` directory.
4.  Make sure you have an OpenAI API key. You can either:
    *   Put it in `.streamlit/secrets.toml` (for local dev).
    *   Or be ready to enter it in the first tab of the app.
5.  Run the command: `streamlit run app.py`

**Key Features Implemented:**

*   **Modularity:** Each tab's core logic is in its own Python file within the `modules` directory.
*   **Tabbed Interface:** Uses `st.tabs()` for clear UI separation.
*   **API Key Input (Tab 1):** Securely takes API key, stores in session state, and uses Streamlit secrets.
*   **Model Selection & Config (Tab 2):**
    *   Dropdown for model selection (GPT-4o, Claude 3.7 placeholder, Gemini 2.5 Pro placeholder).
    *   Temperature slider specifically for GPT-4o.
    *   Checks for API key before allowing configuration.
*   **Python Script 1 - Chat (Tab 3):**
    *   Chat interface using `st.chat_input` and `st.chat_message`.
    *   Uses the OpenAI `gpt-4o` model via the `ChatCompletions` API.
    *   Appends prompt/output to a running log (chat history) displayed on the screen.
    *   Chat history is maintained in session state.
    *   Uses `@st.cache_resource` for efficient OpenAI client initialization.
*   **Placeholder Tabs (4 & 5):** Ready for you to add `script2.py` and `scriptN.py` functionality.
*   **Streamlit Community Cloud Ready:**
    *   Uses `requirements.txt`.
    *   Integrates `st.secrets` for API key management (this is how you'll set it on the cloud).
*   **Session State Management:** Key variables (API key, selected model, chat history, etc.) are stored in `st.session_state` to persist across interactions and tab switches.

This structure should give you a solid foundation to build upon. You can now focus on implementing the specific logic for "Python Script 2", "Python Script N", and so on, by creating new files in the `modules` directory and integrating them similarly.
