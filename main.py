import streamlit as st
from openai import OpenAI

# 💬 Set your OpenAI API key (from secrets.toml or environment)
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# 💖 Wedding theme styling
st.set_page_config(page_title="AskTheCouple 💍", page_icon="💍")
st.markdown("""
    <style>
        body { background-color: #fff8f0; }
        .stButton>button {
            background-color: #fce4ec;
            color: #880e4f;
            border-radius: 25px;
            padding: 0.4rem 1.2rem;
            border: none;
            font-weight: 600;
        }
        .stTextInput>div>div>input {
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# 💌 Welcome Message
st.markdown("## 🎉 Welcome to AskTheCouple!")
st.write("""
Hi there, and welcome to our wedding Q&A space — just for our guests!  
I'm your personal Wedding Helper Bot 🤖  
Got a question about what to wear, where to park, or what this whole Puja thing is?

You're in the right place — just tap a button below or ask your own 💛
""")

# 🧠 Contextual Knowledge Base (for grounding answers)
wedding_info = """
When should I RSVP by?
ASAP (April 2025)

What is an Indian Wedding Puja Ceremony?
An Indian Puja Ceremony is a traditional ritual involving prayers, offerings, and chanting for blessings and prosperity. It’s our way of honoring culture and starting marriage with love. We'll have descriptions of each part of the ceremony at the Wedding.

Is this the real wedding?
Yes! We're doing a traditional Indian ceremony now and a big reception in 2026.

Is there a dress code?
Yes:  
American Semi-Formal (suits, cocktail dresses)  
Indian Semi-Formal (sarees, lehengas, salwar kameez, kurtas)  
It’ll be hot (~90°F in July), so dress light!

Can I wear Indian Attire?
Yes! Inspiration:  
- [Western](https://www.pinterest.com/kimberlygarz/semi-formal-wedding-attire/)  
- [Indian](https://in.pinterest.com/shaadiwish/summer-wedding-outfits/)  
- Borrow or try [saree.com]

Are you registered?
No — your presence is the best gift ❤️

Can I Wear Heels?
Yes! Backyard has no grass, so wear what you love.

Can I bring a plus one?
Only listed guests are invited, thank you for understanding!

Any other events?
Just this one!

Food allergies?
Yes, we accommodate! Full vegetarian menu with dairy-free, gluten-free, and nut-free options.

Parking?
Limited street parking. Forest Ave (no permit needed), Center Drive (permit required). Arrive early.

Kids welcome?
Yes! Bring your little ones.

Will there be other Cultural Traditions?
This ceremony focuses on the Indian Puja. Our 2026 party will blend Habesha and Western traditions!

Hotel Recs?
Yes — check our website for options near Palo Alto and things to do in the Bay Area.

Weather?
Hot — up to 90°F! Dress light, colors welcome.

Schedule:
- 2:15 pm: Arrival (light bites)
- 2:30 pm: Baraat
- 4:00 pm: Indian Puja Ceremony
- 6:00 pm: Dinner, cake & dancing

Venue:
Ankita’s Childhood Backyard  
733 Center Drive, Palo Alto, CA
"""

# 💬 Common Questions
bubble_qs = [
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

st.markdown("### 💬 Common Questions")
selected = None

for i in range(0, len(bubble_qs), 3):
    cols = st.columns(3)
    for col, q in zip(cols, bubble_qs[i:i+3]):
        if col.button(q):
            selected = q

# ✏️ Custom Question
custom_q = st.text_input("Or ask your own question:")

# 🟣 Final question
final_question = custom_q.strip() if custom_q else selected

# 🚀 Ask OpenAI
if final_question:
    with st.spinner("Thinking... 💭"):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful, cheerful wedding assistant helping guests understand details about Ankita and Solomon's wedding. Be concise, warm, and informative. Use emojis occasionally."},
                {"role": "user", "content": f"{final_question}\n\nHere is all the wedding information:\n{wedding_info}"}
            ],
            temperature=0.6
        )

        st.markdown("### 💡 Answer")
        st.success(response.choices[0].message.content)

