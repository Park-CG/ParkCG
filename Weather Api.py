import requests
import datetime
import telepot

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

def send_weather_info(nx, ny):
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
            value = rn1_pcp_category[int(value)]
            
        weather_info[category_name] = value

    # 텔레그램 봇으로 메시지 전송
    message = "오늘의 날씨 정보입니다(부산 동구)\n" + "\n".join([f"{k}: {v}" for k, v in weather_info.items()])
    bot.sendMessage(chat_id='-909878883', text=message)

# 날씨 정보 전송 함수 호출
# 위도와 경도를 원하는 값으로 설정하세요.
send_weather_info(98, 75)
