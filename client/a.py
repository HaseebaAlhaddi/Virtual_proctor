import speech_recognition as sr
import keyboard

r = sr.Recognizer()
while True:
    with sr.Microphone() as src:
        print('قل شيئًا...')
        audio = r.listen(src)

        try:
            t = r.recognize_google(audio, language='ar-AR')
            print(t)
        except sr.UnknownValueError as u:
            print(u)
        except sr.RequestError as r:
            print(r)

    if keyboard.is_pressed('q'):
        break