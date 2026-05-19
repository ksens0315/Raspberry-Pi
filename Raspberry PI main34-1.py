import cv2                       # 영상 처리 및 컴퓨터 비전 라이브러리(OpenCV) 불러오기
from gpiozero import Buzzer      # 라즈베리파이 GPIO 제어 모듈에서 부저(Buzzer) 클래스 불러오기
import time                      # 시간 관련 기능 모듈 불러오기

# 1. 하드웨어 핀 설정
buzzerPin = Buzzer(16)           # 16번 GPIO 핀에 연결된 부저(경보장치) 설정

def main():
    # 2. 카메라 초기 설정
    camera = cv2.VideoCapture(-1)  # 연결된 기본 카메라(-1 또는 0) 장치 활성화
    camera.set(3, 640)             # 카메라 영상의 가로 넓이(Width)를 640으로 설정
    camera.set(4, 480)             # 카메라 영상의 세로 높이(Height)를 480으로 설정
    
    # 3. 객체 탐지용 Haar Cascade 모델 불러오기
    face_xml = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml' # 정면 얼굴 탐지 모델 경로
    eye_xml = cv2.data.haarcascades + 'haarcascade_eye.xml'                  # 눈 탐지 모델 경로
    
    face_cascade = cv2.CascadeClassifier(face_xml) # 얼굴 탐지 분류기 객체 생성
    eye_cascade = cv2.CascadeClassifier(eye_xml)   # 눈 탐지 분류기 객체 생성
    
    # 4. 실시간 영상 프레임 처리 (무한 루프)
    while(camera.isOpened()):      # 카메라가 정상적으로 열려있는 동안 계속 반복
        _, image = camera.read()   # 카메라로부터 현재 순간의 프레임(이미지) 1장 읽어오기
        
        # 인식 속도와 정확도를 높이기 위해 컬러 영상(BGR)을 흑백 영상(GRAY)으로 변환
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

        # 5. 얼굴 객체 탐지
        # 변환된 흑백 영상에서 얼굴을 찾고, 얼굴이 있는 [x, y, 가로, 세로] 좌표값들을 반환
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100,100), flags=cv2.CASCADE_SCALE_IMAGE)
        print("faces detected Number: " + str(len(faces))) # 현재 화면에서 탐지된 얼굴의 개수를 터미널에 출력

        if len(faces):             # 화면에 탐지된 얼굴이 1개 이상 존재한다면
            for (x, y, w, h) in faces:
                # 원본 컬러 이미지에 탐지된 얼굴 영역을 파란색(255,0,0) 사각형(두께 2)으로 표시
                cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
                
                # 6. 눈 객체 탐지 (ROI: 관심 영역 설정)
                # 전체 화면이 아닌, '얼굴이 탐지된 영역' 내부로만 흑백/컬러 데이터를 잘라냄 (연산량 감소)
                face_gray = gray[y:y+h, x:x+w]     
                face_color = image[y:y+h, x:x+w]   
                
                # 잘라낸 얼굴 영역(face_gray) 안에서 눈을 탐지
                eyes = eye_cascade.detectMultiScale(face_gray, scaleFactor=1.1, minNeighbors=5)
                
                # 7. 졸음 감지 및 부저 제어 로직
                if len(eyes) <= 1: # 탐지된 눈이 1개 이하이면 (눈을 감았거나 깜빡임이 길어질 때)
                    buzzerPin.on() # 16번 핀 부저를 켜서 경고음 울림
                else:              # 눈이 정상적으로 2개 탐지되면
                    buzzerPin.off()# 부저를 끔
                
                # 얼굴 영역 이미지(face_color)에 탐지된 눈 영역을 초록색(0,255,0) 사각형으로 표시
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(face_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
        
        # 8. 최종 결과물 화면 출력
        cv2.imshow('result', image) # 사각형이 그려진 최종 프레임을 'result'라는 이름의 윈도우 창에 띄움
        
        # 'q' 키를 누르면 무한 루프 탈출
        if cv2.waitKey(1) == ord('q'): 
            break
    
    # 9. 프로그램 종료 및 자원 해제
    cv2.destroyAllWindows()        # 생성된 모든 OpenCV 윈도우 창 닫기
    buzzerPin.off()                # 프로그램이 종료될 때 부저 소리가 계속 나지 않도록 끔

# 이 파이썬 파일이 직접 실행될 때만 main() 함수 호출
if __name__ == '__main__':
    main()
