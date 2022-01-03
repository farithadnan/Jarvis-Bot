import requests
from functions.online_ops import find_my_ip, get_latest_news, get_random_advice, get_random_joke, get_trending_movies, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, send_whatsapp_message

from pprint import pprint

# Library for text to speech conversion
import pyttsx3

# library to fetch config from .env
from decouple import Config, config

# Datetime library
from datetime import datetime

from functions.os_ops import open_calculator, open_camera, open_cmd, open_vscode, open_discord

# The Recognizer class within the speech_recognition module helps us recognize the audio
import speech_recognition as sr
from random import choice
from utils import opening_text

# Fetch bot details
USERNAME = config('USER')
BOTNAME  = Config('BOTNAME')    

# Initialize Engine
# sapi5 is a Microsoft Speech API that helps us use the voices
engine = pyttsx3.init('sapi5')

# Set Rate
engine.setProperty('rate', 190)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)



# In the speak() method, the engine speaks whatever text is passed to it using the say() method. 
# Using the # runAndWait() method, it blocks during the event loop and returns when the commands queue is cleared

# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""

    engine.say(text)
    engine.runAndWait()


# Greet Function; greets user whenever the program is run
def greet_user():
    """Greets the user according to the time"""

    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good Afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USERNAME}")
    speak(f"I am {BOTNAME}. How may I assist you, {USERNAME}?")


# function to take the commands from the user and recognize the command using the speech_recognition module.
def take_user_input():
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""

    # The Recognizer class within the speech_recognition module helps us recognize the audio.
    r = sr.Recognizer()

    # The same module has a Microphone class that gives us access to the microphone of the device. So with the microphone as the source
    with sr.Microphone() as source:
        print('Listening....')

        # set the pause_threshold to 1, that is it will not complain even if we pause for one second during we speak
        r.pause_threshold = 3
        #  we try to listen to the audio using the listen() method in the Recognizer class
        audio = r.listen(source)
    
    try:
        print('Recognizing....')

        # using the recognize_google() method from the Recognizer class, we try to recognize the audio. 
        # The recognize_google() method performs speech recognition on the audio passed to it, using the Google Speech Recognition API
        query = r.recognize_google(audio, language='en-us')

        # If the query has exit or stop words in it, it means we're asking the assistant to stop immediately. So, before stopping, we greet the user again as per the current hour
        if not 'exit' in query or 'stop' in query:
            # If the query doesn't have those two words (exit or stop), we speak something to tell the user that we have heard them. For that, we will use the choice method from the random module to randomly select any statement from the opening_text list. After speaking, we exit from the program
            speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good Night sir, take care!")
            else:
                speak("Have a good day sir!")
            exit()
    except Exception:
        speak('Sorry, I could not understand. Could you please say that again?')
        query = 'None'
    return query
 
if __name__ == '__main__':
    greet_user()
    while True:
        query = take_user_input().lower()

        if 'open code' in query:
            open_vscode()

        elif 'open discord' in query:
            open_discord()

        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'open camera' in query:
            open_camera()

        elif 'open calculator' in query:
            open_calculator()

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
            print(f'Your IP Address is {ip_address}')

        elif 'wikipedia' in query:
            speak('What do you want to search on Wikipedia, sir?')
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            speak(f"According to Wikipedia, {results}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(results)

        elif 'youtube' in query:
            speak('What do you want to play on Youtube, sir?')
            video = take_user_input().lower()
            play_on_youtube(video)

        elif 'search on google' in query:
            speak('What do you want to search on Google, sir?')
            query = take_user_input().lower()
            search_on_google(query)

        elif "send whatsapp message" in query:
            speak('On what number should I send the message sir? Please enter in the console: ')
            number = input("Enter the number: ")
            speak("What is the message sir?")
            message = take_user_input().lower()
            send_whatsapp_message(number, message)
            speak("I've sent the message sir.")

        elif "send an email" in query:
            speak("On what email address do I send sir? Please enter in the console: ")
            receiver_address = input("Enter email address: ")
            speak("What should be the subject sir?")
            subject = take_user_input().capitalize()
            speak("What is the message sir?")
            message = take_user_input().capitalize()
            if send_email(receiver_address, subject, message):
                speak("I've sent the email sir.")
            else:
                speak("Something went wrong while I was sending the mail. Please check the error logs sir.")

        elif 'joke' in query:
            speak(f"Hope you like this one sir")
            joke = get_random_joke()
            speak(joke)
            speak("For your convenience, I am printing it on the screen sir.")
            pprint(joke)

        elif "advice" in query:
            speak(f"Here's an advice for you, sir")
            advice = get_random_advice()
            speak(advice)
            speak("For your convenience, I am printing it on the screen sir.")
            pprint(advice)

        elif "trending movies" in query:
            speak(f"Some of the trending movies are: {get_trending_movies()}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(*get_trending_movies(), sep='\n')

        elif 'news' in query:
            speak(f"I'm reading out the latest news headlines, sir")
            speak(get_latest_news())
            speak("For your convenience, I am printing it on the screen sir.")
            print(*get_latest_news(), sep='\n')

        elif 'weather' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"Getting weather report for your city {city}")
            weather, temperature, feels_like = get_weather_report(city)
            speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
            speak(f"Also, the weather report talks about {weather}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")

# REFERENCE
# 1. SAPI5 
# https://docs.microsoft.com/en-us/previous-versions/windows/desktop/ee125663(v=vs.85)