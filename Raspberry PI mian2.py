from gpiozero import LED			# 'gpiozero' 라이브러리에서 'LED' 클래스를 가져옴
from time import sleep				# 'time' 라이브러리에서 'sleep' 함수를 가져옴

carLedRed = 2						# 다양한 LED 핀의 핀 번호를 변수로 정의함 (lines 4 ~ 8)
carLedYellow = 3					# carLedRed, carLedYellow, carLedGreen, humanLedRed, humanLedGreen 변수에 각각 핀 번호를 할당
carLedGreen = 4					
humanLedRed = 20
humanLedGreen = 21

carLedRed = LED(2)					# 각 LED를 LED 클래스의 객체로 초기화하며, 핀 번호를 사용하여 LED 객체를 생성 (Lines 10 ~ 14)
carLedYellow = LED(3)
carLedGreen = LED(4)
humanLedRed = LED(20)
humanLedGreen = LED(21)

try:								# 무한 루프 ('while 1:') 를 시작, 이 루프에서는 아래의 동작을 반복함 (Lines 16 ~ 35)
    while 1:						# carLedRed, carLedYellow, carLedGreen, humanLedRed, humanLedGreen의 값을 조절하여 LED를 켜고 끔
        carLedRed.value = 0			# value 속성을 사용하여 1(점등) 또는 0(소등) 값을 설정
        carLedYellow.value = 0		# 각각의 LED를 제어하는 값에 따라 차량 및 보행자 신호등의 상태가 변경됨
        carLedGreen.value = 1		# sleep 함수를 사용하여 LED 상태가 변경된 후 대기 시간을 설정
        humanLedRed.value = 1
        humanLedGreen.value = 0
        sleep(3.0)
        carLedRed.value = 0
        carLedYellow.value = 1
        carLedGreen.value = 0
        humanLedRed.value = 1
        humanLedGreen.value = 0
        sleep(1.0)
        carLedRed.value = 1
        carLedYellow.value = 0
        carLedGreen.value = 0
        humanLedRed.value = 0
        humanLedGreen.value = 1
        sleep(3.0)
    
except KeyboardInterrupt:			# 사용자가 키보드 동작(Ctrl + C, SIGINT)을 사용하여 프로그램 실행을 종료할 때 발생시키는 예외 처리 블록임
    pass							# 사용자가 Ctrl + C를 누르면 루프가 중단되고 코드 실행이 종료됨

carLedRed.value = 0					# 코드 실행이 종료되면 모든 LED의 value값을 0으로 바꿔 모든 LED를 꺼줌 (Lines 40 ~ 44)
carLedYellow.value = 0
carLedGreen.value = 0
humanLedRed.value = 0
humanLedGreen.value = 0
