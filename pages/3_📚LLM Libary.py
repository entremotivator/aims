import streamlit as st

# Configure the app
st.set_page_config(
    page_title="AI Tools Directory",
    page_icon="🤖",
    layout="wide",
)

# Helper function to create tabs with tools
def display_tools(category_name, tools):
    st.header(category_name)
    cols = st.columns(3)
    for i, tool in enumerate(tools):
        with cols[i % 3]:
            st.markdown(f"### {tool['name']}")
            st.markdown(tool['description'])
            if tool.get('link'):
                st.markdown(f"[Learn more about {tool['name']}]({tool['link']})")

# Define categories and tools
categories = {
    "General Chat Models": [
        {"name": "OpenAI GPT-4", "description": "State-of-the-art general-purpose language model for chat and content creation.", "link": "https://openai.com/gpt-4"},
        {"name": "Anthropic Claude", "description": "Ethical and helpful AI focused on safer conversations.", "link": "https://www.anthropic.com"},
        {"name": "Google Bard (LaMDA)", "description": "Conversational AI for natural, human-like dialogues.", "link": "https://bard.google.com"},
        {"name": "Meta LLaMA 2", "description": "Open-source language model optimized for chat and reasoning.", "link": "https://ai.meta.com/llama/"},
        {"name": "Mistral 7B", "description": "High-quality open-weight model focused on general text generation.", "link": "https://mistral.ai"},
        {"name": "ChatGPT Turbo", "description": "A faster, cheaper version of GPT for large-scale conversational tasks.", "link": "https://openai.com/chatgpt"},
        {"name": "EleutherAI GPT-J-6B", "description": "Open-source language model for general conversation.", "link": "https://www.eleuther.ai"},
    ],
    "Instruction-Focused Models": [
        {"name": "Hugging Face BLOOM", "description": "Multilingual instruction-following model.", "link": "https://huggingface.co/bloom"},
        {"name": "Cohere Command", "description": "Model for following detailed instructions across domains.", "link": "https://cohere.ai"},
        {"name": "Anthropic Claude-instruct", "description": "Instruction-optimized variant of Claude.", "link": "https://www.anthropic.com"},
        {"name": "Alpaca", "description": "Fine-tuned LLaMA for instruction-based tasks.", "link": "https://crfm.stanford.edu/2023/03/13/alpaca.html"},
        {"name": "Flan-T5", "description": "Google's fine-tuned transformer for instructional outputs.", "link": "https://ai.googleblog.com/2023/04/flan-t5-instruction-tuned-language.html"},
        {"name": "WizardLM", "description": "Instruction-tuned language model optimized for reasoning.", "link": "https://github.com/ehartford/WizardLM"},
        {"name": "T5 (Text-to-Text Transfer Transformer)", "description": "Pretrained to perform any NLP task as a text-to-text problem.", "link": "https://github.com/google-research/text-to-text-transfer-transformer"},
    ],
    "Code-Centric Models": [
        {"name": "OpenAI Codex", "description": "Backbone of GitHub Copilot for code generation and explanation.", "link": "https://openai.com/blog/openai-codex"},
        {"name": "Amazon CodeWhisperer", "description": "AI pair programmer for multiple languages.", "link": "https://aws.amazon.com/codewhisperer/"},
        {"name": "Meta CodeLlama", "description": "Optimized for understanding and writing code snippets.", "link": "https://ai.meta.com/blog/codellama/"},
        {"name": "TabNine", "description": "Lightweight code completion AI compatible with IDEs.", "link": "https://www.tabnine.com"},
        {"name": "Replit Ghostwriter", "description": "Model designed for real-time collaborative coding.", "link": "https://replit.com/ghostwriter"},
        {"name": "StarCoder", "description": "Open-source model trained on a large-scale code corpus.", "link": "https://huggingface.co/bigcode"},
        {"name": "PolyCoder", "description": "Specialized in low-level language programming.", "link": "https://polycoder.ai"},
        {"name": "Salesforce CodeGen", "description": "Multi-turn conversational code generator.", "link": "https://github.com/salesforce/CodeGen"},
    ],
    "Vision-Centric Models": [
        {"name": "OpenAI DALL-E 3", "description": "Generates detailed images from text prompts.", "link": "https://openai.com/dall-e"},
        {"name": "DeepMind Flamingo", "description": "Combines vision and language for captioning and question answering.", "link": "https://deepmind.com"},
        {"name": "Google PaLM-E", "description": "Robust vision-language model for multimodal tasks.", "link": "https://ai.google/palm-e/"},
        {"name": "CLIP (OpenAI)", "description": "Maps images and text into shared embeddings for comparisons.", "link": "https://openai.com/clip"},
        {"name": "ImageBind (Meta)", "description": "Cross-modal embeddings for vision, text, and audio.", "link": "https://ai.meta.com/blog/imagebind/"},
        {"name": "Blip-2", "description": "Vision-language model for captioning and visual reasoning.", "link": "https://huggingface.co/spaces/Salesforce/BLIP2"},
    ],
    "Voice Models": [
        {"name": "OpenAI Whisper", "description": "Robust ASR (automatic speech recognition) for transcription and translation.", "link": "https://openai.com/whisper"},
        {"name": "ElevenLabs Voice AI", "description": "Text-to-speech synthesis with realistic outputs.", "link": "https://elevenlabs.io"},
        {"name": "Deepgram", "description": "AI for transcription and voice search.", "link": "https://deepgram.com"},
        {"name": "Google WaveNet", "description": "Neural network for ultra-realistic voice generation.", "link": "https://deepmind.com/wavenet"},
        {"name": "Speechmatics", "description": "Multilingual ASR engine with high accuracy.", "link": "https://speechmatics.com"},
        {"name": "Resemble AI", "description": "Voice cloning and text-to-speech with tonal flexibility.", "link": "https://www.resemble.ai"},
    ]
}

# Render tabs for each category
st.title("AI Tools Directory")

with st.sidebar:
    selected_category = st.radio("Select a Category", list(categories.keys()))

display_tools(selected_category, categories[selected_category])
