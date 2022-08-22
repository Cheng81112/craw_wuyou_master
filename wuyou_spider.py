"""
思路：
一、数据来源分析
    数据内容，通过开发者工具抓包分析
    分析数据是分析服务器返回的数据内容，不是元素面板
二、代码实现
    1.发送请求，对于找到分析得到的url地址发送请求
    2.获取数据，获取服务器返回的response响应数据
    3.解析数据，提取我们想要的内容
    4.保存数据，保存到本地文件

"""

# 导入数据请求模块
import requests
# 正则表达式模块
import re
# 导入json模块
import json
# 导入数据格式化模块
import pprint
# 导入csv模块
import csv
# 导入时间模块
import time
import pymysql
import pandas as pd



print('连接到mysql服务器...')

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='685568',
                       db='recruitment_info', port=3306, charset='utf8')
print('数据库连接成功!')
cur = conn.cursor()

# # 判断表是否存在，若存在则删除此表
# cur.execute("DROP TABLE IF EXISTS INFORMATION")
# #创建表
# sql = """CREATE TABLE INFORMATION(
#             pos varchar(255) ,
#             company varchar(255),
#             city varchar(255),
#             exp varchar(255),
#             fuli varchar(255),
#             shijian varchar(255),
#             guimo varchar(255),
#             yewu varchar(255),
#             leixing varchar(255),
#             href varchar(255))
#         """
#
# try:#如果出现异常对异常处理
#     # 执行SQL语句
#     cur.execute(sql)
#     print("创建数据库表成功")
# except Exception as e:
#     print("创建数据库失败：case%s" % e)

# 保存数据
f = open('招聘信息1.csv', mode='a', encoding='utf-8', newline='')
csv_write = csv.DictWriter(f, fieldnames=[
    '职位名称',
    '公司名称',
    '所在城市',
    '经验要求',
    '公司福利',
    '发布时间',
    '公司规模',
    '业务范围',
    '公司类型',
    '详情页面'
])
csv_write.writeheader()  # 写入表头

# 1.发送请求，对于找到分析得到的url地址发送请求

position = input("请输入你想搜索的职位信息：")

# 确定请求的url地址
for page in range(25, 30):
    print(f"===============正在爬取第{page}页的内容================")


    url = f'https://search.51job.com/list/000000,000000,0000,00,9,99,{position},2,{page}.html'

    # header请求头
    headers = {
        'Cookie':'_uab_collina=166089544909110744184897; acw_tc=ac11000116608954467954972e00de0e24b7a7a70f945ad9090059e59a7556; guid=48fd9fd049c1b5aebb96ed0af24e7d0b; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; search=jobarea%7E%60000000%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22182b5154e0680-04ee3b22e7e8f6c-26021d51-1382400-182b5154e073a2%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgyYjUxNTRlMDY4MC0wNGVlM2IyMmU3ZThmNmMtMjYwMjFkNTEtMTM4MjQwMC0xODJiNTE1NGUwNzNhMiJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22182b5154e0680-04ee3b22e7e8f6c-26021d51-1382400-182b5154e073a2%22%7D; ssxmod_itna=QqfxRDyD2D0GYxxl4iwbfD9mODCDgiir6m=Yh0Gx0v4heGzDAxn40iDtorTcE800DxNYF=lm+rQFZhTdpLlZOcRsbDCPGnDB9DqbSYxiiBDCeDIDWeDiDG4Gm94GtDpxG=Djjtz1M6xYPDEjKDaxDbDin8pxGCDeKD0oTFDQKDu6FKD6K+O2Y1W3yDYfG4LxG1F40HeA3qLxgf6RGzYt8ExUbODl9UDCI1n6yFW4GdU2y1x3hxWjbublT7enRD3D4PQQiKWWhdo7iuemhyk7hi+GrnfuDDip2efQGDD=; ssxmod_itna2=QqfxRDyD2D0GYxxl4iwbfD9mODCDgiir6m=Yh0DnIfxaKDseGDLB/OV4LiuiVIgqQqnDn4NPYK8mHKp3B1eOjQeQIEq6m0/ij7==0Ri2Y4RkEQGBgxQ7DLAP8dnfQzK81l66AAlv6Lql873BA7=+BuDCW7D6+gYs3+rM+4oMCn5q4LY+9utXUniwbebXbntRSLUrHpTlt3d/CQbFd+9KsetXiGao1QjsZpnhMWHoo8r7meo3FIo1g2544Ovz/oKIcfqLZrXvN+I2SIIxWGCPAGDnh8HkAgw4CXHtxK7UvWdCQ0DBAv/uaeSoLDZY1P56loBnmqRqD60y6pZCQ67d4ADLnoPimq74qZdme0qr3CGEjnEzomk1356UkPPHAp/hbb=612jjAbPCb=iqH+rImAOUrIBiaDG2zqDFqD+ZKNQIvnY4YD==',
        # 'Host': 'search.51job.com',
        # 'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                      '/104.0.0.0 Safari/537.36'
    }

    # 通过requests模块的里面get请求方法，对于url地址发送请求，并且携带上headers请求头 用变量接收数据
    time.sleep(4)
    response = requests.get(url=url, headers=headers, verify=False)

    # 2.获取数据  获取服务器返回的reponse相应数据（文本数据）
    # print(response.text) # 字符串数据，re正则可以直接对于字符串数据进行提取
    # 3.解析数据   .*?匹配任意字符（除了换行符以外）
    # 正则表达式返回数据是列表类型   根据列表的索引位置提取内容
    # print(response.text)
    html_data = re.findall('window.__SEARCH_RESULT__ = (.*?)</script>', response.text)[0]
    # print(html_data)
    # 字符串数据转换为字典数据类型   因为字典提取数据更加方便
    json_data = json.loads(html_data)
    # IndexError: list index out of range  报错原因：因为正则没有提取到数据内容  返回空列表[]
    # json数据取值，根据冒号左边内容提取冒号右边内容
    engine_jds = (json_data['engine_jds'])

    # 提取出来返回列表，列表一个一个提取元素  用for循环遍历
    for index in engine_jds:
        # 为了方便保存数据，提取出来的数据内容可以用字典接收
        href = f'https://jobs.51job.com/chengdu-jnq/{index["jobid"]}.html'
        dic = {
            '职位名称': index['job_name']  ,
            '公司名称': index['company_name'],
            '所在城市': index['attribute_text'][0],
            '经验要求': index['attribute_text'][1],
            '公司福利': index['jobwelf'],
            '发布时间': index['updatedate'],
            '公司规模': index['companysize_text'],
            '业务范围': index['companyind_text'],
            '公司类型': index['companytype_text'],
            '详情页面': href,
        }
        # pprint.pprint(index)
        csv_write.writerow(dic)
        # print(dic)


        # sql = """insert into INFORMATION values{}""".format(data)

        sql = 'INSERT INTO INFORMATION(pos,company,city,exp,fuli,shijian,guimo,yewu,leixing,href) VALUES ' \
              '("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(dic['职位名称'], dic['公司名称'], dic['所在城市'],
                         dic['经验要求'], dic['公司福利'], dic['发布时间'],
                         dic['公司规模'], dic['业务范围'], dic['公司类型'],
                         dic['详情页面'])
        print(sql)
        # try:
        cur.execute(sql)
        conn.commit()  # 进行数据库提交，写入数据库

# 关闭游标
cur.close()
# 提交
conn.commit()
# 关闭数据库连接
conn.close()
# 成功爬取数据并写入数据库
print("")
print("Done! ")
print("恭喜你！数据爬取结束。")





