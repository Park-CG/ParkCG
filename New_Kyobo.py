from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import telepot
#시간 마다 알람 지정용
from apscheduler.schedulers.blocking import BlockingScheduler



options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)


time.sleep(2)



#Selenium 자동화_1. 사이트 접속하기
url = "https://product.kyobobook.co.kr/new/#?page=1&sort=new&year=2023&month=12&week=4&per=20&saleCmdtDvsnCode=KOR&gubun=newGubun&saleCmdtClstCode="
driver.get(url)

time.sleep(3)


driver.find_element(By.LINK_TEXT,'새로 나온 상품').click()
driver.find_element(By.XPATH,'//*[@id="tabBest03"]/div/div[1]/button/span[1]').click()
driver.find_element(By.LINK_TEXT,'중/고등참고서').click()


time.sleep(5)
#Selenium 자동화_2. 
# x_path = '//*[@id="topLayerQueryInput"]'
# searchbox = driver.find_element_by_xpath(x_path)
# searchbox.click()
# searchbox.send_keys("수능특강")
# searchbox.submit()
# element = driver.find_element_by_xpath('//*[@id="info-search"]/form/button')
# element.click()

#Selenium 자동화_3. '키워드' 입력하기
# element = driver.find_element_by_name("SearchText")
# element.send_keys("도와주세요")
#Selenium 자동화_4. 해당 키워드로 접속하기
# element.submit()

# #Selenium 자동화_5.  클릭하기
# m_morebox = driver.find_element_by_xpath('//*[@id="contents"]/div[6]/a')
# m_morebox.click()

# time.sleep(5)

#텔레그램 봇 생성
token = '6190243237:AAFZc7ImdbJ14OfN_hPoBBZReBTy_YOJXlE'
bot = telepot.Bot(token=token)

#스케줄러 생성
sched = BlockingScheduler()

#기존에 보냈던 링크를 담아둘 리스트
old_links = []

#링크 추출 함수 #새로운 게시글 정보만 보내기 위함
def extract_links(old_links=[]):
    
    ##Selenium 자동화_현재 열려 있는 웹사이트 새로고침(F5)하기
    driver.refresh()
    time.sleep(5)
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    search_result = soup.select('ol > li > div > div > div > div > div > a.prod_info')
    # news_list = search_result.select('.prod_info')
    print(search_result)

    links = []
    for news in search_result[:3]:
        link1 = news['href']
        # link = url + link
        links.append(link1)

    print(links)

    new_links=[]
    for link1 in links:
        if link1 not in old_links:
            new_links.append(link1)

    return new_links

#이전 링크를 매개변수로 받아서 비교 후, 새로운 링크만 출력
#차후 이 부분을 메세지 전송 코드로 변경하고 매시간 동작하도록 설정
#새로운 링크가 없다면 빈 리스트 반환
def send_links():
    global old_links
    new_links = extract_links(old_links)
    if new_links:
        for link1 in new_links:
            bot.sendMessage(chat_id='-792153356', text = link1) # yes24 신간방
            # bot.sendMessage(chat_id='-909878883', text = link)
    else:
        bot.sendMessage(chat_id='-792153356', text = '새글이 없습니다.') # yes24 신간방
        # bot.sendMessage(chat_id='-909878883', text = '새글이 없습니다.')
    old_links += new_links.copy()
    old_links = list(set(old_links))

#최초 시작
send_links()

#스케줄 설정
sched.add_job(send_links, 'interval', minutes = 0.5) # 특정 시간 간격으로 스케쥴 설정
# sched.add_job(send_links, 'cron', hour='10',minute='00', id='test') # 시간 지정해서 스케쥴 설정

#시작
sched.start()
