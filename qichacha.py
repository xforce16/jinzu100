from selenium import webdriver
import time, re, os
from bs4 import BeautifulSoup
import json
import pymongo
from openpyxl import load_workbook

# 输入登录信息
username = '15310675140'
password = 'Taiping159'
client = pymongo.MongoClient("localhost", 27017)  # 链接MongoDB数据库


def get_company_info(file_name):
    target_company_name = []
    open_target = load_workbook(file_name)
    read_content = open_target.get_sheet_by_name('target')
    for row in read_content.rows:
        for col in row:
            target_company_name.append(col.value)
    return (target_company_name)


def open_browser(url):
    driver = webdriver.Chrome(executable_path='D:\\爬虫\\chromedriver_win32\\chromedriver.exe')
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)
    return driver


def log_in(driver):
    # 模拟登陆
    driver.find_element_by_xpath('//*[@id="nameNormal"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="pwdNormal"]').send_keys(password)
    time.sleep(10)
    driver.find_element_by_xpath('//*[@id="user_login_normal"]/button/strong').click()
    return driver


def search_company(driver, keyword):
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="searchkey"]').clear()
    driver.find_element_by_xpath('//*[@id="searchkey"]').send_keys(keyword)
    driver.find_element_by_xpath('//*[@id="V3_Search_bt"]').click()
    time.sleep(3)
    content = driver.page_source
    soup1 = BeautifulSoup(content, "html.parser")
    soup2 = soup1.find("table", {"class": "m_srchList"})
    companylist_source = soup2.findAll('tr')
    length = len(companylist_source)
    print(length)
    for i in range(0, length):
        historyname = ''
        sp = BeautifulSoup(str(companylist_source[i]), "html.parser")
        title = sp.find("a", {"class": "ma_h1"})
        text_re = re.search(r'(历史名称：)[^\x00-\xff]+', sp.text)
        if text_re:
            content01 = text_re.group()
            historyname = content01[5:]
        try:
            company_title = title.text
        except:
            company_title = ''
        if (company_title == keyword) or (historyname == keyword):
            href = BeautifulSoup(str(title), "html.parser")
            link = href.a['href']
            d = link.replace("/firm_", "").replace(".html", "")
            link_muhou = 'https://www.qichacha.com/company_muhou3?keyNo={}'.format(d)  # 关联图谱
            link_guquan = 'https://www.qichacha.com/company_guquan?keyNo={}'.format(d)  # 股权结构图
            link_touzhi = 'https://www.qichacha.com/company_relation?keyNo={}'.format(d)  # 投资族谱

            # 抓取关联图谱数据
            driver.get(link_muhou)
            html = driver.page_source
            data1 = re.search('>{(.*?)}<', html).group(0)
            d = data1.replace(">", "").replace("<", "")
            data = json.loads(d, encoding='utf-8')
            # 存入MongoDB数据库
            db = client.api
            posts = db.company_muhou3
            posts.insert_one(data)

            # 抓取股权结构图
            driver.get(link_guquan)
            html = driver.page_source
            data1 = re.search('>{(.*?)}<', html).group(0)
            d = data1.replace(">", "").replace("<", "")
            data = json.loads(d, encoding='utf-8')
            # 存入MongoDB数据库
            db = client.api
            posts = db.company_guquan
            posts.insert_one(data)

            # 抓取投资族谱
            driver.get(link_guquan)
            html = driver.page_source
            data1 = re.search('>{(.*?)}<', html).group(0)
            d = data1.replace(">", "").replace("<", "")
            data = json.loads(d, encoding='utf-8')
            # 存入MongoDB数据库
            db = client.api
            posts = db.company_relation
            posts.insert_one(data)


if __name__ == "__main__":
    file_name = "D:\\User Desktop\\ZHANGZHI\\桌面\\target.xlsx"
    keyword_list = get_company_info(file_name=file_name)
    url = 'https://www.qichacha.com/user_login'
    driver = open_browser(url)
    for keyword in keyword_list:
        search_company(driver, keyword)








