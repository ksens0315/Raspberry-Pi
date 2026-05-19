import speech_recognition as sr  # 음성 인식(STT) 라이브러리 불러오기
import requests                  # 기상청 RSS 서버에 HTTP 요청을 보내기 위한 라이브러리 불러오기
import re                        # XML 데이터에서 온습도를 추출하기 위한 정규표현식 모듈 불러오기
import os                        # 시스템 명령어(espeak tts)를 실행하기 위한 모듈 불러오기
import time                      # 시간 관련 기능 모듈 불러오기

# 기상청 동네예보 RSS URL 설정 (특정 지역 격자 좌표 데이터)
url = "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4139054000"

# 리눅스 espeak 명령어를 사용해 문자열을 음성으로 출력(TTS)하는 함수 정의
def speak(option, msg):
    # os.system을 통해 터미널에 "espeak 옵션 '메시지'" 명령어를 전달하여 실행
    os.system("espeak {} '{}'".format(option, msg))

try:
    while True:
        r = sr.Recognizer()      # 구글 음성 인식을 위한 인스턴스(객체) 생성
        
        # 마이크를 음성 입력 소스로 설정
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)  # 마이크로부터 주변 소리를 듣고 수음 데이터 저장
            
        try:
            # 구글 웹 API를 이용하여 한국어(ko-KR)로 음성을 텍스트로 변환(STT)
            text = r.recognize_google(audio, language='ko-KR')
            print("You said: " + text)  # 변환된 텍스트 결과를 터미널에 출력
            
            # 변환된 텍스트에 "날씨"라는 단어가 포함되어 있다면
            if text in "날씨":
                print("날씨 음성을 인식하였습니다.")
                
                # 1. 기상청 RSS 서버에 날씨 데이터 요청 (HTTP GET)
                response = requests.get(url)
                
                # 2. 정규표현식을 이용해 XML 태그 데이터 추출
                temp = re.findall(r'<temp>(.+)</temp>', response.text)  # <temp> 태그 안의 온도 값 추출
                humi = re.findall(r'<reh>(.+)</reh>', response.text)    # <reh> 태그 안의 습도 값 추출
                
                # 3. 음성으로 출력할 안내 메시지 문자열 생성 (온도의 소수점 이하는 절삭)
                msg = '    기온은 ' + temp[0].split('.')[0] + '도 습도는 ' + humi[0] + '퍼센트 입니다'
                
                # 4. espeak 설정 옵션 (속도 180, 음높이 50, 음량 200, 한국어 여성 5번 목소리)
                option = '-s 180 -p 50 -a 200 -v ko+f5'
                speak(option, msg)  # 설정한 옵션과 메시지로 음성 출력 함수 실행
            
        # 구글 음성 인식기가 소리를 정상적으로 말소리로 분별하지 못했을 때의 예외 처리
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        # 네트워크 단절 등 구글 서버에 요청을 보낼 수 없을 때의 예외 처리
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

# 사용자가 Ctrl + C를 눌러 프로그램을 강제 종료했을 때 에
