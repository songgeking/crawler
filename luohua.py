import requests
import re
import pymysql
# 导入多线程池
from concurrent.futures import ThreadPoolExecutor


domain = "http://k.luohua197.com"
# 定义一个函数把photo,name,xfplay,full_url保存到mysql数据库中
def save_mysql(photo, name, xfplay, full_url, href):
    # 创建连接
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='luohua', charset='utf8')
    # 创建游标
    cursor = conn.cursor()
    # 执行sql语句
    sql = "insert into luohua(photo, name, xfplay, full_url, href) values('%s', '%s', '%s', '%s', '%s')" % (photo, name, xfplay, full_url, href)
    cursor.execute(sql)
    # 提交
    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()

# 定义read_mysql函数,读取eeuss表中的href数据
def read_mysql():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='luohua', charset='utf8')
    cursor = conn.cursor()
    sql = "select href from luohua"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# 设置一个变量接收read_mysql()
href_list = read_mysql()

def get_url(url):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }
    resp=requests.get(url, headers=headers)
    resp.encoding = "GBK"    
    
    obj1 = re.compile(r'<dl><dt><a href="(?P<href>.*?)" target="_blank" title="(?P<name>.*?)"', re.S)
    obj2 = re.compile(r"<a title='中文字幕' href='(?P<href2>.*?)'", re.S)
    obj3 = re.compile(r'<div class="tp"><img src="(?P<photo>.*?)"', re.S)
    obj4 = re.compile(r'document.write.*?"(?P<xfplay>.*?)"', re.S)
            
    result1 = obj1.finditer(resp.text)
    # print(get_url)
    for it in result1:
        href = it.group("href")
        full_url = domain + href
        list1 = []
        list1.append(href)
        tuple_href = tuple(list1)   # 把字符串转换为整个元组
        # 如果full_url在数据库中存在，则跳过
        if tuple_href in href_list:
            continue
        name = it.group("name")

        resp2 = requests.get(full_url, headers=headers)
        resp2.encoding = "GBK"
        result2 = obj2.search(resp2.text)
        href2 = result2.group("href2")
        full_child_url = domain + href2
            
        result3 = obj3.search(resp2.text)
        photo = result3.group("photo")

        resp3 = requests.get(full_child_url, headers=headers)
        resp3.encoding = "GBK"
        result4 = obj4.search(resp3.text)
        xfplay = result4.group("xfplay")
            
        print(photo, name, xfplay, full_url)
            # 把数据存到数据库中
        save_mysql(photo, name, xfplay, full_url, href)


if __name__ == '__main__':
       
    # 创建50个线程池
    with ThreadPoolExecutor(30) as t:        
        for i in range(1, 31):             
            if i == 1:                
                i = ""
            url = domain + f'/xxfj/ym/index{i}.html'         
            t.submit(get_url, url)
    print("全部下载完毕")
