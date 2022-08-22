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
# 导入数据解析模块
import parsel
# 导入pdf模块
import pdfkit
# 导入文件操作模块
import os
import random
html_str = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<body>
{article}
</body>
</html>
"""

# 保存数据
f = open('招聘信息1.csv', mode='a', encoding='utf-8', newline='')
csv_write = csv.DictWriter(f,fieldnames=[
    '职位名称',
    '公司名称',
    '所在城市',
    '经验要求',
    '学历要求',
    '公司福利',
    '工作薪资',
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
for page in range(4, 5):
    print(f"===============正在爬取第{page}页的内容================")
    time.sleep(3)

    url = f'https://search.51job.com/list/000000,000000,0000,00,9,99,{position},2,{page}.html'

    # header请求头
    headers = {
        'Cookie': '_uab_collina=166089544909110744184897; acw_tc=ac11000116608954467954972e00de0e24b7a7a70f945ad9090059e59a7556; guid=48fd9fd049c1b5aebb96ed0af24e7d0b; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; search=jobarea%7E%60000000%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22182b5154e0680-04ee3b22e7e8f6c-26021d51-1382400-182b5154e073a2%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgyYjUxNTRlMDY4MC0wNGVlM2IyMmU3ZThmNmMtMjYwMjFkNTEtMTM4MjQwMC0xODJiNTE1NGUwNzNhMiJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22182b5154e0680-04ee3b22e7e8f6c-26021d51-1382400-182b5154e073a2%22%7D; ssxmod_itna=QqfxRDyD2D0GYxxl4iwbfD9mODCDgiir6m=Yh0Gx0v4heGzDAxn40iDtorTcE800DxNYF=lm+rQFZhTdpLlZOcRsbDCPGnDB9DqbSYxiiBDCeDIDWeDiDG4Gm94GtDpxG=Djjtz1M6xYPDEjKDaxDbDin8pxGCDeKD0oTFDQKDu6FKD6K+O2Y1W3yDYfG4LxG1F40HeA3qLxgf6RGzYt8ExUbODl9UDCI1n6yFW4GdU2y1x3hxWjbublT7enRD3D4PQQiKWWhdo7iuemhyk7hi+GrnfuDDip2efQGDD=; ssxmod_itna2=QqfxRDyD2D0GYxxl4iwbfD9mODCDgiir6m=Yh0DnIfxaKDseGDLB/OV4LiuiVIgqQqnDn4NPYK8mHKp3B1eOjQeQIEq6m0/ij7==0Ri2Y4RkEQGBgxQ7DLAP8dnfQzK81l66AAlv6Lql873BA7=+BuDCW7D6+gYs3+rM+4oMCn5q4LY+9utXUniwbebXbntRSLUrHpTlt3d/CQbFd+9KsetXiGao1QjsZpnhMWHoo8r7meo3FIo1g2544Ovz/oKIcfqLZrXvN+I2SIIxWGCPAGDnh8HkAgw4CXHtxK7UvWdCQ0DBAv/uaeSoLDZY1P56loBnmqRqD60y6pZCQ67d4ADLnoPimq74qZdme0qr3CGEjnEzomk1356UkPPHAp/hbb=612jjAbPCb=iqH+rImAOUrIBiaDG2zqDFqD+ZKNQIvnY4YD==',
        # 'Host': 'search.51job.com',
        # 'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                      '/104.0.0.0 Safari/537.36'
    }

    # 通过requests模块的里面get请求方法，对于url地址发送请求，并且携带上headers请求头 用变量接收数据
    response = requests.get(url=url, headers=headers, verify=False)

    # 2.获取数据  获取服务器返回的reponse相应数据（文本数据）
    # print(response.text) # 字符串数据，re正则可以直接对于字符串数据进行提取
    # 3.解析数据   .*?匹配任意字符（除了换行符以外）
    # 正则表达式返回数据是列表类型   根据列表的索引位置提取内容
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
            '职位名称': index['job_name'],
            '公司名称': index['company_name'],
            '所在城市': ','.join(index['providesalary_text']),
            '经验要求': index['attribute_text'][1],
            '学历要求': index['attribute_text'][2],
            '公司福利': index['jobwelf'],
            '工作薪资': index['providesalary_text'],
            '发布时间': index['updatedate'],
            '公司规模': index['companysize_text'],
            '业务范围': index['companyind_text'],
            '公司类型': index['companytype_text'],
            '详情页面': href,
        }
        # pprint.pprint(index)
        csv_write.writerow(dic)
        # print(dic)



        # 1.发送请求头
        # url = 'https://jobs.51job.com/chengdu/141296604.html'
        url = href
        # header请求头

        headers = {
            # 也可以每请求十次，重新获取一次cookie
            'Cookie': '_uab_collina=166089554482731363097584; guid=48fd9fd049c1b5aebb96ed0af24e7d0b; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; search=jobarea%7E%60000000%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2248fd9fd049c1b5aebb96ed0af24e7d0b%22%2C%22first_id%22%3A%22182b5154e0680-04ee3b22e7e8f6c-26021d51-1382400-182b5154e073a2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgyYjUxNTRlMDY4MC0wNGVlM2IyMmU3ZThmNmMtMjYwMjFkNTEtMTM4MjQwMC0xODJiNTE1NGUwNzNhMiIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjQ4ZmQ5ZmQwNDljMWI1YWViYjk2ZWQwYWYyNGU3ZDBiIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%2248fd9fd049c1b5aebb96ed0af24e7d0b%22%7D%2C%22%24device_id%22%3A%22182b5154e0680-04ee3b22e7e8f6c-26021d51-1382400-182b5154e073a2%22%7D; acw_tc=ac11000116608955433413865e00dfdcb4d22f2eb2396fd521d3b318e949ef; acw_sc__v2=62ff41374adc762c06e0a56278fb05de9b918d5a; ssxmod_itna=Yqfx0DyDgDuQqD5P0dD=G7IHG=kwmGA+OwGS8GrqGXd+oDZDiqAPGhDC8+U4R78Gh4sijSGfdaf77p4N6WRnv+aQVpx0aDbqGktIDO4GG0xBYDQxAYDGDDPDo2PD1D3qDkD7O1lS9kqi3DbO=Df4DmDGAc3qDgDYQDGTK6D7QDIk6=48=ec+rSAWtKil+dFqDMjeGXYiaqFqRakcDZiCnbqCpRDB61xBQMAkNUAeDHCwXM4eA3FOG3IBvYIGGF7B4oF+eA2GGxiBh3Y7qdB7qQ3ie=+z1qDDfdQYws7iD===; ssxmod_itna2=Yqfx0DyDgDuQqD5P0dD=G7IHG=kwmGA+OwGS8GxA=c3pxD/9ffDFhrgfKRA4KApxcQWwqi1eXGDFR8e70lF6OrPzhic8/Y8MR98FHbWBwASU7B4QKqxw05bv0Wn9dQYcH+KC2pe3FnK0Giz0evbIPYi7AuNHADhBGDWereFxauN9A0+O/vNV09NV1xWtIokI8uNkWWQ8IOLI/5LPE8jyDmAmzk6I9SA99O6GULLDrL=PwS27K8UNwOE5pEtI9BOX+6Fr133KF1rT55qKDtH1v=Q4OEQ81jRROqkHAKZT69MAxw=4haV+qC/MC5dt438S7DExYDwiH8NVGtcMY++tI8D7doHwFBxWzoT1g8eS5e4W3nTP2Ct4NeMYwmW8q73w+OR3HwYNMbL+zfWYvSb/n32DvvxdeZKsr8do8numQMG+fdfjr4OE/WfD2vjgb++=CSW7SGH=GG1GppjkuAhk+vZhcQpEwk5185=EnkAXpbGW7wc5/miAiPD7QuxGcDG7IuDQ0di0iHhx4D==',
            # 'Referer': 'https://jobs.51job.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                          '/104.0.0.0 Safari/537.36'
            }
        # 通过requests模块的里面get请求方法，对于url地址发送请求，并且携带上headers请求头 用变量接收数据
        time.sleep(4)
        response = requests.get(url=href, headers=headers,)
        response.encoding = 'gbk'
        # 2.获取数据

        print(response.text)

        # 3.解析数据
        selector = parsel.Selector(response.text)
        # css选择器 提取标签的属性内容
        content_1 = selector.css('.cn').get()
        content_2 = selector.css('.tCompany_main').get()
        content = content_1 + content_2
        html = html_str.format(article=content)

        html_path = 'html\\' + index['company_name'] + index['job_name'] +'.html'
        pdf_path = 'html\\' + index['company_name'] + index['job_name'] +'.pdf'
        with open(pdf_path, mode='w',encoding='utf-8' ) as f:
            f.write(html_path)
            config = pdfkit.configuration(wkhtmltopdf=r'E:\tools\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdfkit.from_file(html_path,pdf_path, configuration=config)
