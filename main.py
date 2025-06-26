import streamlit as st
import openai
from typing import Optional
import time

# --- Configuration ---
st.set_page_config(
    page_title="AskTheCouple Wedding Bot 💍", 
    page_icon="💐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Enhanced Styling ---
st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #fff0f5 0%, #fdf2f8 100%);
            padding: 2rem 1rem;
        }
        
        .stButton > button {
            color: white;
            background: linear-gradient(135deg, #d86f91 0%, #c2185b 100%);
            border: none;
            border-radius: 25px;
            padding: 0.6rem 2rem;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(216, 111, 145, 0.3);
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(216, 111, 145, 0.4);
        }
        
        .stSelectbox > div > div > div {
            color: #8b0000;
            font-weight: 500;
        }
        
        .wedding-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%);
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        
        .answer-box {
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            border-left: 5px solid #d86f91;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin: 1rem 0;
        }
        
        .error-box {
            background: #ffebee;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #f44336;
            color: #c62828;
            margin: 1rem 0;
        }
        
        .loading-text {
            color: #d86f91;
            font-style: italic;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# --- Enhanced Header ---
st.markdown("""
    <div class="wedding-header">
        <h1>💌 Welcome to AskTheCouple!</h1>
        <p style="font-size: 1.2rem; color: #666; margin-top: 1rem;">
            Hi there, and welcome to our wedding Q&A space — just for our guests!<br>
            I'm your personal Wedding Helper Bot 🤖
        </p>
        <p style="color: #888; margin-top: 1rem;">
            Got a question about what to wear, where to park, or what this whole Puja thing is? 
            You're in the right place 💛
        </p>
    </div>
""", unsafe_allow_html=True)

# --- Functions ---
@st.cache_data
def load_wedding_context() -> str:
    """Load wedding information from file with error handling."""
    try:
        with open("ankita_solomon_wedding_info.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error("Wedding information file not found. Please contact the wedding hosts.")
        return ""
    except Exception as e:
        st.error(f"Error loading wedding information: {str(e)}")
        return ""

def get_openai_response(prompt: str, context: str) -> Optional[str]:
    """Get response from OpenAI with error handling and retry logic."""
    
    # Check if API key is configured
    api_key = st.secrets.get("OPENAI_API_KEY")
    if not api_key or api_key == "sk-REPLACE_THIS_WITH_YOURS":
        st.error("🔑 OpenAI API key not configured. Please contact the administrators.")
        return None
    
    openai.api_key = api_key
    
    full_prompt = f"""
    You are AskTheCouple — a warm, culturally-aware wedding chatbot helping guests get answers.
    
    Guidelines:
    - Be friendly, warm, and welcoming
    - Provide clear, helpful answers
    - If you don't know something from the context, politely say so
    - Use emojis appropriately to match the festive mood
    - Be culturally sensitive, especially regarding Indian wedding traditions
    
    Context about the wedding:
    {context}
    
    Guest question: {prompt}
    
    Answer in a friendly, helpful tone:
    """
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are AskTheCouple, a culturally-aware, kind, and helpful wedding assistant for guests. Provide warm, informative answers about wedding details."
                    },
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.7,
                max_tokens=500,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            return response['choices'][0]['message']['content'].strip()
            
        except openai.error.RateLimitError:
            if attempt < max_retries - 1:
                st.warning(f"Rate limit reached. Retrying in {2 ** attempt} seconds...")
                time.sleep(2 ** attempt)
            else:
                st.error("Rate limit exceeded. Please try again in a few minutes.")
                return None
                
        except openai.error.InvalidRequestError as e:
            st.error(f"Invalid request: {str(e)}")
            return None
            
        except openai.error.AuthenticationError:
            st.error("Authentication failed. Please check the API key configuration.")
            return None
            
        except Exception as e:
            if attempt < max_retries - 1:
                st.warning(f"Error occurred. Retrying... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(1)
            else:
                st.error(f"Sorry, I couldn't process your question right now. Please try again later.")
                return None
    
    return None

def display_answer(answer: str):
    """Display answer in a styled box."""
    st.markdown(f"""
        <div class="answer-box">
            <h4>💬 Answer</h4>
            <p>{answer}</p>
        </div>
    """, unsafe_allow_html=True)

# --- Main App Logic ---
def main():
    # Load wedding context
    context = load_wedding_context()
    if not context:
        st.stop()
    
    # Create two columns for better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Quick Questions")
        
        # Enhanced question list with categories
        questions = {
            "📅 Event Details": [
                "When should I RSVP by?",
                "Is this the real wedding?",
                "Are there any other events around the wedding?",
                "What's the weather going to be like?"
            ],
            "🎭 Cultural & Traditions": [
                "What is an Indian Wedding Puja Ceremony?",
                "Will there be other Cultural Traditions?",
                "Can I wear Indian Attire?"
            ],
            "👗 Dress Code & Attire": [
                "Is there a dress code?",
                "Can I Wear Heels?"
            ],
            "🍽️ Food & Logistics": [
                "I have a food allergy, can I make a special request?",
                "Is there parking for the Wedding?",
                "Are kids welcome?",
                "Can I bring a plus one?"
            ],
            "🎁 Gifts & Accommodation": [
                "Are you registered? Where?",
                "Do you have any hotel recommendations?"
            ],
            "❓ Other": [
                "What would you like to know that we haven't already covered?"
            ]
        }
        
        # Flatten questions for selectbox
        all_questions = []
        for category, q_list in questions.items():
            all_questions.extend(q_list)
        
        selected_question = st.selectbox(
            "Choose a question or browse by category:",
            [""] + all_questions,
            help="Select a common question to get instant answers!"
        )
        
        if selected_question:
            with st.spinner("💭 Thinking..."):
                answer = get_openai_response(selected_question, context)
                if answer:
                    display_answer(answer)
    
    with col2:
        st.subheader("📝 Categories")
        for category, q_list in questions.items():
            with st.expander(category):
                for q in q_list:
                    if st.button(q, key=f"btn_{q}"):
                        with st.spinner("💭 Getting your answer..."):
                            answer = get_openai_response(q, context)
                            if answer:
                                display_answer(answer)
    
    # Custom question section
    st.markdown("---")
    st.subheader("✍️ Ask Your Own Question")
    
    with st.form("custom_question_form", clear_on_submit=True):
        user_question = st.text_area(
            "Type your question here:",
            placeholder="e.g., What time does the ceremony start?",
            height=100
        )
        submit_button = st.form_submit_button("Ask Question 🤔")
        
        if submit_button and user_question:
            with st.spinner("💭 Finding the perfect answer for you..."):
                answer = get_openai_response(user_question, context)
                if answer:
                    display_answer(answer)

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #888; padding: 1rem;">
            <p>💕 Made with love for our wedding guests 💕</p>
            <p><small>Having trouble? Feel free to reach out to us directly!</small></p>
        </div>
    """, unsafe_allow_html=True)

# --- Initialize session state ---
if 'initialized' not in st.session_state:
    st.session_state.initialized = True

if __name__ == "__main__":
    main()

