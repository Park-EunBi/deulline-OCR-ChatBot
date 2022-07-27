from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def tvCrawling():
    driver = set_chrome_driver()
    driver.implicitly_wait(time_to_wait=5)

    url = "https://www.e-himart.co.kr/"
    driver.get(url)
    driver.implicitly_wait(time_to_wait=5)

    d_url = driver.page_source
    soup = BeautifulSoup(d_url, 'html.parser')
    time.sleep(5)

    #TV/냉장고/세탁기/건조기 카테고리로 이동
    menu = driver.find_element(By.XPATH, '//*[@id="header"]/div[3]/div/div[2]/div/div/ul/li[1]/a')
    ActionChains(driver).click(menu).perform()
    driver.implicitly_wait(time_to_wait=10)

    #TV/영상가전 카테고리로 이동
    menu2 = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[5]/a[1]')
    ActionChains(driver).click(menu2).perform()
    driver.implicitly_wait(time_to_wait=10)

    #TV 카테고리로 이동
    menu3 = driver.find_element(By.XPATH, '//*[@id="displayForm"]/div[2]/div[1]/div/ul/li[1]/a')
    ActionChains(driver).click(menu3).perform()
    driver.implicitly_wait(time_to_wait=30)

    #페이지 별 상품 url 수집 ... 한 페이지에 40갠데 28개만 뜬다 왜지? 확인하기
    tv_prdList = soup.findAll("a", {"class": "prdLink"})
    tv_linkList = []
    for prd in tv_prdList:
        prd_link = prd['href']
        prd_link = 'https://www.e-himart.co.kr' + prd_link
        tv_linkList.append(prd_link)
    print(tv_linkList)
    print(len(tv_linkList))

    #페이지 돌면서 상품 정보 수집
    for link in tv_linkList:
        driver.get(link)
        driver.implicitly_wait(time_to_wait=30)

        d_url = driver.page_source
        soup = BeautifulSoup(d_url, 'html.parser')
        time.sleep(5)

        #상품명, 가격 수집
        tv_prdName = soup.find("h2").get_text()
        tv_prdPrice = soup.find("span", {"class": "price"}).get_text()
        print(tv_prdName, " / ", tv_prdPrice)

tvCrawling()