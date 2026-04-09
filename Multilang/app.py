import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# ----------------------
# Load API Key
# ----------------------
load_dotenv()
MY_GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not MY_GROQ_API_KEY:
    st.error("API key not found. Please set MY_GROQ_API_KEY in Secrets.")
    st.stop()

client = Groq(api_key=MY_GROQ_API_KEY)

# ----------------------
# Page Config
# ----------------------
st.set_page_config(
    page_title="🌍 AI Language Translator",
    page_icon="🌐",
    layout="centered"
)

st.title("🌍 AI Multi-Language Translator")
st.markdown("Translate between multiple international and local languages instantly.")

# ----------------------
# Language Options
# ----------------------
languages = {
    "English": "English",
    "Urdu (اردو)": "Urdu written in Arabic (Nastaliq) script only",
    "Hindi (हिन्दी)": "Hindi written in Devanagari script only",
    "Arabic (العربية)": "Arabic",
    "French (Français)": "French",
    "German (Deutsch)": "German",
    "Chinese (中文)": "Chinese",
    "Spanish (Español)": "Spanish"
}

col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox("From:", list(languages.keys()), index=0)

with col2:
    target_lang = st.selectbox("To:", list(languages.keys()), index=1)

# ----------------------
# Example Text Buttons
# ----------------------
st.markdown("### ✨ Try Example Text")

if st.button("Example 1"):
    st.session_state.example_text = "Technology is changing the way we live and work."

if st.button("Example 2"):
    st.session_state.example_text = "Success comes from consistency and hard work."

input_text = st.text_area(
    "Enter text:",
    value=st.session_state.get("example_text", ""),
    height=150
)

# ----------------------
# Translate Button
# ----------------------
if st.button("🚀 Translate"):
    if not input_text.strip():
        st.warning("Please enter text to translate.")
    else:
        with st.spinner("Translating..."):
            try:
                prompt = f"""
                Translate the following text from {source_lang} to {languages[target_lang]}.
                Follow correct grammar and script rules.
                Output only the translated text.

                Text:
                {input_text}
                """

                response = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a professional multilingual translator."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.2
                )

                translated_text = response.choices[0].message.content.strip()

                st.markdown("### ✅ Translation Result")
                st.success(translated_text)

            except Exception as e:
                st.error(f"Error: {e}")

# ----------------------
# Footer
# ----------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit + Groq API")
