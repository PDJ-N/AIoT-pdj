import urllib.request
import json
import datetime
import asyncio
from telegram import Bot

# 텔레그램 일기예보 알리미 프로젝트:
# OpenWeatherMap에서 서울의 3시간 단위 예보를 가져와 정해진 시간마다 텔레그램으로 전송한다.

# 실제 실행할 때는 각 서비스에서 발급받은 값으로 바꿔야 한다.
telegram_id = 'Enter your chat ID here'     # 메시지를 받을 텔레그램 채팅 ID
my_token = 'Enter your bot token here'      # BotFather에서 발급받은 텔레그램 봇 토큰
api_key = 'Enter your API key here'         # OpenWeatherMap API 키

bot = Bot(token=my_token)                   # 봇 토큰으로 메시지 전송 객체를 준비한다.

ALERT_HOURS = [7, 10, 13, 16, 19, 22]     # 오전 7시부터 3시간 간격으로 정각 알림을 보낸다.
ALERT_TIMES = ["08:30", "15:20"]          # 실습이나 추가 알림을 위해 직접 지정한 시각이다.

def getWeather():
    # cnt=8은 3시간 간격 예보 8개, 즉 약 하루치 서울 날씨 데이터를 요청한다.
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=en&cnt=8"

    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read())         # API 응답 JSON을 파이썬 자료형으로 바꿔 사용한다.

    text = ""
    for i in range(8):
        item = data['list'][i]              # 각 예보에는 시간, 기온, 습도, 날씨 설명이 들어 있다.
        hour = str((int(item['dt_txt'][11:13]) + 9) % 24).zfill(2)
        temp = item['main']['temp']
        humi = item['main']['humidity']
        desc = item['weather'][0]['description']
        text += f"({hour}h {temp}C {humi}% {desc})\n"   # 텔레그램에 보낼 한 줄 형태로 정리한다.

    return text

async def main():
    try:
        while True:
            now = datetime.datetime.now()
            hm = now.strftime('%H:%M')      # 현재 시간을 "시:분" 형식으로 만들어 지정 시간과 비교한다.

            # 정각 알림과 직접 지정한 알림 시간을 각각 확인한다.
            # second가 0일 때만 보내면 같은 분에 메시지가 여러 번 전송되는 일을 줄일 수 있다.
            is_alert_hour = now.hour in ALERT_HOURS and now.minute == 0 and now.second == 0
            is_alert_time = hm in ALERT_TIMES and now.second == 0

            if is_alert_hour or is_alert_time:
                msg = getWeather()          # 조건에 맞는 시간에 최신 예보 문자열을 만든다.
                print(msg)                  # 터미널에서도 전송 내용을 확인한다.
                await bot.send_message(chat_id=telegram_id, text=msg)

            await asyncio.sleep(1)          # 1초마다 시간을 다시 확인한다.

    except KeyboardInterrupt:
        pass                                # Ctrl+C로 종료해도 오류 메시지 없이 끝낸다.

asyncio.run(main())                         # 비동기 메인 루프를 실행한다.
