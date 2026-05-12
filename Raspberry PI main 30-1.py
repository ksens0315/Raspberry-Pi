import paho.mqtt.client as mqtt  # MQTT 통신 모듈 불러오기
import time                      # 시간 관련 기능 모듈 불러오기
from gpiozero import LED         # GPIO 제어 모듈에서 LED 클래스 불러오기
import threading                 # 두 작업을 동시에 처리하기 위한 스레드 모듈 불러오기

# 1. 하드웨어(LED) 핀 설정
greenLed = LED(16)               # 16번 GPIO 핀에 연결된 초록 LED 설정
blueLed = LED(20)                # 20번 GPIO 핀에 연결된 파란 LED 설정
redLed = LED(21)                 # 21번 GPIO 핀에 연결된 빨간 LED 설정

# 2. 메시지 수신 시 실행되는 콜백 함수 정의 (구독 동작)
def on_message(client, userdata, msg):
    # 수신된 토픽 이름과 바이트 데이터를 터미널에 1차 출력
    print(msg.topic + " " + str(msg.payload))
    
    # 수신된 바이트 데이터(예: b'green_on')를 일반 문자열('green_on')로 변환
    message = msg.payload.decode()
    print(message)               # 변환된 문자열 메시지를 터미널에 최종 출력
    
    # 수신된 문자열 조건에 맞춰 LED 제어
    if message == "green_on":         # 수신된 메시지가 "green_on"이면
        greenLed.on()                 # 16번 핀 초록 LED 켜기
    elif message == "green_off":      # 수신된 메시지가 "green_off"이면
        greenLed.off()                # 16번 핀 초록 LED 끄기
    elif message == "blue_on":        # 수신된 메시지가 "blue_on"이면
        blueLed.on()                  # 20번 핀 파란 LED 켜기
    elif message == "blue_off":       # 수신된 메시지가 "blue_off"이면
        blueLed.off()                 # 20번 핀 파란 LED 끄기
    elif message == "red_on":         # 수신된 메시지가 "red_on"이면
        redLed.on()                   # 21번 핀 빨간 LED 켜기
    elif message == "red_off":        # 수신된 메시지가 "red_off"이면
        redLed.off()                  # 21번 핀 빨간 LED 끄기

# 3. MQTT 클라이언트 설정 및 브로커 연결
client = mqtt.Client()                # MQTT 클라이언트 객체 생성
client.on_message = on_message        # 메시지 수신 시 위에서 정의한 on_message 함수가 실행되도록 연결

broker_address = "192.168.137.230"    # 브로커가 실행 중인 라즈베리파이의 IP 주소 설정
client.connect(broker_address)        # 설정한 IP 주소의 브로커에 연결
client.subscribe("led", 1)            # "led" 토픽 구독 등록, QoS 1로 설정 (메시지 최소 1회 수신 보장)

# 4. 백그라운드 메시지 발행 스레드 설정 (발행 동작)
count = 0                             # 발행할 숫자의 초기값을 0으로 설정

def send_thread():                    # 1초마다 메시지를 발행하는 스레드 함수 정의
    global count                      # 함수 외부에서 선언된 count 변수를 전역으로 사용 선언
    while 1:                          # 프로그램이 종료될 때까지 무한 반복
        count = count + 1             # count 값을 1씩 증가
        client.publish("hello", str(count))  # "hello" 토픽으로 count 값을 문자열로 변환하여 발행
        time.sleep(1.0)               # 1초 대기 후 다시 반복

task = threading.Thread(target=send_thread)  # send_thread 함수를 별도의 스레드로 생성
task.start()                                 # 스레드 시작, 이 순간부터 '발행'과 '구독'이 동시에 실행됨

# 5. 프로그램 종료 방지 및 통신 유지
client.loop_forever()                 # 메시지 수신을 위한 무한 대기 루프 실행 (프로그램이 종료되지 않고 계속 구독 유지)
