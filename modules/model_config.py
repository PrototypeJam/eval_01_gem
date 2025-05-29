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
        "Claude 3.7 Opus (Not Implemented)": "claude-3.7-opus",  # Placeholder
        "Gemini 2.5 Pro (Not Implemented)": "gemini-2.5-pro",    # Placeholder
    }

    # Initialize session state for model selection if not already present
    if "selected_model_name" not in st.session_state:
        st.session_state.selected_model_name = "GPT-4o"  # Default
    if "selected_model_id" not in st.session_state:
        st.session_state.selected_model_id = model_options["GPT-4o"]

    # Model selection dropdown
    selected_model_name = st.selectbox(
        "Select Model:",
        options=list(model_options.keys()),
        index=list(model_options.keys()).index(st.session_state.selected_model_name),
    )

    if selected_model_name != st.session_state.selected_model_name:
        st.session_state.selected_model_name = selected_model_name
        st.session_state.selected_model_id = model_options[selected_model_name]
        # Reset model-specific configs if model changes
        if "model_temperature" in st.session_state:  # Example reset
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
            help="Controls randomness. Lower values make the model more deterministic.",
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
