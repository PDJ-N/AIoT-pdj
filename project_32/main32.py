import speech_recognition as sr

try:
    while True :
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
            
        try:
            text = r.recognize_google(audio, language='ko-KR')
            print("You said: " + text)
            if text in "날씨":
                print("날씨 음성을 인식하였습니다.")
            
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

except KeyboardInterrupt:
    pass