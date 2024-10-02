import streamlit as st
import google.generativeai as genai
import os

# Configure the generative AI
genai.configure(api_key="AIzaSyA2SM2y12UnvsRowTqNcJLRVvl1kpBzRUQ")

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "Login"

# CSS Styling
def add_css():
    st.markdown("""
        <style>
            body {
                background-color: #f0f8ff;
                font-family: 'Courier New', Courier, monospace;
            }
            .chat-bubble {
                padding: 10px;
                background-color: #d1e7ff;
                border-radius: 20px;
                margin: 5px;
                width: fit-content;
                display: inline-block;
            }
            .chat-bubble-user {
                background-color: #ffffff;
                border: 1px solid #d1e7ff;
                color: #000000;
            }
            .center {
                text-align: center;
            }
            .header {
                font-size: 25px;
                font-weight: bold;
                color: #007acc;
                margin-bottom: 10px;
            }
            .sidebar .block-container {
                background-color: #f8f9fa;
            }
            .stButton>button {
                background-color: #007acc;
                color: white;
                border-radius: 10px;
                padding: 5px;
            }
        </style>
    """, unsafe_allow_html=True)

# Dummy Login Page
def login():
    add_css()
    st.title("🎓 Welcome to the Student Wellness Chatbot")
    st.subheader("Login to Get Started")
    email = st.text_input("Enter your student email")
    password = st.text_input("Enter your password", type="password")
    if st.button("Login"):
        if email and password:
            st.session_state.logged_in = True
            st.session_state.page = "Chat"
        else:
            st.warning("Please enter valid credentials.")

# Chatbot Function to generate response
def get_response(question):
    prompt = f"You are a licensed psychologist. Please provide this patient with a helpful response to their concern: {question}"
    response = model.generate_content(prompt)
    return response.text

# Sidebar Navigation
def sidebar_navigation():
    with st.sidebar:
        st.title("📄 **Navigation**")
        if st.button("Chat"):
            st.session_state.page = "Chat"
        if st.button("Profile"):
            st.session_state.page = "Profile"
        if st.button("Games"):
            st.session_state.page = "Games"
        if st.button("Videos & Articles"):
            st.session_state.page = "Videos"
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "Login"

# Chat Interface
def chat_interface():
    add_css()
    sidebar_navigation()
    st.title("💬 Student Wellness Chatbot")

    st.write('<div class="header">How can I help you today?</div>', unsafe_allow_html=True)

    # Chat input and response
    question = st.text_input("Ask a question", "")
    
    if st.button("Send"):
        if question:
            answer = get_response(question)
            st.session_state.chat_history.append({"user": question, "ai": answer})
        else:
            st.warning("Please enter a question.")

    # Display Chat History as Bubbles
    if st.session_state.chat_history:
        for chat in st.session_state.chat_history:
            st.markdown(f'<div class="chat-bubble chat-bubble-user">👤 {chat["user"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bubble">🤖 {chat["ai"]}</div>', unsafe_allow_html=True)

# Profile Page
def profile_page():
    add_css()
    sidebar_navigation()
    st.title("👤 Your Profile")
    st.write("John Doe - Sample University")
    st.write("Major: Psychology")
    st.write("Graduation Year: 2024")
    st.write("Interests: Mindfulness, Mental Health Advocacy")
    
    if os.path.exists("profile_image.png"):
        st.image("profile_image.png", use_column_width=True)
    else:
        st.image("https://via.placeholder.com/150", use_column_width=True)

    if st.button("Back to Chat"):
        st.session_state.page = "Chat"

# Games Section - Updated with more activities
def games_section():
    add_css()
    sidebar_navigation()
    st.title("🎮 Mindfulness & Games")

    # Interactive Games
    game_choice = st.selectbox("Choose an activity", [
        "Mindfulness Exercise", 
        "Breathing Exercise", 
        "Positive Affirmations",
        "Quick Relaxation Exercise",
        "5-Minute Gratitude Journal"
    ])

    if game_choice == "Mindfulness Exercise":
        st.write("Take a moment to focus on your breath. Close your eyes and pay attention to the sensation of breathing in and out.")
        st.write("Tip: Focus on the present moment and let go of any wandering thoughts.")
        if st.button("Try Again"):
            st.write("Close your eyes again and focus on the sounds around you.")
    
    elif game_choice == "Breathing Exercise":
        st.write("**Follow this breathing pattern**:")
        st.write("1. Inhale for 4 seconds")
        st.write("2. Hold your breath for 4 seconds")
        st.write("3. Exhale slowly for 4 seconds")
        st.write("Repeat this for at least 5 rounds to feel more relaxed.")
        st.image("https://via.placeholder.com/400x200", caption="Breathing Guide")
    
    elif game_choice == "Positive Affirmations":
        affirmations = ["I am strong.", "I am capable.", "I can achieve anything I set my mind to.", "I am in control of my emotions."]
        st.write("Here are some positive affirmations to repeat:")
        for affirmation in affirmations:
            st.write(f"- {affirmation}")
        st.write("Remember to say them out loud for a stronger impact!")
    
    elif game_choice == "Quick Relaxation Exercise":
        st.write("This is a 1-minute quick relaxation exercise:")
        st.write("1. Sit comfortably in your chair.")
        st.write("2. Close your eyes and relax your shoulders.")
        st.write("3. Inhale deeply through your nose for 5 seconds, then slowly exhale through your mouth.")
        st.write("4. Imagine yourself in a calm place like a beach or forest.")
    
    elif game_choice == "5-Minute Gratitude Journal":
        st.write("Write down 3 things you're grateful for today:")
        gratitude1 = st.text_input("1. I'm grateful for...")
        gratitude2 = st.text_input("2. I'm grateful for...")
        gratitude3 = st.text_input("3. I'm grateful for...")
        if gratitude1 and gratitude2 and gratitude3:
            st.write("Great job! Reflect on these moments throughout the day.")
    
    if st.button("Back to Chat"):
        st.session_state.page = "Chat"

# Positive Videos and Articles Section
def videos_and_articles_page():
    add_css()
    sidebar_navigation()
    st.title("📺 Positive Videos & Articles")
    
    st.write("Here's a collection of positive and inspirational content to help uplift your mood:")
    
    # Dummy Video Embed
    st.video("https://www.youtube.com/watch?v=4pKly2JojMw", start_time=10)
    
    # Sample Articles
    st.write("### Inspiring Articles")
    st.write("1. [The Power of Positive Thinking](https://example.com) - Learn how positivity can transform your mindset.")
    st.write("2. [Overcoming Anxiety](https://example.com) - Strategies to manage and reduce anxiety.")
    st.write("3. [Building Resilience](https://example.com) - Tips on how to bounce back from difficult situations.")
    
    if st.button("Back to Chat"):
        st.session_state.page = "Chat"

# Main App Logic - Page Navigation
if st.session_state.page == "Login":
    login()
elif st.session_state.logged_in:
    if st.session_state.page == "Chat":
        chat_interface()
    elif st.session_state.page == "Profile":
        profile_page()
    elif st.session_state.page == "Games":
        games_section()
    elif st.session_state.page == "Videos":
        videos_and_articles_page()
else:
    login()
