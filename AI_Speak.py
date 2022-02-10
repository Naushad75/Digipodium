import pyttsx3
#import speech_recognition as sr

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices)
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

speak("Naushad is a good boy")    
#if __name__ == "__main__":
#    speak("Naushad is a good boy")

def takecommand():
    command = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        command.pause_threshold = 1
        audio = command.listen(source)

        try:
            print("Recognizing...")
            query = command.recognize_google(audia,language='en-in')
            print(f"You Said : {query}")
            
        except Exception as Error:
            return "None"

        return query.lower()

query = takecommand()

if 'hello' in query:
    speak("hello sir")

else:
    speak("no command found")
