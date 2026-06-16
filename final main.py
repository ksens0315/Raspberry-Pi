AIoT 기반 실시간 외부인 침입 감지 및 원격 경보 시스템
(AIoT Real-time Intruder Detection & Remote Alarm System)

import cv2
from gpiozero import Buzzer, LED
import requests
import threading
import time

# ==========================================
# 1. 하드웨어 핀 번호 및 환경 변수 설정
# ==========================================
# 라즈베리파이 GPIO 핀 맵핑 (BCM 기준)
buzzerPin = Buzzer(16)  # 액티브 부저
redLed = LED(21)        # 경고용 빨간색 LED

# 텔레그램 봇 API 정보
TOKEN = "여기에_본인의_봇_토큰을_입력하세요"
CHAT_ID = "여기에_본인의_Chat_ID를_입력하세요"

# 중복 알람을 방지하기 위한 전역 상태 플래그
alarm_triggered = False  

# ==========================================
# 2. 클라우드 통신 함수 (Telegram API)
# ==========================================
def send_telegram_alert():
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        params = {'chat_id': CHAT_ID, 'text': '🚨 [보안 긴급] 시스템에 외부인 침입(얼굴)이 감지되었습니다!'}
        # HTTP GET 요청으로 텔레그램 서버에 메시지 전송
        requests.get(url, params=params)
    except Exception as e:
        print("텔레그램 전송 오류:", e)

# ==========================================
# 3. 메인 보안 시스템 루프
# ==========================================
def main():
    global alarm_triggered
    
    # 카메라 객체 초기화 (0 또는 -1은 기본 웹캠을 의미함)
    camera = cv2.VideoCapture(-1)
    
    # 연산 속도 향상을 위해 카메라 해상도를 640x480으로 고정
    camera.set(3, 640)
    camera.set(4, 480)
    
    # 머신러닝 기반 정면 얼굴 탐지 모델(XML) 로드
    face_xml = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(face_xml)
    
    print("시스템 준비 완료: 보안 모드가 활성화되었습니다.")
    print("종료하려면 영상 창이 활성화된 상태에서 키보드 'q'를 누르세요.")

    # 실시간 프레임 분석 무한 루프
    while(camera.isOpened()):
        # 카메라로부터 1장의 프레임(이미지) 읽기
        success, image = camera.read()
        if not success:
            break

        # 객체 탐지 연산량을 줄이기 위해 컬러(BGR) 영상을 흑백(Grayscale)으로 변환
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 이미지 내의 얼굴 검출 (얼굴 좌표 리스트 반환)
        # - scaleFactor: 이미지 피라미드 축소 비율
        # - minNeighbors: 객체로 판단하기 위한 최소 이웃 사각형 개수
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100,100))

        # ------------------------------------------
        # 침입자(얼굴) 감지 시 제어 로직
        # ------------------------------------------
        if len(faces) > 0: 
            # 감지된 모든 얼굴에 대해 빨간색 사각형(B, G, R = 0, 0, 255) 렌더링
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 3)
            
            # 1차 로컬 알람: 부저 소리와 LED 켜기
            buzzerPin.on()
            redLed.on()
            
            # 2차 원격 알람: 알람이 아직 울리지 않은 최초 1회에만 텔레그램 전송
            if not alarm_triggered:
                # 메인 루프를 방해하지 않도록 스레드를 분리하여 전송 시작
                threading.Thread(target=send_telegram_alert, daemon=True).start()
                alarm_triggered = True
                print("침입자 감지! 경보 작동 및 텔레그램 알림을 전송했습니다.")
                
        # ------------------------------------------
        # 정상 상태 유지 로직 (침입자 없음)
        # ------------------------------------------
        else: 
            buzzerPin.off()
            redLed.off()
            alarm_triggered = False # 다음 침입에 대비해 알람 상태 초기화
        
        # 처리된 결과 프레임을 화면에 출력
        cv2.imshow('AIoT Smart Security System', image)
        
        # 'q' 키를 누르면 무한 루프 탈출
        if cv2.waitKey(1) == ord('q'):
            print("보안 시스템을 안전하게 종료합니다.")
            break
            
    # 프로그램 종료 시 메모리 해제 및 하드웨어 핀 안전 상태(OFF) 전환
    camera.release()
    cv2.destroyAllWindows()
    buzzerPin.off()
    redLed.off()

# 스크립트가 직접 실행될 때만 main() 함수 호출
if __name__ == '__main__':
    main()
