

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import  Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import  BeautifulSoup
import  xlwt

browser = webdriver.Chrome()
WAIT = WebDriverWait(browser, 10)

def search():
    try:
        browser = webdriver.Chrome()

        WAIT =WebDriverWait(browser,10)
        browser.get("http://www.bilibili.com/")
        # 通过 #id  .class  和 标签名称找到元素
        inputdata = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#nav_searchform > input")))
        # 通过xml的 标签路径找到元素
        # submit = WAIT.until(EC.element_to_be_clickable((By.XPATH,
        # '/html/body/div[2]/div/div[1]/div/div[2]/div/form/div/button')))
        submit = WAIT.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[2]/div/div[1]/div[1]/div/div[2]/div/form/div/button')))
        inputdata.send_keys('蔡徐坤 篮球')
        submit.click()

        # 跳转到新的窗口
        print('跳转到新窗口')
        all_h = browser.window_handle

        browser.switch_to.window(all_h[1])
        # 第二页加载完成的标志
        WebDriverWait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#all-list > div.flow-loader'
                                                                              ' > div > ul > li.page-item.last > button')))
        get_source()
        #
        # total = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,
        #                                                    "#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.last > button")))
        # return int(total.text)
    except TimeoutError:
        return search()


search()


def get_source():
    WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#all-list > div.flow-loader > div.filter-wrap')))
    html = browser.page_source
    soup = BeautifulSoup(html,'lxml')
    print('soup data : ' +soup)