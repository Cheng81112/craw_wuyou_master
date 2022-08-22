# ecoding=utf-8
import requests


from bs4 import BeautifulSoup



def getHTMLtext(url):  # 解析  处理异常

    headers = {
        'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/69.0.3497.100 Safari/537.36',
        'Cookie': 'ZHID=CCC8B4400353A570033374E648EFDA0E; PassportCaptchaId=0f1e50ea3608e2d3024a51f53eee15c9; AST=1592249886067677c205d83; ver=2018; zh_visitTime=1592242687503; v_user=%7Chttp%3A%2F%2Fhuayu.zongheng.com%2Fbook%2F962248.html%7C20123841; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22172b90f4f4797-0d1cbcbbcf66ac-f313f6d-1049088-172b90f4f483f5%22%2C%22%24device_id%22%3A%22172b90f4f4797-0d1cbcbbcf66ac-f313f6d-1049088-172b90f4f483f5%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; zhffr=0; Hm_lvt_c202865d524849216eea846069349eb9=1592242688,1592242737; logon=NTI1MTg5Mjc%3D%7CMA%3D%3D%7C%7C5Lmm5Y%2BLNTg2OTMwNTc%3D%7CdHJ1ZQ%3D%3D%7CLTE2Njg4NjE5OTg%3D%7C95EA0D410A9AB3465EEF40A2C076F991; __logon__=NTI1MTg5Mjc%3D%7CMA%3D%3D%7C%7C5Lmm5Y%2BLNTg2OTMwNTc%3D%7CdHJ1ZQ%3D%3D%7CLTE2Njg4NjE5OTg%3D%7C95EA0D410A9AB3465EEF40A2C076F991; loginphone=15608113353; visit_list=52518927; Hm_lpvt_c202865d524849216eea846069349eb9=1592242779; Hm_up_c202865d524849216eea846069349eb9=%7B%22uid_%22%3A%7B%22value%22%3A%2252518927%22%2C%22scope%22%3A1%7D%7D'
    }
    r = requests.get(url, timeout=30, headers=headers)  # 发送请求

    r.raise_for_status()
    r.encoding = r.apparent_encoding  # 解析文本编码   可以套用

    return r.text  # 返回页面内容


# 获取每个页面的小说链接
def getpage_itemurl(html):  # 获得文本内容
    url_list = []
    soup = BeautifulSoup(html, "html.parser")

    # print(soup)#核心代码   寻找标签
    page = soup.find_all('div', 'bookimg')
    for bookimg in page:
        url_item = bookimg.find_all('a')[0].get('href')

        url_list.append(url_item)

    return url_list


# 获取每个小说的信息
import re


def getInformation(html):
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)#核心代码   寻找标签

    content = soup.find_all('div', 'book-info')

    bookname = content[0].find_all('div', 'book-name')[0].text

    bookname = re.findall(r'[\u4e00-\u9fa5]+', bookname)[0]

    classify = content[0].find_all('a', 'label')[0].text

    all = soup.find_all('div', 'nums')[0].find_all('i')
    # au_name =soup.find_all('div', 'au-name')[0].text #作者

    information = re.findall(r'\d+(?:\.\d+[\u4e00-\u9fa5]+)?', str(all))
    wordcount = information[0]
    all_recomm = information[1]
    click = information[2]
    # week_recomm = information[3]
    item = [bookname, classify, wordcount, all_recomm, click]

    return item


import csv


def get_data(page_url_list):
    file = open('data.csv', 'a', encoding='gbk', newline='')
    writer = csv.writer(file, dialect="excel")
    page = []
    for url1 in page_url_list:
        html = getHTMLtext(url1)

        information = getInformation(html)
        page.append(information)
    for i in page:
        writer.writerow((i[0],i[1],i[2],i[3],i[4]))


def main():


    for page in range(55, 72):  # 15页
        url = 'http://book.zongheng.com/store/c0/c0/b0/u1/p{0}/v9/s0/t0/u0/i1/ALL.html'.format(page)
        print(url)
        html = getHTMLtext(url)

        page_url_list = getpage_itemurl(html)

        get_data(page_url_list)
        print(page)


main()



