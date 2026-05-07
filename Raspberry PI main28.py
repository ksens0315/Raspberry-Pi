import requests                                                                        # 웹 요청 라이브러리
import re                                                                              # re 데이터 처리 라이브러리

url = "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4139054000"                       # OpenWeatherMap API 키
response = requests.get(url)

time = re.findall(r'<hour>(.+?)</hour>',response.text)                                 # 시간 목록 추출
temp = re.findall(r'<temp>(.+)</temp>',response.text)                                  # 기온 목록 추출
humi = re.findall(r'<reh>(.+?)</reh>',response.text)                                   # 습도 목록 추출
wfKor = re.findall(r'<wfKor>(.+?)</wfKor>',response.text)                              # 날씨 설명 목록 추출

print(time)                                                                            # 시간 출력
print(temp)                                                                            # 온도 출력
print(humi)                                                                            # 습도 출력
print(wfKor)                                                                           # 날씨 설명 출력
