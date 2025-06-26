import streamlit as st
from openai import OpenAI
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
            color: #8b0000;
            background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%);
            border: 1px solid #f48fb1;
            border-radius: 20px;
            padding: 8px 16px;
            font-weight: 500;
            font-size: 0.85rem;
            box-shadow: 0 2px 6px rgba(244, 143, 177, 0.2);
            transition: all 0.2s ease;
            width: 100%;
            margin: 2px 0;
            text-align: center;
            white-space: normal;
            height: auto;
            min-height: 40px;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #f48fb1 0%, #d86f91 100%);
            color: white;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(216, 111, 145, 0.3);
        }
        
        /* Style the custom question button differently */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #d86f91 0%, #c2185b 100%);
            color: white;
            border-radius: 12px;
            padding: 0.5rem 1.5rem;
            font-weight: 600;
            width: auto;
            min-width: 120px;
        }
        
        .stSelectbox > div > div > div {
            color: #8b0000;
            font-weight: 500;
        }
        
        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 2px solid #f0f0f0;
            transition: border-color 0.2s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #d86f91;
            box-shadow: 0 0 0 1px #d86f91;
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
    """Load wedding information with all the details."""
    return """
    Solomon Demmessie and Ankita Avadhani Wedding
    June 21, 2025 - Palo Alto, California
    
    SCHEDULE:
    - Welcome and Arrival: 2:15 pm - 2:30 pm at Ankita's Childhood Backyard, 733 Center Drive, Palo Alto, CA 94301
    - Baraat & Refreshments: 2:30 pm - 4:00 pm - Join us for the Baraat — a joyful wedding procession where we dance and celebrate as the groom makes his grand entrance!
    - Indian Puja Wedding Ceremony: 4:00 pm - 6:00 pm - Traditional Indian ritual led by a guru (Indian Priest), filled with meaningful prayers and blessings
    - Dinner and Dancing: 6:00 pm - 10:00 pm - Indian dishes, cocktails, cake cutting, and DJ
    
    WEDDING INFORMATION:
    
    RSVP: ASAP (April 2025)
    
    Indian Puja Ceremony: A traditional Indian ritual led by a guru (Indian Priest), filled with meaningful prayers and blessings. During the ceremony, the guru will guide us in offering flowers, fruits, and prayers to the deities while chanting mantras to invoke prosperity and happiness. You'll see us light a sacred fire, which symbolizes purity and new beginnings. It's a peaceful and joyous tradition. We will have descriptions of each part of the ceremony for you at the Wedding.
    
    Is this the real wedding: To us, yes! We want to celebrate with a traditional Indian ceremony surrounded by you all and will get legally married at the courthouse. We're planning a large reception and big party in 2026.
    
    Dress Code: 
    - American Semi-Formal: Tuxes and gowns are welcome, and so are suits and cocktail dresses
    - Indian Semi-Formal: sarees, lehenga cholis, or salwar kameez, and kurtas or Nehru jackets with trousers
    - Bright colors and light fabrics are perfect for the occasion. July is typically a very warm month in California (with high's of 90) so dress light!
    
    Indian Attire: Yes! You can wear Indian attire. American Semi-Formal Inspiration: https://www.pinterest.com/kimberlygarz/semi-formal-wedding-attire/ 
    Indian Semi-Formal Inspiration: https://in.pinterest.com/shaadiwish/summer-wedding-outfits/
    If you're interested in wearing Indian attire, this website https://www.saree.com/ offers options with U.S. shipping. Please order 2-3 months in advance to ensure timely delivery or talk to Ankita about borrowing outfits if desired!
    
    Registry: We are not registered, as your presence is truly the best gift we could ask for. We're just excited to celebrate this special day with our loved ones!
    
    Heels: Yes! Luckily we have no grass in our backyard so feel free to wear whatever shoes you feel comfortable with!
    
    Plus One: We're keeping the celebration intimate with just close family and friends, so all invited guests will have their names listed on the invite. We appreciate your understanding!
    
    Other Events: Just this event! We are excited to have our larger party in 2026 and appreciate all of you taking the time to come to our small backyard wedding.
    
    Food Allergies: Absolutely! We will have a full vegetarian menu but will accommodate for all allergies. We will have dairy-free, gluten-free and nut-free options but please feel free to reach out with any requests!
    
    Parking: There will be limited street parking available as the wedding is in a small residential area. Center Drive requires a permit for street parking, but you can find parking on Forest Avenue (which runs perpendicular to Center Drive) without a permit. We recommend arriving a bit early to secure a spot!
    
    Kids: Yes! Since this is a small, family event, please bring your kids!
    
    Cultural Traditions: For this celebration, we'll be focusing on the Indian puja and wedding ceremony. Our larger reception in 2026 will blend both Habesha and Western traditions, along with diverse cuisine and more festivities.
    
    Hotels: We've put together a list of affordable recommended hotels within 20 minutes of the venue:
    - Courtyard Redwood City Marriott: 600 Bair Island Rd, Redwood City, CA 94063 (~10 Minute Drive to Ankita's House)
    We recommend Ubering to and from hotels to Ankita's House.
    
    Weather: Hot! July is an extremely hot month in California with temps up to 90 degrees! While we have a shaded backyard, we encourage everyone to dress colorfully and lightly to accommodate the heat!
    
    About the Ceremony: This will be an intimate ceremony with just Solomon and Ankita's closest friends and family. The puja is a sacred Indian ritual performed to invoke blessings, prosperity, and happiness as we begin this new chapter together. The ceremony includes prayers, offerings, and beautiful customs. While it's rooted in Indian tradition, it's a heartfelt and welcoming event for all to enjoy.
    """

def get_openai_response(prompt: str, context: str) -> Optional[str]:
    """Get response from OpenAI with error handling and retry logic."""
    
    # Check if API key is configured
    try:
        # Try different possible configurations
        api_key = None
        if "openai" in st.secrets and "api_key" in st.secrets["openai"]:
            api_key = st.secrets["openai"]["api_key"]
        elif "OPENAI_API_KEY" in st.secrets:
            api_key = st.secrets["OPENAI_API_KEY"]
        elif hasattr(st.secrets, 'openai') and hasattr(st.secrets.openai, 'api_key'):
            api_key = st.secrets.openai.api_key
            
        if not api_key or api_key == "sk-REPLACE_THIS_WITH_YOURS":
            st.error("🔑 OpenAI API key not configured. Please contact the administrators.")
            return None
            
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
    except Exception as e:
        st.error(f"🔑 Error accessing OpenAI API key: {str(e)}")
        return None
    
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
            response = client.chat.completions.create(
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
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            error_message = str(e).lower()
            
            if "rate limit" in error_message:
                if attempt < max_retries - 1:
                    st.warning(f"Rate limit reached. Retrying in {2 ** attempt} seconds...")
                    time.sleep(2 ** attempt)
                else:
                    st.error("Rate limit exceeded. Please try again in a few minutes.")
                    return None
                    
            elif "invalid" in error_message or "bad request" in error_message:
                st.error(f"Invalid request: {str(e)}")
                return None
                
            elif "authentication" in error_message or "unauthorized" in error_message:
                st.error("Authentication failed. Please check the API key configuration.")
                return None
                
            else:
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
    
    # Simplified single-column layout
    st.subheader("💬 Quick Questions")
    st.markdown("Click on any question below:")
    
    # Question list
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
        "What would you like to know that we haven't already covered?"
    ]
    
    # Create question bubbles using columns for layout
    cols = st.columns(3)
    
    for i, question in enumerate(questions):
        with cols[i % 3]:
            if st.button(question, key=f"q_{i}", help="Click to get an answer!"):
                with st.spinner("💭 Getting your answer..."):
                    answer = get_openai_response(question, context)
                    if answer:
                        display_answer(answer)
    
    # Custom question section
    st.markdown("---")
    st.subheader("✍️ Have Something Else in Mind?")
    
    user_question = st.text_input(
        "Type your own question:",
        placeholder="e.g., What time does the ceremony start?",
        help="Ask us anything about the wedding!"
    )
    
    if st.button("Ask Question", type="primary") and user_question:
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
