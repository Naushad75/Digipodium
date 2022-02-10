from math import degrees
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib


print("Initializing Jarvis")

MASTER = "Naushad"
engine = pyttsx3.init('sapi5')
voice = engine.getProperty('voice')
engine.setProperty('voice', voice)


# Speak function will pronounce the string which is passed to it
def speak(text):
    engine.say(text)
    engine.runAndWait()

# This function will wish you as per the corrent time
def wishMe():
    hour = int(datetime.datetime.now().hour)
    print(hour)

    if hour >=0 and hour <12:
        speak("Good Morning" + MASTER)

    elif hour >=12 and hour <16:
        speak("Good Afternoon" + MASTER)

    else :
        speak("Good Night" + MASTER)

    speak("I am jarvis, How may I help you?")

# This Function will take commend from the microphone
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listining...")
        audio = r.listen(source)

    try:
        print("Recogining...")
        query = r.recognize_google(audio, Language = 'en-in')
        print(f"user said: {query}\n")

    except Exception as e:
        print("Say that again please")

# Main program start hear...
speak("Initilizing Jarvis...")
wishMe()
takeCommand()