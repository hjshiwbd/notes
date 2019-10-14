# coding:utf-8
"""
肉肉屋网站https://www.rourouwu.com/ 小说爬虫
"""

import urllib2
import traceback
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

site = 'https://www.rourouwu.com'

book_index_url = site + '/read/67484/'


def curl_get(url, timeout=5):
    try:
        resp = urllib2.urlopen(url, timeout=timeout)
        # return resp.read().decode('gbk')
        return resp.read()
    except urllib2.URLError, e:
        # raise Exception("curl_get error:%r"%e)
        traceback.print_exc()


def get_homepage():
    s = curl_get(book_index_url).decode('gbk')
    return s


def get_homepage_local():
    fileio = open("C:\\Users\\Administrator\\Desktop\\rourouwu1.html")
    return "\n".join([line.strip() for line in fileio.readlines()])


def parse_href(link):
    if link.lower().startswith("javascript:"):
        split1 = link.index("(")
        split2 = link.index(")")
        arr = link[split1 + 1: split2].split(",")
        return "/read/%s/%s/" % (arr[1], arr[0])
    else:
        return link
    pass


def get_chapter(chapter_url):
    chtml = curl_get(chapter_url).decode('gbk')
    c = BeautifulSoup(chtml, "html.parser")
    main = c.find("div", id="main")
    raw = main.find_all("div")[4].find_all("p")[2].text
    return "\n".join([x.strip() for x in raw.split("\n")])


def run():
    homepage = get_homepage()
    # homepage = get_homepage_local()
    # print homepage
    index_page = BeautifulSoup(homepage, "html.parser")
    title = index_page.find("div", class_="infotitle").h1.text  # 书名
    author = index_page.find("div", class_="infotitle").span.a.text  # 作者
    ddlist = index_page.find_all("dd", class_="chapter_list")  # 章节列表
    chapters = []
    for dd in ddlist:
        href = parse_href(dd.a.get("href"))
        name = dd.a.text
        chapters.append(
            {
                "name": name,
                "href": href
            }
        )

    output = open(title + ".txt", "w+")
    output.write("作者：%s\r\n" % author)
    ll = len(chapters)
    progress = 1
    for i in range(0, ll, 3):
        for j in range(2, -1, -1):
            if ll > (i + j):
                href = chapters[i + j]['href']  # 章节网址
                cname = chapters[i + j]['name']  # 章节名称
                chapter_url = site + href
                txt = get_chapter(chapter_url)  # 章节内容
                output.write(cname + "\r\n\r\n" + txt + "\r\n\r\n")
                print "%d/%d done" % (progress, ll)
                progress += 1
        # if i > 1:
        #     break
    output.close()
    print "all finish"


if __name__ == '__main__':
    run()
    # run2()

