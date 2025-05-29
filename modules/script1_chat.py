import streamlit as st
from openai import OpenAI, APIError, RateLimitError

# Helper function to initialize OpenAI client (cached for efficiency)
# This ensures the client is created only once or when the API key changes.
@st.cache_resource
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
        st.info(
            "Chat functionality is currently only implemented for GPT-4o. "
            "Please select GPT-4o in the 'Model Config' tab."
        )
        return

    # Get the OpenAI client
    client = get_openai_client(st.session_state.openai_api_key)
    if not client:
        st.error("OpenAI client could not be initialized. Please check your API key.")
        return

    # Initialize chat history in session state if it doesn't exist
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []  # List of {"role": "user/assistant", "content": "..."}

    # Display past chat messages
    if st.session_state.chat_history:
        st.markdown("#### Conversation Log:")
        chat_container = st.container(height=300)
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
        messages_for_api = [
            {"role": msg["role"], "content": msg["content"]} for msg in st.session_state.chat_history
        ]

        # Add a system message (optional, but good practice)
        if not any(msg["role"] == "system" for msg in messages_for_api):
            messages_for_api.insert(0, {"role": "system", "content": "You are a helpful assistant."})

        try:
            with st.spinner("AI is thinking..."):
                response = client.chat.completions.create(
                    model=st.session_state.selected_model_id,
                    messages=messages_for_api,
                    temperature=st.session_state.get("model_temperature", 0.7),
                )

            ai_response = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

            st.rerun()

        except APIError as e:
            st.error(f"OpenAI API Error: {e}")
        except RateLimitError:
            st.error("Rate limit exceeded. Please try again later or check your OpenAI plan.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

    if st.button("Clear Chat History", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()
