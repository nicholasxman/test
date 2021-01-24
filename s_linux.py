#! /usr/bin/python3
# 这个网站的http://www.tzfdc.com.cn/hetong/index.php/index/xsxk.html 填词查询，注意次级链接xsxk 变成xsxkInfo
import requests
import pymysql
# import xml.etree.ElementTree as etree
from lxml import etree
import time
import random
import uuid
#第一处修改测试111111111111111111111111111

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!再加上定时
MY_USER_AGENT = [
	"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
	"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
	"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
	"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
	"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
	"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
	"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
	"Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
	"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
	"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
# 打开数据库连接
conn = pymysql.connect(host="192.168.164.130", database="yuanchao", user="root", password="123456", charset='utf8')
# 使用cursor()方法创建一个游标对象
cur = conn.cursor()
sql1 = '''  select  f1  FROM yuanchao.TaiZhou_Project   order by f1  desc limit 10  '''
cur.execute(sql1)
project_names = cur.fetchall()
for project_name in project_names:
    print(project_name[0])

    baseurl = 'http://www.tzfdc.com.cn/hetong/index.php/index/xsxkInfo.html?'
    params = {
        'XMMC' : project_name[0] ,
        # 'XMMC' : '世纪新城' ,
        'XSXZK':''   ,
        'QYMC': ''  ,
        'ctl00$ctl00$cc$ccModule$ep1$bq': '预售许可查询'
    }

    # 自动对params进行编码,然后自动和url进行拼接,去发请求
    time.sleep(2)
    head = random.choice(MY_USER_AGENT)
    res = requests.get(baseurl,params=params,headers={ 'User-Agent': head} ,      timeout=5)
    res.encoding = 'utf-8'
    print(res.text)
    print(res.encoding)


    response = etree.HTML(res.text)
    # for i in range(2,len(assessment_en)+1):
        # assessment_en = response.xpath("//table/tr["+ str(i)  +"]")
    assessment_en = response.xpath("//table/tr")
    for i in assessment_en[1:len(assessment_en)]   :

        print(i)
        ass = etree.tostring(i, encoding='utf-8', pretty_print=False, method='html')
        # # print("************", assessment_en)
        print(ass.decode('utf-8'))
        # F2=response.xpath("//table/tr[" + str(i) +"]"+ "/td[2]/text()")[0] #放弃这种写法
        F1=i.xpath("./td[1]/text()")[0]
        F2=i.xpath("./td[2]/text()")[0]
        F3=i.xpath("./td[3]/text()")[0]
        F4=i.xpath("./td[4]/text()")[0]
        F5=i.xpath("./td[5]/text()")[0]
        print(F2)

        fields=','.join(['%s']*7)
        sql = '''  insert into yuanchao.taizhou_test values(%s)   ''' % (fields)
        #使用execute()方法执行sql查询
        cur.execute(sql, ( uuid.uuid1(),  F1, F2,  F3, F4,F5,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        conn.commit()
        # conn.close()

