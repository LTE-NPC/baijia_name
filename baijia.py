# 爬取百家姓姓名大全
# -----------------------------------
import requests
from lxml import etree

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

from models import BaijiaName

# 设置链接MySQL的配置
engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/baijia?charset=utf8", max_overflow=5,
                       encoding='utf-8')
session_maker = sessionmaker(bind=engine)
session = session_maker()


# 获取页面HTML
def get_one_page(url):
    # 客户端配置
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    # 使用get方式请求
    response = requests.get(url, headers=headers)
    # 判断返回状态码
    if response.status_code == 200:
        # 设置返回的字符编码
        text = response.content.decode('utf-8')
        # 返回
        return text
    # 没有内容就返回空
    return None


# 解析页面,取链接
def get_name_links(html):
    # 解析这个页面
    etree_html = etree.HTML(html)
    # 使用xpath匹配网址内容，取到的内容是列表
    result = etree_html.xpath('//a[contains(@class,"btn2")]/@href')
    # print(result)
    return result


# 得到name_list网址，然后使用字符串拼接
def get_one_name_all_page_links(name_link):
    # print(type(name_link))
    # 得到的是字符串有//需要用.split分割取下标为2的值就是网址
    domain_name = name_link.split('/')[2]
    # print(domain_name)

    # 建立2个空的列表存储
    all_boy_page_links = []
    all_girl_page_links = []


    # 循环10次，因为爬取的页面只有10页
    for i in range(10):
        # 用%s代替上面得到的字符串，%d代替数字，每循环一次加1
        page_link = 'http://%s/name/boys_%d.html' % (domain_name, i + 1)
        # print(page_link)
        # .append把值添加到列表里面
        all_boy_page_links.append(page_link)

        page_link = 'http://%s/name/girls_%d.html' % (domain_name, i + 1)
        # print(page_link)
        all_girl_page_links.append(page_link)

    return (all_boy_page_links, all_girl_page_links)


# 匹配网址里面的内容
def parse_name_page(page_html):
    etree_html = etree.HTML(page_html)
    result = etree_html.xpath('//div[@class="col-xs-12"]/a[contains(@class,"btn-link")]/text()')
    return result


# 保存到MySQL数据库names=boy_names/girl_names, gender=M/F
def save_db(names, gender):
    # engine = create_engine("mysql+pymysql://root:123456@127.0.0.1/taobao?charset=utf8", max_overflow=5)
    # session_maker = sessionmaker(bind=engine)
    # session = session_maker()

    # 遍历这个名字
    for name in names:
        # print(name)

        # 调用models表里面BaijiaName类
        baijia = BaijiaName()
        baijia.name = name
        baijia.gender = gender

        session.add(baijia)
        session.commit()

    # session.close()


#
def get_all_name_info(name_links):
    # all_boy_names = []
    # all_girl_names = []

    # 遍历这个列表
    for name_link in name_links:
        # 在遍历出来的值上面加http:
        real_name_link = 'http:%s' % name_link
        # print(real_name_link)

        # get_one_name_all_page_links：调用上面写的函数拼接出每条网址(传参数)在赋值
        # 得到得是['b','g']，所以赋值的时候可以用2个，将系列分解成单独的变量
        boy_links, girl_links = get_one_name_all_page_links(real_name_link)
        # print(boy_links, girl_links)
        # 拿到男孩名称遍历
        for boy_link in boy_links:
            # 调用get_one_page爬取boy_link的网址
            boy_html = get_one_page(boy_link)
            # 调用这个parse_name_page函数获取刚刚爬去到的页面里的内容
            boy_names = parse_name_page(boy_html)
            # print(boy_names)
            # all_boy_names.extend(boy_names)

            # 插入数据库(M表示男)(调用函数save_db)
            save_db(boy_names, 'M')

        # 女孩名称
        for girl_link in boy_links:
            girl_html = get_one_page(girl_link)
            girl_names = parse_name_page(girl_html)
            # print(girl_names)
            # all_girl_names.extend(girl_names)

            # 插入数据库
            save_db(girl_names, 'F')

    # return (all_boy_names, all_girl_names)


def main():
    # 1、网址
    url = 'http://www.resgain.net/xmdq.html'
    # 2、调用函数传参
    html = get_one_page(url)
    # 打印网址
    # print(html)
    # 3、调用函数解析页面赋值给name_links
    name_links = get_name_links(html)
    # print(name_links)
    # 4、把解析得到的内容(str)name_links作为参数传给get_all_name_info
    get_all_name_info(name_links)
    # 关闭数据库链接
    session.close()
    # boy_names, girl_names = get_all_name_info(name_links)
    # print(len(boy_names))
    # print(len(girl_names))


if __name__ == '__main__':
    main()
