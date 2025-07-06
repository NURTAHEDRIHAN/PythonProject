import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # female voice
engine.setProperty("rate", 150)


def speak(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        command = r.recognize_google(audio, language="en-in")
        print(f"You said: {command}")
    except sr.UnknownValueError:
        print("Sorry, didn't catch that. Please say again.")
        return "None"
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service")
        return "None"
    except Exception as e:
        print(f"Error occurred: {e}")
        return "None"
    return command.lower()

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning Nur tahed rihan!")
    elif 12 <= hour < 18:
        speak("Good Afternoon Nur tahed rihan!")
    else:
        speak("Good Evening Nur tahed rihan!")
    speak("I am your A..I desktop assistant. How can I help you today?")

def voice_password():
    speak(" Noor tahedd rihhhan...... i am A  i ruuumi...Please say the password to start.")
    password = "2501"
    while True:
        command = take_command()
        if password in command:
            speak("Password accepted. Starting assistant.")
            break
        elif command == "None":
            # If speech was not recognized, just prompt again without saying incorrect password
            continue
        else:
            speak("Incorrect password, please try again.")

def get_weather_dynamic(city):
    api_key = "8efed81fec545efc777bf81da48aa562"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"


    try:
        response = requests.get(url)
        data = response.json()
        print(data)  # DEBUG

        if data.get("cod") != "404" and data.get("main"):
            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"]
            speak(f"The weather in {city} is {int(temp)}°C with {weather}.")
        else:
            speak("Sorry Rihan, I couldn't find that city. Please try again.")
    except Exception as e:
        print("Error:", e)
        speak("Something went wrong while getting the weather.")



voice_password()
wish_me()

while True:
    query = take_command()

    if query == "None":
        continue  # ignore unrecognized input


    elif "open youtube" in query:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "play song" in query:
        speak("Which song do you want to play?")
        song = take_command()
        if song != "None":
            speak(f"Playing {song} on YouTube")
            url = f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}"
            webbrowser.open(url)
        else:
            speak("Sorry, I did not get the song name.")

    elif "time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Rihan, the time is {strTime}")
    elif "linkedin" in query or "open my linkedin" in query:
        speak("Opening LinkedIn main page")
        webbrowser.open("https://www.linkedin.com")

    elif "facebook" in query or "open my facebook" in query:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    elif "weather in" in query:
        speak("Which city are you asking about?")
        city_query = query.replace("weather in", "").strip()
        get_weather_dynamic(city_query)

    elif "stop" in query or "exit"  in query:
        speak("Goodbye Rihan, see you later!")
        break
