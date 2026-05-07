import urllib.request                                                                     # 웹 요청 라이브러리
import json                                                                               # JSON 데이터 처리 라이브러리

api_key = 'Enter your API key here'                                                       # OpenWeatherMap API 키

url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=en&cnt=8" # 서울 24시간 예보 URL

with urllib.request.urlopen(url) as r:                                                    # API에 요청 보내기 
data = json.loads(r.read())                                                               # 응답을 JSON으로 변환

text = ""                                                                                 # 결과 문자열 초기화 
for i in range(8):                                                                        # 8개 시간대 순회 
item = data['list'][i]                                                                    # i번째 날씨 데이터 가져오기 
hour = item['dt_txt'][11:13]                                                              # 시간 추출 (예: "07") 
temp = item['main']['temp']                                                               # 기온 추출 
humi = item['main']['humidity']                                                           # 습도 추출 
desc = item['weather'][0]['description']                                                  # 날씨 설명 추출 
text = text + "(" + str(hour) + “h "                                                       
text = text + str(temp) + "C "                                                            # 기온 추가 
text = text + str(humi) + "% "                                                            # 습도 추가 
text = text + str(desc) + ")"                                                             # 날씨 설명 추가

print(text)                                                                               # 완성된 날씨 문자열 출력
