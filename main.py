import streamlit as st
import openai

# --- Configuration ---
st.set_page_config(page_title="AskTheCouple Wedding Bot 💍", page_icon="💐")

st.markdown("""
    <style>
        .main {background-color: #fff0f5;}
        .stButton>button {color: white; background-color: #d86f91; border-radius: 12px;}
        .stSelectbox>div>div>div {color: #8b0000;}
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.title("💌 Welcome to AskTheCouple!")
st.markdown("Hi there, and welcome to our wedding Q&A space — just for our guests!\nI'm your personal Wedding Helper Bot 🤖\n\nGot a question about what to wear, where to park, or what this whole Puja thing is? You're in the right place 💛")

# --- OpenAI Setup ---
openai.api_key = st.secrets.get("OPENAI_API_KEY", "sk-REPLACE_THIS_WITH_YOURS")

# --- Dropdown Menu of Common Questions ---
questions = [
    "When should I RSVP by?",
    "What is an Indian Wedding Puja Ceremony?",
    "Is this the real wedding?",
    "Is there a dress code?",
    "Can I wear Indian Attire?",
    "Are you registered? Where?",
    "Can I Wear Heels?",
    "Can I bring a plus one?",
    "Are there any other events around the wedding?",
    "I have a food allergy, can I make a special request?",
    "Is there parking for the Wedding?",
    "Are kids welcome?",
    "Will there be other Cultural Traditions?",
    "Do you have any hotel recommendations?",
    "What's the weather going to be like?",
    "What would you like to know that we haven’t already covered"
]

question = st.selectbox("Choose a question:", questions)

if question:
    # Combine with your wedding FAQ content
    with open("ankita_solomon_wedding_info.txt", "r") as f:
        context = f.read()

    prompt = f"""
    You are AskTheCouple — a warm, culturally-aware wedding chatbot helping guests get answers.
    Use the context below to answer clearly and kindly:

    Context:
    {context}

    Guest question: {question}
    Answer:
    """

    # --- Get response from OpenAI ---
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a culturally-aware, kind, wedding assistant for guests."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    answer = response['choices'][0]['message']['content']
    st.markdown(f"### 💬 Answer\n{answer}")

# Optional: allow users to ask a custom question
toggle = st.checkbox("Or, ask your own question ✍️")
if toggle:
    user_q = st.text_input("Type your question here")
    if user_q:
        prompt = f"""
        You are AskTheCouple — a warm, culturally-aware wedding chatbot.
        Based on the following context, answer the guest's custom question.

        Context:
        {context}

        Guest question: {user_q}
        Answer:
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a culturally-aware, kind, wedding assistant for guests."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        answer = response['choices'][0]['message']['content']
        st.markdown(f"### 💬 Answer\n{answer}")
