import urllib.request                                                         # 웹 요청 라이브러리 / Web request library
import json                                                                   # JSON 데이터 처리 라이브러리 / JSON data processing library 
import datetime                                                               # 날짜/시간 라이브러리 / Date and time library
import asyncio                                                                # 비동기 실행 라이브러리 / Asynchronous execution library 
from telegram import Bot                                                      # 텔레그램 봇 객체 / Telegram bot object

telegram_id = 'Enter your chat ID here'                                       # 내 텔레그램 chat_id / My Telegram chat ID
my_token = 'Enter your bot token here'                                        # BotFather에서 발급받은 토큰 / Bot token from BotFather 
api_key = 'Enter your API key here'                                           # OpenWeatherMap API 키 / OpenWeatherMap API key

bot = Bot(token=my_token)                                                     # 토큰으로 봇 객체 생성 / Create bot object with token

ALERT_HOURS = [7, 10, 13, 16, 19, 22]                                         # 3시간 간격 정각 알림 시간 목록 / Hourly alerts every 3 hours 
ALERT_TIMES = ["08:30", "14:45"]                                              # 추가 지정 시간 알림 목록 / Custom time alerts (add your times here)

def getWeather():                                                             # 날씨 정보를 가져와 문자열로 반환하는 함수 / Function to fetch weather and return as string 
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=en&cnt=8" # 서울 24시간 예보 URL / Seoul 24h forecast URL

    with urllib.request.urlopen(url) as r:                                     # API에 요청 보내기 / Send request to API
        data = json.loads(r.read())                                            # 응답을 JSON으로 변환 / Convert response to JSON

    text = ""                                                                  # 결과 문자열 초기화 / Initialize result string 
    for i in range(8):                                                         # 8개 시간대 순회 / Loop through 8 time slots 
        item = data['list'][i]                                                 # i번째 날씨 데이터 가져오기 / Get i-th weather data 
        hour = str((int(item['dt_txt'][11:13]) + 9) % 24).zfill(2)             # 시간 추출 후 KST 변환 (2자리 유지) / Extract hour and convert to KST (keep 2 digits) 
        temp = item['main']['temp']                                            # 기온 추출 / Extract temperature 
        humi = item['main']['humidity']                                        # 습도 추출 / Extract humidity 
        desc = item['weather'][0]['description']                               # 날씨 설명 추출 / Extract weather description 
        text += f"({hour}h {temp}C {humi}% {desc})\n"                          # 결과 문자열에 추가 / Append to result string

    return text                                                                # 완성된 날씨 문자열 반환 / Return completed weather string

async def main():                                                              # 비동기 메인 함수 / Async main function 
    try:
     while True:                                                               # 무한 반복 / Infinite loop
          now = datetime.datetime.now()                                        # 현재 시간 가져오기 / Get current time
          hm = now.strftime('%H:%M')                                           # 현재 시:분 추출 (예: "08:30") / Extract current HH:MM (e.g. "08:30")

          is_alert_hour = now.hour in ALERT_HOURS and now.minute == 0 and now.second == 0 # 정각 알림 조건 확인 / Check scheduled hour alert condition 
          is_alert_time = hm in ALERT_TIMES and now.second == 0                           # 지정 시간 알림 조건 확인 / Check custom time alert condition

          if is_alert_hour or is_alert_time:                                   # 두 조건 중 하나라도 해당되면 전송 / Send if either condition is met 
              msg = getWeather()                                               # 날씨 정보 가져오기 / Fetch weather info 
              print(msg)                                                       # 터미널에 출력 / Print to terminal 
              await bot.send_message(chat_id=telegram_id, text=msg)            # 텔레그램으로 메시지 전송 / Send message to Telegram

            await asyncio.sleep(1)                                             # 1초 대기 후 반복 / Wait 1 second before next check

      except KeyboardInterrupt:                                                # Ctrl+C 입력 시 정상 종료 / Exit gracefully on Ctrl+C 
          pass

asyncio.run(main())                                                            # 비동기 메인 함수 실행 / Run async main function
