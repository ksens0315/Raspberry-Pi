from flask import Flask                        # 웹 서버 만드는 Flask 라이브러리
from gpiozero import LED                       # 라즈베리 파이 GPIO 핀 제어 라이브러리

app = Flask(__name__)                          # Flask 앱 생성

red_led = LED(21)                              # 21번 핀에 연결된 LED 설정

@app.route('/')                                # 기본 주소(/) 접속 시 실행
def flask():
   return "hello Flask"                        # 브라우저에 텍스트 출력

@app.route('/ledon')                           # /ledon 주소 접속 시 실행
def ledOn():
   red_led.on()                                # LED 켜기
   return "<h1> LED ON </h1> "                 # 브라우저에 결과 출력

@app.route('/ledoff')                          # /ledoff 주소 접속 시 실행
def LedOff():
   red_led.off()                               # LED 켜기      
   return "<h1> LED OFF </h1>"                 # 브라우저에 결과 출력

if __name__ == "__main__":
   app.run(host = "0.0.0.0", port = "80")      # 모든 IP(0.0.0.0)에서 80번 포트로 서버 실행
