import streamlit as st
import requests
import json
import speech_recognition as sr
import pyttsx3
from datetime import datetime

# Ollama API configuration
OLLAMA_API_URL = "http://localhost:11434/api"

# Initialize speech recognition and text-to-speech
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def get_models():
    try:
        response = requests.get(f"{OLLAMA_API_URL}/tags")
        response.raise_for_status()
        models_info = response.json()
        if "models" in models_info:
            return [model["name"] for model in models_info["models"]]
        else:
            st.warning("No models found. Please install some models first.")
            return []
    except requests.RequestException as e:
        st.error(f"Error connecting to Ollama: {str(e)}")
        return []

def get_ollama_response(prompt, model):
    try:
        response = requests.post(f"{OLLAMA_API_URL}/generate", 
                                 json={"model": model, "prompt": prompt})
        response.raise_for_status()
        return response.json()['response']
    except requests.RequestException as e:
        return f"Error communicating with Ollama: {str(e)}"

def capture_voice_input():
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
    return audio

def convert_voice_to_text(audio):
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "SPEECH_NOT_RECOGNIZED"
    except sr.RequestError as e:
        return f"SPEECH_RECOGNITION_ERROR: {e}"

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    st.set_page_config(page_title="Advanced AI Voice Assistant", page_icon="🎤", layout="wide")
    st.title("🎤 Advanced AI Voice Assistant")

    # Sidebar for settings
    st.sidebar.header("Settings")
    
    # Model selection
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = None

    models = get_models()
    if models:
        st.session_state.selected_model = st.sidebar.selectbox("Select AI Model:", models)
    else:
        st.sidebar.warning("No models available. Please check your Ollama installation.")
        return

    # Voice output toggle
    voice_output = st.sidebar.checkbox("Enable voice output", value=True)

    # Initialize conversation history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input method selection
    input_method = st.radio("Choose input method:", ("Text", "Voice"))

    if input_method == "Voice":
        if st.button("Start Voice Input"):
            audio = capture_voice_input()
            text = convert_voice_to_text(audio)
            if text.startswith("SPEECH_NOT_RECOGNIZED"):
                st.warning("Sorry, I couldn't understand that. Please try again.")
            elif text.startswith("SPEECH_RECOGNITION_ERROR"):
                st.error(f"Speech recognition error: {text.split(': ')[1]}")
            else:
                st.session_state.messages.append({"role": "user", "content": text})
                with st.chat_message("user"):
                    st.markdown(text)
                
                with st.chat_message("assistant"):
                    response = get_ollama_response(text, st.session_state.selected_model)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    if voice_output:
                        speak_text(response)

    else:  # Text input
        if prompt := st.chat_input("Type your message here"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                response = get_ollama_response(prompt, st.session_state.selected_model)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                if voice_output:
                    speak_text(response)

    # Additional features
    st.sidebar.header("Additional Features")
    if st.sidebar.button("Clear Conversation"):
        st.session_state.messages = []
        st.experimental_rerun()

    if st.sidebar.button("Save Conversation"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump(st.session_state.messages, f, indent=2)
        st.sidebar.success(f"Conversation saved as {filename}")

if __name__ == "__main__":
    main()
