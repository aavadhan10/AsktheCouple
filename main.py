import streamlit as st
import openai

st.set_page_config(page_title="AskTheCouple 💛", page_icon="💍", layout="centered")

# Load API key from secrets
openai.api_key = st.secrets["openai"]["api_key"]

# Full wedding info (from your message)
wedding_info = """
🗓️ EVENT SCHEDULE — SATURDAY, JUNE 21, 2025

📍 Location: 733 Center Drive, Palo Alto, CA 94301 (Ankita’s childhood backyard)

Welcome & Arrival (2:15 pm – 2:30 pm): Guests arrive. Light bites and cocktails.  
Baraat & Refreshments (2:30 pm – 4:00 pm): Joyful groom's entrance + snacks.  
Indian Puja Wedding Ceremony (4:00 pm – 6:00 pm): Traditional ritual with a priest, fire, chanting, offerings.  
Dinner & Dancing (6:00 pm – 10:00 pm): Indian food, cocktails, cake, DJ & dancing!

👗 DRESS CODE:  
– American Semi-Formal: Tuxes, suits, cocktail dresses  
– Indian Semi-Formal: Sarees, lehengas, kurtas, Nehru jackets  
🌞 Dress light, July gets hot (~90°F).  
👠 Heels welcome — no grass!

🧒 Kids welcome  
🎁 No registry — your presence is the gift!  
🥘 Menu: Fully vegetarian, gluten/dairy/nut-free options available. Notify us of any allergies.  
🚗 Parking: Forest Ave = free, Center Drive = permit-only  
🌍 2026 will include Habesha + Western culture

FAQs:
– RSVP by: April 2025  
– Indian Ceremony: A peaceful, spiritual blessing with mantras, fire, flowers, etc. Inclusive for all.  
– This is our real wedding — legal one is separate. Reception in 2026.  
– Can I wear Indian attire? Yes! [saree.com] ships to U.S. or borrow from Ankita.  
– Registry? No!  
– Can I wear heels? Yes!  
– Plus ones? Only if invited (intimate event)  
– Other events? Nope, just this one!  
– Food allergies? Let us know — we’ll accommodate.  
– Kids? Yes!  
– Other cultures? 2026 event will be multicultural  
– Hotel info? See ‘Travel’ tab on website  
– Weather? Hot! Dress light and colorful.
"""

# List of button questions
questions = [
    "What should I wear?",
    "Is Parking Available?",
    "RSVP Details",
    "Kids & Plus Ones",
    "What is the Indian ceremony?",
    "Is there a gift registry?",
    "Event schedule?",
    "Food & Allergies",
    "Will there be other cultural traditions?",
    "Can I wear heels?",
    "What’s the weather like?",
    "Do you have hotel suggestions?",
    "What would you like to know that we haven’t already covered?"
]

st.title("💍 AskTheCouple")
st.markdown("Hi there! I’m your personal Wedding Q&A helper bot 🤖 for Ankita & Solomon’s wedding. \
Click a question below or ask your own!")

# Buttons as a radio menu
selected = st.radio("Pick a question:", questions, index=0)

# Optional custom question
st.markdown("Or ask your own:")
custom_question = st.text_input("Type your question here:")

# Determine which question to use
final_question = custom_question if custom_question else selected

# When clicked or typed
if final_question:
    with st.spinner("Thinking...💭"):
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are AskTheCouple — a warm, helpful wedding chatbot for Ankita & Solomon’s Palo Alto wedding. "
                        "Answer kindly, only using the info below. If you're not sure, say: 'Please check with the couple directly!'\n\n"
                        + wedding_info
                    )
                },
                {
                    "role": "user",
                    "content": final_question
                }
            ],
            temperature=0.6
        )
        st.success(response["choices"][0]["message"]["content"])

