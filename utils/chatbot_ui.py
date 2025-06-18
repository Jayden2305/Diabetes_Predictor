import streamlit as st
import google.generativeai as genai


def format_prompt(user_input):
    return f"""
You are a helpful, professional healthcare provider that specializes in diabetes care.

Your job is to answer questions only related to:
- Diabetes (type 1, type 2, gestational)
- Health and wellness
- Diet, nutrition, fitness
- Lifestyle tips to manage or prevent diabetes
- Diabetes medications or monitoring

If the user asks anything that is not related to healthcare or diabetes, politely respond:

"I'm here to help with questions about diabetes and health. Please ask something related to that."

---

User: {user_input}
"""


@st.cache_resource
def load_gemini_api():
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        return genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        st.error(f"Error initializing Gemini: {str(e)}")
        return None

def render_chat_ui():
    model = load_gemini_api()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "last_submitted_input" not in st.session_state:
        st.session_state.last_submitted_input = None

    # Render chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown("<h4>🩺 Ask Me About Diabetes</h4>", unsafe_allow_html=True)

    # Show chat history
    for chat in st.session_state.chat_history:
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**Gemini:** {chat['gemini']}")

    # Chat form
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Your message", key="chat_input", label_visibility="collapsed")
        submitted = st.form_submit_button("Send")

    # ✅ Process after rerun
    if submitted:
        st.session_state.last_submitted_input = user_input

    if st.session_state.last_submitted_input:
        user_input = st.session_state.last_submitted_input
        st.session_state.last_submitted_input = None  # clear temp state

        st.session_state.chat_history.append({"user": user_input, "gemini": "..."})
        try:
            formatted_prompt = format_prompt(user_input)
            response = model.generate_content(formatted_prompt)
            st.session_state.chat_history[-1]["gemini"] = response.text
        except Exception as e:
            st.error("Error getting response from Gemini.")
            st.session_state.chat_history[-1]["gemini"] = "Error."

    st.markdown("</div>", unsafe_allow_html=True)


