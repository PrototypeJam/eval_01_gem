import streamlit as st

def render_api_key_tab():
    st.subheader("API Key Configuration")

    # This function now assumes st.session_state.openai_api_key has been initialized
    # (e.g., to "" in app.py if not already set).
    # We attempt to populate it from st.secrets if it's currently empty
    # or if st.secrets has a value and session_state doesn't.

    # Check if st.secrets has the key. This is safe even if secrets.toml doesn't exist.
    secret_api_key_exists = "OPENAI_API_KEY" in st.secrets
    secret_api_key_value = st.secrets["OPENAI_API_KEY"] if secret_api_key_exists else None

    # Initialize or update session_state.openai_api_key from secrets if appropriate:
    # 1. If session_state key isn't set at all (should be handled by app.py, but defensive)
    # 2. If session_state key is set but empty, and secrets has a value.
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = secret_api_key_value if secret_api_key_value else ""
    elif not st.session_state.openai_api_key and secret_api_key_value:
        # If current API key in session is empty, but secrets has one, use the one from secrets.
        st.session_state.openai_api_key = secret_api_key_value

    # Use a text input for the API key
    # We use session state to persist the key across reruns or tab switches
    entered_api_key = st.text_input(
        "Enter your OpenAI API Key:",
        type="password",
        value=st.session_state.openai_api_key,
        help="Get your API key from https://platform.openai.com/api-keys",
    )

    if entered_api_key:
        if entered_api_key != st.session_state.openai_api_key:
            st.session_state.openai_api_key = entered_api_key
            st.success("API Key updated!")
            # Optionally, re-initialize the client if it depends on the key
            if "openai_client" in st.session_state:
                del st.session_state.openai_client  # Force re-creation
            st.rerun()  # Rerun to reflect changes immediately

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
