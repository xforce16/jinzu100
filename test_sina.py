#!usr/bin/env python
#-*- coding:utf-8 -*-

import requests
from urllib import parse
from lxml import etree
from pyquery import PyQuery as pq
import re

keyword = '上海石化'
base_url = 'https://search.sina.com.cn/?q={}&c=news&from=index&ie=gbk'.format(parse.quote(keyword.encode('gb2312')))

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN",
    "Connection": "keep-alive",
    "Cookie": "UOR=,finance.sina.com.cn,; ULV=1534845786251:1:1:1::; SINAGLOBAL=172.16.92.25_1534845786.467970; Apache=172.16.92.25_1534845786.467973; U_TRS1=000000a0.21c37a97.5b7be35a.2ed7630a; U_TRS2=000000a0.21cc7a97.5b7be35a.36e8f01d; lxlrttp=1532434326; hqEtagMode=0; WEB2_OTHER=f236fc0a92d2ce55e95e423abbb7978c; SSCSum=4",
    "DNT": "1",
    "Host": "search.sina.com.cn",
    "Referer": "https://search.sina.com.cn/?t=news",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.2.1.6000",
    "X-DevTools-Emulate-Network-Conditions-Client-Id": "dcf30bce-afd2-4781-a4e2-c0d985ee5007",
}



class NewsSpider():

    def __init__(self):
        pass


    def url_list(self):
        page = requests.get(url=base_url, headers=headers)
        # print(page.content.decode('gbk'))
        # page.encoding ='gbk'
        # html = etree.HTML(page.content)
        # selector = etree.tostring(html)
        # selector = etree.fromstring(selector)
        # url_list = selector.xpath('//div[@class="result"]//div[@class="box-result clearfix"]//h2/a@href')[0]
        # print(url_list)
        doc = pq(page.content.decode('gbk'))
        news_amount = doc('.l_v2').text()
        amount = re.search(r'\d+(,\d+)*',news_amount)
        print(int(amount.group(0).replace(',','')))
        url = doc('.r-info h2 a')
        print(url)
        print(type(url))
        url_list=[]
        for u in url.items():
            url_list.append(u.attr('href'))
        print(url_list)
        return url_list


    def parse_url(self,url_list):
        if url_list:
            for url in url_list:
                page = requests.get(url,headers=headers)




    def run(self):
        url_list = self.url_list()
        self.parse_url(url_list)


if __name__ == '__main__':
    news = NewsSpider()
    news.run()






