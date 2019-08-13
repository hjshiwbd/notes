# coding:utf-8
# crawler for t66y, get the basic info of the posts

import urllib2
import traceback
from bs4 import BeautifulSoup
import sys
import zlib
import time

reload(sys)
sys.setdefaultencoding('utf-8')

site = 'http://www.doushuge.com'

# book_index_url = site + '/145/145496/index.html'
# book_index_url = site + '/108/108747/index.html'
# book_index_url = site + '/148/148560/index.html'
book_index_url = site + '/8/8216/'


def curl_get(url, timeout=5, proxy=False, headers=None, gzip=False):
    if headers is None:
        headers = {}
    try:
        opener = urllib2.build_opener()
        if proxy:
            proxy_info = {'host': '127.0.0.1',
                          'port': 10801}
            proxy_support = urllib2.ProxyHandler({"http": "http://%(host)s:%(port)d" % proxy_info})
            opener = urllib2.build_opener(proxy_support)

        request = urllib2.Request(url, headers=headers)

        resp = opener.open(request, timeout=timeout)
        resp_html = resp.read()
        if gzip:
            resp_html = zlib.decompress(resp_html, 16 + zlib.MAX_WBITS)
        return resp_html
    except urllib2.URLError, e:
        traceback.print_exc()


def from_remote(url):
    # s = curl_get(book_index_url).decode('gbk')
    # url = 'http://www.google.com'
    s = curl_get(url, proxy=True, gzip=True, headers={
        "Host": "t66y.com",
        "Proxy-Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }).decode('gbk')
    return s


def from_local():
    # io = open('C:\\Users\\Administrator\\Desktop\\page1.html')
    io = open('C:\\Users\\Administrator\\Desktop\\page5.html')
    return ''.join([s.decode('utf-8') for s in io.readlines()])


def get_page_html(url):
    # return from_remote(url)
    return from_local()


def resolve_html(page_obj):
    content_div = page_obj.find_all(id="content")[0]
    txt = content_div.get_text()

    title = page_obj.find_all(id="bgdiv")[0].h2.get_text()
    return title + '\n' * 2 + txt + '\n' * 2


def run():
    url = 'http://t66y.com/thread0806.php?fid=25&search=&page=1'
    html = get_page_html(url)
    index_page = BeautifulSoup(html, "html.parser")
    trs = index_page.find_all('tr', class_='tr3 t_one tac')
    for tr in trs:
        ignores = ['來訪者必看的內容 - 使你更快速上手', '草榴官方客戶端 & 大陸入口', 'BT區注意事項，版規']
        txt = tr.get_text()
        flag = False
        for s in ignores:
            if s in txt:
                flag = True
        if flag:
            continue

        tds = tr.find_all('td')
        dom_link = tds[1].h3.a
        dom_date = tds[2].div
        dates = dom_date.get_text().split(' ')
        # print dates
        if len(dates) == 2:
            date1 = ''
            if dates[0] == '今天':
                date1 = time.strftime('%Y-%m-%d', time.localtime())
            elif dates[0] == '昨天':
                date1 = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60))
            create_date = date1 + ' ' + dates[1]
        else:
            create_date = dates[0] + ' 00:00:00'

        href = dom_link['href']
        id = href.split("/")[3][0:-5]
        o = {
            "id": id,
            "href": dom_link['href'],
            "title": dom_link.get_text(),
            'create_date': create_date
        }
        print o

    return 0


def run2():
    s = '   s   1'
    print s.replace(' ', '')


if __name__ == '__main__':
    run()
    # run2()
