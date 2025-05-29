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
