import speech_recognition as sr

# Recognizer 인스턴스 생성
r = sr.Recognizer()

# 마이크를 오디오 소스로 사용
with sr.Microphone() as source:
    print("마이크에 대고 말씀해보세요...")
    # 주변 소음 수준을 파악하여 인식을 보정합니다. (1초간)
    r.adjust_for_ambient_noise(source)
    # 마이크로부터 음성 입력을 받습니다.
    audio = r.listen(source)

# 구글 웹 음성 인식을 사용하여 텍스트로 변환 시도
try:
    # 한국어로 인식하도록 설정
    text = r.recognize_google(audio, language='ko-KR')
    print("인식된 텍스트: " + text)

except sr.UnknownValueError:
    print("음성을 인식할 수 없습니다. 소리가 너무 작거나 주변이 시끄럽지 않은지 확인해주세요.")

except sr.RequestError as e:
    print(f"구글 음성 인식 서비스에 연결할 수 없습니다; {e}")
    print("인터넷 연결을 확인하거나, API 키 설정을 확인해주세요.")