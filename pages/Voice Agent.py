import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import av
import numpy as np
from typing import List, NamedTuple
import pyttsx3
from langchain.llms import Ollama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.callbacks import StreamlitCallbackHandler

# Initialize text-to-speech engine
engine = pyttsx3.init()

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

class AudioFrame(NamedTuple):
    data: np.ndarray
    sample_rate: int

def process_audio(audio: AudioFrame) -> str:
    # This is where you'd implement your speech-to-text logic
    # For now, we'll just return a placeholder
    return "Placeholder text from audio"

def process_voice_command(text, conversation):
    if text:
        st_callback = StreamlitCallbackHandler(st.container())
        response = conversation.predict(input=text, callbacks=[st_callback])
        st.markdown(response)
        engine.say(response)
        engine.runAndWait()

def main():
    st.title("Enhanced Voice Chat App")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    webrtc_ctx = webrtc_streamer(
        key="speech-to-text",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        rtc_configuration=RTCConfiguration(
            {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
        ),
        media_stream_constraints={"video": False, "audio": True},
    )

    if webrtc_ctx.audio_receiver:
        sound_chunk = pydub.AudioSegment.empty()
        audio_frames = []
        while True:
            try:
                audio_frames.append(webrtc_ctx.audio_receiver.get_frame())
            except queue.Empty:
                break

        if len(audio_frames) > 0:
            sound_chunk += pydub.AudioSegment(
                data=audio_frames[-1].to_ndarray().tobytes(),
                sample_width=audio_frames[-1].format.bytes,
                frame_rate=audio_frames[-1].sample_rate,
                channels=len(audio_frames[-1].layout.channels),
            )

            if len(sound_chunk) > 0:
                try:
                    text = process_audio(AudioFrame(sound_chunk.raw_data, sound_chunk.frame_rate))
                    st.session_state.messages.append({"role": "user", "content": text})
                    with st.chat_message("user"):
                        st.markdown(text)
                    
                    with st.chat_message("assistant"):
                        process_voice_command(text, conversation)
                except Exception as e:
                    st.error(f"Error processing audio: {str(e)}")

    # Text input as an alternative to voice
    if prompt := st.chat_input("Or type your message here"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            process_voice_command(prompt, conversation)

if __name__ == "__main__":
    main()
