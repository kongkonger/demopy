#coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import  By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import xlwt
# browser = webdriver.PhantomJS('E:/commontools/pctools/phantomjs-2.1.1-windows/bin/phantomjs')
browser = webdriver.Chrome()
WAIT = WebDriverWait(browser,10)
browser.set_window_size(1400,900)
book = xlwt.Workbook(encoding='utf-8',style_compression=0)

sheet = book.add_sheet("腾讯美女热舞视频",cell_overwrite_ok=True)
sheet.write(0,0,'名称')
sheet.write(0,1,'图片地址')
sheet.write(0,2,'视频网页')
sheet.write(0,3,'发布时间')


# sheet = book.add_sheet("蔡徐坤篮球",cell_overwrite_ok=True)
# sheet.write(0,0,'名称')
# sheet.write(0,1,'地址')
# sheet.write(0,2,'描述')
# sheet.write(0,3,'观看次数')
# sheet.write(0,4,'弹幕数')
# sheet.write(0,5,'发布时间')

n =1
def search():
    try:
        print('开始访问腾讯视频...')
        browser.get('https://v.qq.com/')

        input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#keywords')))
        # submit  = WAIT.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div[1]/div[1]/div/div[2]/div/form/div/button')))
        # .mod_search .search_btn
        submit  = WAIT.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div[1]/div[2]/form/button')))

        input.send_keys('美女热舞')
        submit.click()

        #跳转到新的窗口
        print('跳转到新窗口')
        all_h = browser.window_handles
        browser.switch_to.window(all_h[1])
        get_source()
        #
        # total = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,
        # "#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.last"
        # " > button")))
        total = 20
        return int(total)
    except TimeoutException:
        return search()


def next_page(page_num):
    try:
        print('获取下一页数据')
        # #等到底部的翻页  list.page-item.next  是对于ul元素的定位吗，没有看到list，是  li元素，可以用next定位下一个按钮
        # next_btn = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#all-list > div.flow-loader > div.page-wrap'
        #                                                                   ' > div > ul > li.page-item.next > button')))
        # next_btn.click()
        # # 等到底部的翻页显示出来的时候
        # WAIT.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#all-list > div.flow-loader > div.page-wrap > div '
        #                                                              '> ul > li.page-item.active > button'),str(page_num)))


        # 等到底部的翻页  list.page-item.next  是对于ul元素的定位吗，没有看到list，是  li元素，可以用next定位下一个按钮
        next_btn = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.mod_pages > a.page_next')))
        next_btn.click()
        # 等到底部的翻页显示出来的时候
        # a.page_num current  cmc !!!! a.page_num.current
        # WAIT.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'div.mod_pages > a.page_num.current'), str(page_num)))
        # cmc ！！！重要点 必须从顶部容器 到定位 到我们的元素，这样才可以找到 ！！！
        WAIT.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'div.search_container > div.wrapper > div.wrapper_main > div.mod_pages > span._items > a.page_num.current'), str(page_num)))
        get_source()
    except TimeoutException:
        browser.refresh()
        return next_page(page_num)

def save_to_excel(soup):
    #          find定位父级元素 class_属性            find_all定位item元素的 class_
    list = soup.find(class_='wrapper_main').find_all(class_ = 'result_item result_item_h _quickopen')
    for item in list:
        try:
            # cmc 判断属性是否存在 ！！！
            if (item.find(class_='desc_text') != None):
                item_title = item.find(class_='desc_text').get('title')
            else:
                item_title = item.find('img').get('alt')
            # item_title = item.find(class_ ='desc_text').get('title')
            item_img_link = item.find('img').get('src')
            item_video_link = item.find(class_ ='figure result_figure').get('href')

            # parent_item_date = item.find_parent(class_ ='info_item info_item_odd')
            item_dates =item.find_all(class_ ='content')
            item_date = item_dates[0].text
            # item_date = item.find(class_ ='info_item info_item_odd').find(class_ ='content').text
            #   find标签元素  get对应标签的属性名称的内容  title=
            # <a href="//www.bilibili.com/video/BV15b41157i4?from=search&amp;seid=13120563605744278563"
            # title="蔡徐坤原版无特效打篮球视频" target="_blank" class="img-anchor"><div class="img"><div class="lazy-img"><img alt="" src="//i2.hdslb.com/bfs/archive/96743ef8a99ff3ee5f637c30118c4f0c9c3e40d0.jpg@400w_250h.webp"></div><span class="so-imgTag_rb">01:11</span><div class="watch-later-trigger watch-later"></div><span class="mask-video"></span></div><!----></a>
            # item_title = item.find('img').get('alt')
            # item_link = item.find('img').get('src')
            # s对应标签中内容区  <div class="des hide">
            #       https://weibo.com/u/2365849183?refer_flag=1001030103_&amp;amp;is_hot=1
            #     </div>
            # item_dec = item.find(class_ = 'des hide').text
            # <span title="观看" class="so-icon watch-num"><i class="icon-playtime"></i>
            #         17.4万
            #       </span>
            # item_view = item.find(class_ = 'so-icon watch-num').text
            # <span title="弹幕" class="so-icon hide"><i class="icon-subtitle"></i>
            #         393
            #       </span>
            # item_biubiu = item.find(class_ = 'so-icon hide').text
            # <span title="上传时间" class="so-icon time"><i class="icon-date"></i>
            #         2019-04-17
            #       </span>
            # item_date = item.find(class_= 'so-icon time').text

            print('爬取: ' + item_title)
            global n

            sheet.write(n,0,item_title)
            sheet.write(n,1,item_img_link)
            sheet.write(n,2,item_video_link)
            sheet.write(n,3,item_date)
            # sheet.write(n,4,item_biubiu)
            # sheet.write(n,5,item_date)
            n = n + 1
        except Exception:
            n=n+1



def get_source():
    #  #all-list > div.flow-loader  标签tag为div，标签的class为flow-loader
    # WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#all-list > div.flow-loader > div.filter-wrap')))
    # WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#all-list > div.flow-loader > div.filter-wrap')))
    newSubmit = WAIT.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[1]/div/div[3]/a')))
    newSubmit.click()
    # cmc !!！
    WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.search_container > div.search_tools > div.mod_filter')))
    html = browser.page_source
    soup = BeautifulSoup(html,'lxml')
    print('到这')

    save_to_excel(soup)


def main():
    try:
        total = search()
        print(total)
         # for i in range(2, int(2)):
        # for i in range(2,int(total+1)):
        for i in range(2, int(10)):
            next_page(i)
    finally:
        browser.close()

if __name__ == '__main__':
    main()
    book.save('腾讯美女热舞视频.xls')

