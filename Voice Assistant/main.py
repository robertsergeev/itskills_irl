import speech_recognition as sr
import webbrowser
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)  

yt_url = 'https://www.youtube.com/'


while(True):
    with sr.Microphone() as source:
        print("Слушаю: ")
        
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            print("Вы сказали: " + text)
            if(text == "Джарвис"):
                engine.say("Сэр да сэр!")
                engine.runAndWait()

            elif(text == "Открыть YouTube"):
                webbrowser.open(yt_url, new=0, autoraise=True)
                engine.say("Запускаю!")
                engine.runAndWait()
            

        except sr.UnknownValueError:
            print("Не удалось распознать речь!")
