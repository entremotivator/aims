import streamlit as st
import subprocess
import os
from datetime import datetime
from functools import lru_cache
import shutil

# --- Helper Functions ---
def run_command(command):
    """Run a shell command and return its output."""
    try:
        with st.spinner("Executing command..."):
            result = subprocess.run(command, shell=True, text=True, capture_output=True)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if result.returncode == 0:
                return f"✅ Success [{timestamp}]\n\n{result.stdout}"
            else:
                return f"❌ Error [{timestamp}]\n\n{result.stderr}"
    except Exception as e:
        return f"❌ Exception: {e}"

@lru_cache(maxsize=1)
def list_models():
    """Return a list of installed Ollama models."""
    try:
        result = subprocess.run("ollama list", shell=True, text=True, capture_output=True)
        if result.returncode == 0:
            models = [line.split()[0] for line in result.stdout.strip().split("\n")[1:]]
            return models if models else ["No models installed."]
        return ["Error fetching models."]
    except Exception:
        return ["Error: Unable to fetch models."]

def check_system_space():
    """Check disk space and memory usage."""
    disk_usage = shutil.disk_usage("/")
    total = disk_usage.total // (1024 ** 3)
    used = disk_usage.used // (1024 ** 3)
    free = disk_usage.free // (1024 ** 3)
    return total, used, free

def list_local_llm_models(directory, limit=50):
    """List up to 50 LLM model files in a specified directory."""
    try:
        models = [f for f in os.listdir(directory) if f.endswith(".llm")][:limit]
        return models if models else ["No LLM models found in the directory."]
    except Exception as e:
        return [f"Error accessing directory: {e}"]

def is_server_running():
    """Check if Ollama server is running."""
    try:
        result = subprocess.run("pgrep -f 'ollama serve'", shell=True, capture_output=True)
        return result.returncode == 0
    except Exception:
        return False

def save_logs(content, filename="ollama_logs.txt"):
    """Save log content to a file."""
    with open(filename, "w") as f:
        f.write(content)
    st.success(f"Logs saved as {filename}")

# --- Page Config ---
st.set_page_config(page_title="Ollama Command Manager", layout="wide", page_icon="🧠")

# --- Sidebar Navigation ---
st.sidebar.title("⚙️ Navigation")
tabs = ["🏠 Home", "🚀 Server Management", "📦 Model Management", "💬 Model Interaction",
        "📜 Logs", "🖥️ System Info", "📁 Local LLM Directory", "⚙️ Settings"]
selected_tab = st.sidebar.radio("Choose a Section", tabs)

# --- Home ---
if selected_tab == "🏠 Home":
    st.title("🧠 Ollama Command Manager")
    st.write("Welcome to the Ollama Command Manager! Use the sidebar to navigate through the app.")
    st.image("https://ollama.ai/ollama.svg", width=300)
    st.markdown("""
        ### Key Features:
        - **Server Management**: Start, stop, and monitor the Ollama server.
        - **Model Management**: Pull, list, and remove models.
        - **Model Interaction**: Run models interactively with custom prompts.
        - **Logs**: Monitor and save logs for troubleshooting.
        - **System Info**: Check computer capacity and space.
        - **Local LLM Directory**: View locally stored LLM model files.
        - **Settings**: Customize the app's behavior.
    """)
    st.write("---")

# --- Server Management ---
elif selected_tab == "🚀 Server Management":
    st.header("🚀 Server Management")

    server_running = is_server_running()
    if server_running:
        st.success("✅ Ollama server is currently **running**.")
    else:
        st.warning("⚠️ Ollama server is **not running**.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Ollama Server"):
            output = run_command("ollama serve")
            st.code(output)

    with col2:
        st.info("To stop the server, terminate the process in your terminal.")

    st.write("---")
    st.subheader("🗂️ Installed Models")
    models = list_models()
    for model in models:
        st.markdown(f"- {model}")

# --- Model Management ---
elif selected_tab == "📦 Model Management":
    st.header("📦 Model Management")
    model_name = st.text_input("Enter Model Name", placeholder="e.g., llama3")
    if st.button("Pull Model"):
        if model_name:
            output = run_command(f"ollama pull {model_name}")
            st.code(output)
        else:
            st.warning("Please enter a valid model name.")

    models = list_models()
    selected_model = st.selectbox("Select Model to Remove", models)
    if st.button("Remove Model"):
        if selected_model and "Error" not in selected_model:
            confirmation = st.checkbox("Confirm removal")
            if confirmation:
                output = run_command(f"ollama rm {selected_model}")
                st.code(output)

# --- Model Interaction ---
elif selected_tab == "💬 Model Interaction":
    st.header("💬 Model Interaction")
    models = list_models()
    selected_model = st.selectbox("Choose a Model", models)
    system_prompt = st.text_area("System Prompt", placeholder="Set context...")
    user_prompt = st.text_area("User Prompt", placeholder="Ask the model...")

    if st.button("Run Model"):
        if user_prompt:
            command = f"ollama run {selected_model} \"{system_prompt}\n{user_prompt}\""
            output = run_command(command)
            st.code(output)
        else:
            st.warning("Please provide a user prompt.")

# --- Logs ---
elif selected_tab == "📜 Logs":
    st.header("📜 Logs")
    lines = st.slider("Number of Log Lines", 10, 100, 20)
    if st.button("Fetch Logs"):
        output = run_command(f"tail -n {lines} /var/log/ollama.log")
        st.code(output)
    if st.button("Save Logs"):
        save_logs(output)

# --- System Info ---
elif selected_tab == "🖥️ System Info":
    st.header("🖥️ System Information")
    total, used, free = check_system_space()
    st.write(f"💾 **Disk Capacity**: {total} GB")
    st.write(f"📊 **Used**: {used} GB")
    st.write(f"🟢 **Free**: {free} GB")

# --- Local LLM Directory ---
elif selected_tab == "📁 Local LLM Directory":
    st.header("📁 Local LLM Directory")
    directory = st.text_input("Enter Directory Path", value=".")
    limit = st.slider("Max Files to List", 10, 50, 20)
    if st.button("List Models"):
        models = list_local_llm_models(directory, limit)
        for model in models:
            st.markdown(f"- {model}")

# --- Settings ---
elif selected_tab == "⚙️ Settings":
    st.header("⚙️ Settings")
    st.info("Customize your app preferences here.")

# Footer
st.write("---")
st.caption("Built with ❤️ using Streamlit | [Ollama Documentation](https://ollama.ai)")
