import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime
import urllib.parse
import requests
from openai import OpenAI
from dotenv import dotenv_values
import time
import json

# Load API keys from .env file
secrets = dotenv_values(".env")
openAiKey = secrets.get("OPENAI_KEY")
newsKey = secrets.get("NEWS_KEY")
weatherKey = secrets.get("WEATHER_KEY")  # Added for weather API

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set speech rate for better responsiveness
engine.setProperty('volume', 0.9)  # Set volume

# Sample music library
music_library = {
    "despacito": "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
    "shape of you": "https://www.youtube.com/watch?v=JGwWNGJdvx8",
    "blinding lights": "https://www.youtube.com/watch?v=4NRXx6U8ABQ"
}

def speak(text):
    """Speak the provided text using pyttsx3."""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speech: {e}")

def aiprocess(command):
    """Process a command using OpenAI's API."""
    try:
        client = OpenAI(api_key=openAiKey)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant named Friday."},
                {"role": "user", "content": command}
            ],
            max_tokens=150
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "Sorry, I couldn't process that request right now."

def get_news():
    """Fetch top news headlines using News API."""
    if not newsKey:
        return ["News API key is missing."]
    
    url = f"https://newsapi.org/v2/top-headlines?country=us&category=general&apiKey={newsKey}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        news_data = response.json()
        
        if news_data["status"] == "ok":
            articles = news_data["articles"][:5]  # Fetch top 5 news articles
            return [f"Headline: {article['title']} - {article['description'] or 'No description available'}" for article in articles]
        else:
            return ["Could not fetch the news at this moment."]
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return [f"Error fetching news: {e}"]

def get_weather(city="New York"):
    """Fetch weather for a specified city using OpenWeatherMap API."""
    if not weatherKey:
        return ["Weather API key is missing."]
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weatherKey}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        weather_data = response.json()
        
        if weather_data.get("cod") == 200:
            temp = weather_data["main"]["temp"]
            description = weather_data["weather"][0]["description"]
            return [f"The weather in {city} is {description} with a temperature of {temp}°C."]
        else:
            return ["Could not fetch weather data."]
    except requests.RequestException as e:
        print(f"Error fetching weather: {e}")
        return [f"Error fetching weather for {city}: {e}"]

def set_alarm(command):
    """Set an alarm for the specified time in HH:MM format."""
    try:
        time_str = command.lower().replace("set alarm for", "").strip()
        alarm_time = datetime.datetime.strptime(time_str, "%H:%M").time()
        now = datetime.datetime.now()
        alarm_datetime = datetime.datetime.combine(now.date(), alarm_time)
        
        if alarm_datetime < now:
            alarm_datetime += datetime.timedelta(days=1)
        
        speak(f"Alarm set for {alarm_datetime.strftime('%I:%M %p')}")
        while datetime.datetime.now() < alarm_datetime:
            time.sleep(10)
        speak("Wake up! It's time!")
    except ValueError:
        speak("Please specify the alarm time in HH:MM format, like 07:30.")

def get_time_date(command):
    """Return current time or date based on command."""
    now = datetime.datetime.now()
    if "time" in command.lower():
        speak(f"The current time is {now.strftime('%I:%M %p')}")
    elif "date" in command.lower():
        speak(f"Today is {now.strftime('%B %d, %Y')}")

def search_web(query):
    """Perform a web search on Google."""
    if query:
        speak(f"Searching for {query} on Google")
        query = urllib.parse.quote(query)
        webbrowser.open(f"https://www.google.com/search?q={query}")
    else:
        speak("Please specify what to search for.")

def process_command(command):
    """Process the user's voice command."""
    print(f"Processing command: {command}")
    command_lower = command.lower().strip()
    
    try:
        if "google" in command_lower:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
        elif "youtube" in command_lower and "play" not in command_lower:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
        elif "linkedin" in command_lower:
            speak("Opening LinkedIn")
            webbrowser.open("https://www.linkedin.com")
        elif "facebook" in command_lower:
            speak("Opening Facebook")
            webbrowser.open("https://www.facebook.com")
        elif command_lower.startswith("play"):
            song = command_lower.replace("play", "").strip()
            if song in music_library:
                speak(f"Playing {song}")
                webbrowser.open(music_library[song])
            else:
                speak(f"Sorry, {song} is not in the music library. Searching on YouTube instead.")
                query = urllib.parse.quote(song)
                webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        elif "news" in command_lower:
            speak("Fetching the latest news...")
            news = get_news()
            for item in news:
                print(item)
                speak(item)
        elif "weather" in command_lower:
            city = command_lower.replace("weather", "").replace("in", "").strip() or "New York"
            speak(f"Fetching weather for {city}")
            weather = get_weather(city)
            for item in weather:
                print(item)
                speak(item)
        elif "set alarm" in command_lower:
            set_alarm(command_lower)
        elif "time" in command_lower or "date" in command_lower:
            get_time_date(command_lower)
        elif "search" in command_lower:
            query = command_lower.replace("search", "").strip()
            search_web(query)
        else:
            # Fallback to OpenAI for unknown commands
            output = aiprocess(command)
            print(output)
            speak(output)
    except Exception as e:
        print(f"Error processing command: {e}")
        speak("Sorry, I encountered an error while processing your request.")

def main():
    """Main loop to listen for commands."""
    speak("Initializing Friday, your AI assistant...")
    while True:
        print("Listening for wake word 'Friday'...")
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            print("Recognizing...")
            word = recognizer.recognize_google(audio)
            print(f"Wake word detected: {word}")
            if word.lower() == "friday":
                speak("Yes, boss? How can I assist you?")
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    print("Friday is active...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

                command = recognizer.recognize_google(audio)
                print(f"Command received: {command}")
                process_command(command)

        except sr.WaitTimeoutError:
            print("Listening timed out, waiting for wake word again...")
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            speak("I'm having trouble connecting to the speech service.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            speak("An unexpected error occurred.")

if __name__ == "__main__":
    main()
