# coding:utf-8
"""
肉肉屋网站https://www.rourouwu.com/ 小说爬虫
"""
import sys
import traceback

import utils
from bs4 import BeautifulSoup

site = 'https://www.rourouwu.com'

book_index_url = site + '/read/51295/'


def get_homepage():
    s = utils.get_url(book_index_url)
    s.encoding = 'gbk'
    return s.text


def get_homepage_local():
    fileio = open("C:\\Users\\Administrator\\Desktop\\rourouwu1.html")
    return "\n".join([line.strip() for line in fileio.readlines()])


def parse_href(link):
    if link.lower().startswith("javascript:"):
        split1 = link.index("(")
        split2 = link.index(")")
        arr = link[split1 + 1: split2].split(",")
        return site + "/read/%s/%s/" % (arr[1], arr[0])
    elif link.startswith("http"):
        return link
    else:
        return site + link


def get_chapter(chapter_url):
    chtml = ""
    try:
        r = utils.get_url(chapter_url)
        r.encoding = 'gbk'
        chtml = r.text
    except Exception:
        print(chapter_url)
        traceback.print_exc()
        sys.exit(1)
    c = BeautifulSoup(chtml, "html.parser")
    main = c.find("div", id="main")
    raw = main.find_all("div")[4].find_all("p")[2].text
    return "\n".join([x.strip() for x in raw.split("\n")])


def fix_win_filename(title):
    arr = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for w in arr:
        title = title.replace(w, '_')
    return title


def run():
    print("start")
    homepage = get_homepage()
    print("get index done")
    # homepage = get_homepage_local()
    # print homepage
    index_page = BeautifulSoup(homepage, "html.parser")
    title = index_page.find("div", class_="infotitle").h1.text  # 书名
    title = fix_win_filename(title)
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

    output = open(title + ".txt", "w+", encoding="utf-8")
    output.write("作者：%s\r\n" % author)
    ll = len(chapters)
    progress = 1
    for i in range(0, ll, 3):
        for j in range(2, -1, -1):
            if ll > (i + j):
                href = chapters[i + j]['href']  # 章节网址
                cname = chapters[i + j]['name']  # 章节名称
                txt = get_chapter(href)  # 章节内容
                output.write(cname + "\r\n\r\n" + txt + "\r\n\r\n")
                print("%d/%d done" % (progress, ll))
                progress += 1
                # time.sleep(10)
        # if i > 1:
        #     break
    output.close()
    print("all finish")


if __name__ == '__main__':
    run()
    # run2()
