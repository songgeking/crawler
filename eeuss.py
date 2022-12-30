import requests
import re
import pymysql
from concurrent.futures import ThreadPoolExecutor

def save_mysql(photo, name, xfplay, full_url, href):
    # 创建连接
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='luohua', charset='utf8')
    # 创建游标
    cursor = conn.cursor()
    # 执行sql语句
    sql = "insert into eeuss(photo, name, xfplay, full_url, href) values('%s', '%s', '%s', '%s', '%s')" % (photo, name, xfplay, full_url, href)
    cursor.execute(sql)
    # 提交
    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()

# 定义read_mysql函数,读取eeuss表中的full_url数据
def read_mysql():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='luohua', charset='utf8')
    cursor = conn.cursor()
    sql = "select href from eeuss"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# 设置一个变量接收read_mysql()
href_list = read_mysql()
domain = "https://vip.eeussma.com/"



def get_url(url):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }
    resp = requests.get(url, headers=headers)  # 获取目录页
    resp.encoding = "GBK"
    obj1 = re.compile(r'listCover.*?<a href="(?P<href>.*?)"><img src="(?P<photo>.*?)".*?alt="(?P<name>.*?)" />', re.S)

    result1 = obj1.finditer(resp.text)
    for i in result1:
        href = i.group('href')
        full_url = domain + href

        list1 = []
        list1.append(href)
        tuple_href = tuple(list1)   # 把字符串转换为整个元组
        # 如果full_url在数据库中存在，则跳过
        if tuple_href in href_list:
            continue

        photo = i.group('photo')
        name = i.group('name')
        
        resp2 = requests.get(full_url, headers=headers)  # 获取详情页
        resp2.encoding = "GBK"
        obj2 = re.compile(r"<a title=.*?href='(?P<href2>.*?)'", re.S)
        result2 = obj2.search(resp2.text)
        href2 = result2.group('href2')
        full_url2 = domain + href2
        
        resp3 = requests.get(full_url2, headers=headers)  # 获取播放页
        resp3.encoding = "GBK"
        obj3 = re.compile(r'<div class="player"><script type="text/javascript" src="(?P<href3>.*?)"', re.S)
        result3 = obj3.search(resp3.text)
        href3 = result3.group('href3')
        full_url3 = domain + href3
        
        resp4 = requests.get(full_url3, headers=headers)  # 获取xfplay页
        resp4.encoding = "GBK"
        obj4 = re.compile(r'xfplay://(?P<xfplay>.*?)xfplay', re.S)
        result4 = obj4.search(resp4.text)
        xfplay = result4.group('xfplay')
        full_xfplay = "xfplay://" + xfplay.replace('$', '')
        save_mysql(photo, name, full_xfplay, full_url, href)
        print(name, full_xfplay)
                


if __name__ == '__main__':
       
    # 创建50个线程池
    with ThreadPoolExecutor(30) as t:
        for i in range(1, 51):
            a = "_" 
            if i == 1:
                a = ""
                i = ""
            url = domain + f"/cn/index36{a}{i}.htm"            
            t.submit(get_url, url)
    print("全部下载完毕")
            
