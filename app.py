import streamlit as st
import pyttsx3
import datetime
import wikipedia
import requests

# ================= INITIAL SETUP =================
engine = pyttsx3.init()
engine.setProperty("rate", 160)
engine.setProperty("volume", 1)

def speak(text):
    """Alexa will speak"""
    engine.say(text)
    engine.runAndWait()

def get_weather(city="Lucknow"):
    """Fetch weather using free API"""
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url)
        return response.text
    except:
        return "Weather service not available right now."

def fallback_answer(query):
    """Try to answer any question"""
    # Predefined quick replies
    if "your name" in query:
        return "My name is Alexa, your personal assistant."
    elif "who are you" in query:
        return "I am Alexa, a simple voice assistant made in Python."
    elif "how are you" in query:
        return "I am fine, thank you! How can I help you?"

    # Try Wikipedia as backup
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except:
        return "Sorry, I don't know the answer to that. Please try asking something else."

# ================= STREAMLIT APP =================
st.title("Alexa Voice Assistant (Text Version)")
st.write("Type your query below and press Enter. Alexa will answer!")

query = st.text_input("Your Question:")

if query:
    query = query.lower()
    response = ""

    if "time" in query:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"The time is {time}"
    elif "date" in query:
        date = datetime.datetime.now().strftime("%d %B %Y")
        response = f"Today is {date}"
    elif "wikipedia" in query:
        st.write("🔍 Searching Wikipedia...")
        topic = query.replace("wikipedia", "").strip()
        try:
            result = wikipedia.summary(topic, sentences=2)
            response = result
        except:
            response = "Sorry, I could not find anything on Wikipedia."
    elif "weather" in query:
        city = "Lucknow"
        if "in" in query:
            city = query.split("in")[-1].strip()
        response = get_weather(city)
    elif "exit" in query or "quit" in query or "stop" in query:
        response = "Goodbye! Have a nice day."
    else:
        response = fallback_answer(query)

    st.write(f"**Alexa:** {response}")
    speak(response)
