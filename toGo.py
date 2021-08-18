from selenium import webdriver
import time
# from selenium.common.exceptions import UnexpectedAlertPresentException
import os
import telegram
from dotenv import load_dotenv

# 텔레그램 봇 토큰
load_dotenv(verbose=True)
my_token = os.getenv('TELEGRAM_TOKEN')

# 이전 재고 저장해서 이전 재고가 0 이었을 때만 알림
pre_stock = '0'


# Mac 알림
def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}" sound name "default"'
              """.format(text, title))


if __name__ == "__main__":
    # 텔레그램 봇 설정
    bot = telegram.Bot(token=my_token)
    updates = bot.getUpdates()
    chat_id = bot.getUpdates()[-1].message.chat.id
    # notify("Hello world", "test")
    # bot.sendMessage(chat_id=chat_id, text="test 봇입니다" + pre_stock + "\n" + url)

    # open Browser
    url = "https://www.galaxytogo.co.kr/reservation/step1/"
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)

    # 제품 선택 4: Fold 3
    product_button = driver.find_element_by_xpath("//div[@class='frm']/ul/li[4]")
    product_button.click()
    time.sleep(1)

    # 팝업창 확인
    try:
        time.sleep(1)
        driver.switch_to.alert.accept();
    except:
        pass

    # 지역 선택 a[4] 경상/제주
    location_button = driver.find_element_by_xpath("//div[@class='location']/a[4]")
    location_button.click()
    time.sleep(1)

    while (True):
        try:
            # refresh
            driver.refresh()
            time.sleep(2)

            # 매장 재고 확인 li[2] 대구
            stock_num = driver.find_element_by_xpath("//div[@class='store_list']/ul/"
                                                     "li[2]/p/strong").text
            # print(stock_num[0])
            if stock_num[0] != '0' and pre_stock == '0':
                notify("Fold 3 재고 입고", stock_num)
                bot.sendMessage(chat_id=chat_id, text="Fold 3 재고 입고 재고 : " + stock_num + "\n" + url)

            pre_stock = stock_num[0]
        except:
            print("ERROR")
            continue
