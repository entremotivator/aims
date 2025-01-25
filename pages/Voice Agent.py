import streamlit as st
import speech_recognition as sr
import pyttsx3
from langchain.llms import Ollama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.callbacks import StreamlitCallbackHandler

from langchain.globals import get_verbose, set_verbose

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Define the function for capturing voice input
def capture_voice_input():
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
    return audio

# Define the function for converting voice input to text
def convert_voice_to_text(audio):
    try:
        text = recognizer.recognize_google(audio)
        st.write("You said: " + text)
        return text
    except sr.UnknownValueError:
        st.write("Sorry, I didn't understand that.")
        return ""
    except sr.RequestError as e:
        st.write("Error: {0}".format(e))
        return ""

# Define the function for processing voice commands using Ollama and LangChain
def process_voice_command(text, conversation):
    if text:
        st_callback = StreamlitCallbackHandler(st.container())
        response = conversation.predict(input=text, callbacks=[st_callback])
        st.markdown(response)
        test_tts(response)

# Function to speak the text
def test_tts(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    st.title("Enhanced Voice Chat App")

    # Initialize LangChain components
    llm = Ollama(model="llama3.2")
    
    template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

    Current conversation:
    {history}
    Human: {input}
    AI Assistant:"""

    prompt = PromptTemplate(input_variables=["history", "input"], template=template)
    memory = ConversationBufferMemory(return_messages=True)
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt,
        verbose=True
    )

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.button("Start Voice Input"):
        audio = capture_voice_input()
        text = convert_voice_to_text(audio)
        if text:
            st.session_state.messages.append({"role": "user", "content": text})
            with st.chat_message("user"):
                st.markdown(text)
            
            with st.chat_message("assistant"):
                process_voice_command(text, conversation)

    # Text input as an alternative to voice
    if prompt := st.chat_input("Or type your message here"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            process_voice_command(prompt, conversation)

if __name__ == "__main__":
    main()