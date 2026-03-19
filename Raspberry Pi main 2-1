from gpiozero import LEDBoard		# 'gpiozero' 라이브러리에서 'LEDBoard' 클래스를 가져옴
from time import sleep				# 'time' 라이브러리에서 'sleep' 함수를 가져옴

leds = LEDBoard(2,3,4,20,21)		# LEDBoard 클래스를 사용하여 다수의 LED를 초기화함 (하나의 객체로 관리)
									# 여기서는 핀 번호 2, 3, 4, 20, 21을 가진 다섯 개의 LED를 초기화함
try:
    while 1:						# 무한 루프 'while 1:' 시작되며, 이 루프에서는 아래의 동작을 반복함 (Lines 06 ~ 14)
        leds.value = (0,0,1,1,0)	# 'leds.value'를 설정하여 다섯 개의 LED를 동시에 제어함
        sleep(3.0)					# 각각의 숫자는 해당 LED의 상태를 나타냄 (0은 꺼짐, 1은 켜짐)
        leds.value = (0,1,0,1,0)	# LED 상태를 변경한 후에는 'sleep' 함수를 사용하여 대기 시간을 설정
        sleep(1.0)
        leds.value = (1,0,0,0,1)
        sleep(3.0)
    
except KeyboardInterrupt:			# 사용자가 Ctrl + C를 누를 때까지 코드를 실행하는 예외 처리 블록임
    pass							# 사용자가 Ctrl + C를 누르면 루프가 중단되고 코드 실행이 종료됨

leds.off()							# 코드 실행이 종료되면 모든 LED를 끔
