from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import telepot

app = Flask(__name__, static_url_path='/assets')

# Selenium 설정
options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
time.sleep(2)
url = "https://product.kyobobook.co.kr/new/#?page=1&sort=new&year=2023&month=12&week=4&per=20&saleCmdtDvsnCode=KOR&gubun=newGubun&saleCmdtClstCode="
driver.get(url)
time.sleep(3)
driver.find_element(By.LINK_TEXT,'새로 나온 상품').click()
driver.find_element(By.XPATH,'//*[@id="tabBest03"]/div/div[1]/button/span[1]').click()
driver.find_element(By.LINK_TEXT,'중/고등참고서').click()
time.sleep(5)

# 링크 추출 함수
def extract_links():
    driver.refresh()
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    search_result = soup.select('ol > li > div > div > div > div > div > a.prod_info')
    links = [news['href'] for news in search_result[:3]]
    return links

@app.route('/')
def home():
    links = extract_links()  # 새로운 책 링크를 얻습니다.
    return render_template('index.html', links=links)  # index.html에 결과를 보냅니다.

if __name__ == '__main__':
    app.run(debug=True)
