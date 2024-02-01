import requests
import datetime
import telepot
import pandas as pd
import time

# 텔레그램 봇 생성
token = '6190243237:AAFZc7ImdbJ14OfN_hPoBBZReBTy_YOJXlE'
bot = telepot.Bot(token=token)

# 코드값과 범주를 텍스트로 변환하는 딕셔너리 생성
sky_code = {1: '맑음', 3: '구름많음', 4: '흐림'}
pty_code = {0: '없음', 1: '비', 2: '비/눈', 3: '눈', 5: '빗방울', 6: '빗방울눈날림', 7: '눈날림', 4: '소나기'}
rn1_pcp_category = {0: '없음', 1: '1mm 미만', 2: '1mm 이상'}

# 항목값과 항목명을 매핑하는 딕셔너리 생성
category_names = {
    'POP': '강수확률',
    'PTY': '강수형태',
    'PCP': '1시간 강수량',
    'REH': '습도',
    'SNO': '1시간 신적설',
    'SKY': '하늘상태',
    'TMP': '1시간 기온',
    'TMN': '일 최저기온',
    'TMX': '일 최고기온',
    'UUU': '풍속(동서성분)',
    'VVV': '풍속(남북성분)',
    'WAV': '파고',
    'VEC': '풍향',
    'WSD': '풍속',
    'T1H': '기온',
    'RN1': '1시간 강수량',
    'LGT': '낙뢰',
}

# 엑셀 파일 읽기
df = pd.read_excel("C:\\Users\\ckdrb\\OneDrive\\Desktop\\Works\\Weather\\grid.xlsx")

# 행정구역과 격자 좌표 매핑
location_to_grid = {row['2단계']: (row['격자 X'], row['격자 Y']) for idx, row in df.iterrows()}

# 사용자의 메시지를 처리하는 함수
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        location = msg['text']
        # 이 부분에 위치의 격자 좌표를 반환하는 코드를 추가해 주세요.
        nx, ny = location_to_grid[location]
        send_weather_info(nx, ny, chat_id, location)

# 날씨 정보를 전송하는 함수
def send_weather_info(nx, ny, chat_id, location):
    # 오늘 날짜를 YYYYMMDD 형태로 변환
    today = datetime.date.today()
    date_str = today.strftime("%Y%m%d")

    # 기상청 API 주소
    url = f"https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst?serviceKey=wZKiRIqUYJ3V9BBhOr%2BN1%2FPKsUGmKaSWriqLu44kZGh5gduL0FEosF9ttkkmOrZp8qC5DPto3o5Uv5NpGaCBnw%3D%3D&pageNo=1&numOfRows=1000&dataType=JSON&base_date={date_str}&base_time=0600&nx={nx}&ny={ny}"

    # API 요청
    response = requests.get(url)
    data = response.json()

    # 날씨 정보 추출
    weather_info = {}
    for item in data['response']['body']['items']['item']:
        category = item['category']
        value = item['obsrValue']

        # 항목값을 항목명으로 변환
        category_name = category_names.get(category, category)
        if category == 'PTY':
            value = pty_code[int(value)]
        elif category == 'SKY':
            value = sky_code[int(value)]
        elif category in ['RN1', 'PCP']:
            value = rn1_pcp_category[int(float(value))]
            
        weather_info[category_name] = value

    # 텔레그램 봇으로 메시지 전송
    message = f"{location}의 오늘의 날씨 정보입니다.\n" + "\n".join([f"{k}: {v}" for k, v in weather_info.items()])
    bot.sendMessage(chat_id=chat_id, text=message)

# 봇에 메시지 핸들러 설정
bot.message_loop(handle)

# 이 부분이 무한루프를 생성하여 봇이 계속 실행될 수 있도록 합니다.
while True:
    time.sleep(10)
