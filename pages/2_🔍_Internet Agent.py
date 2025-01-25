import streamlit as st
from langchain.llms import Ollama
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks import StreamlitCallbackHandler
from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler

# Title
st.title("AI Chat Assistant with Ollama Integration")

# Sidebar for user settings
st.sidebar.header("Settings")

# Model selection
ollama_models = ["llama2-uncensored:latest", "llama3:latest", "codellama:latest"]
selected_model = st.sidebar.selectbox("Choose Ollama Model", ollama_models, index=0)

# Internet search toggle
search_internet = st.sidebar.checkbox("Enable Internet Search?", value=False, key="internet")

# Session State for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to get response
def get_response(prompt, model, search):
    try:
        if not search:
            # Without internet search
            llm = Ollama(model=model, callback_manager=CallbackManager([StreamlitCallbackHandler(st.container())]))
            return llm.predict(prompt)
        else:
            # With internet search
            llm = Ollama(
                model=model,
                callback_manager=CallbackManager([FinalStreamingStdOutCallbackHandler()])
            )
            agent = initialize_agent(
                tools=load_tools(["ddg-search"]),
                llm=llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                handle_parsing_errors=True
            )
            return agent.run(prompt, callbacks=[StreamlitCallbackHandler(st.container())])
    except Exception as e:
        return f"Error: {str(e)}"

# Chat input
prompt = st.text_input("Enter your prompt:", key="prompt_input", help="Type a message to start the conversation.")

# Submit button
if st.button("Submit", type="primary"):
    if prompt:
        # Get response
        response = get_response(prompt, selected_model, search_internet)
        # Update chat history
        st.session_state.chat_history.append({"prompt": prompt, "response": response})

# Display chat history
st.subheader("Chat History")
for i, chat in enumerate(st.session_state.chat_history):
    st.markdown(f"**You:** {chat['prompt']}")
    st.markdown(f"**Assistant:** {chat['response']}")
    st.divider()

# Clear chat history
if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.experimental_rerun()

# Footer
st.markdown("---")
st.caption("Built with Ollama, LangChain, and Streamlit. Enhanced for real-time interactions.")


