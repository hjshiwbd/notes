# coding:utf-8
# crawler for dd373, wow gold sale
# 
import re
import urllib
import urllib.request
import traceback
import sys
import zlib
import logging

# reload(sys)
# sys.setdefaultencoding('utf-8')
logging.basicConfig(level=logging.INFO,format='%(asctime)s|%(levelname)s|%(process)d|%(filename)s.%(lineno)d|%(message)s',datefmt='%y-%m-%d %H:%M:%S')

is_from_local = True
# is_from_local = False
# 
def curl_get(url, timeout=5, proxy=False, headers=None, gzip=False):
    if headers is None:
        headers = {}
    opener = urllib.request.build_opener()
    if proxy:
        proxy_info = {'host': '127.0.0.1',
                      'port': 7890}
        proxy_support = urllib.ProxyHandler({"http": "http://%(host)s:%(port)d" % proxy_info})
        opener = urllib.build_opener(proxy_support)

    request = urllib.request.Request(url, headers=headers)

    resp = opener.open(request, timeout=timeout)
    resp_html = resp.read()
    if gzip:
        resp_html = zlib.decompress(resp_html, 16 + zlib.MAX_WBITS)
    return resp_html


def from_remote(url):
    # s = curl_get(book_index_url).decode('gbk')
    # url = 'http://www.google.com'
    s = curl_get(url, proxy=False, gzip=True, timeout=60, headers={
        "authority": "t66y.com",
        "method": "GET",
        "path": "/thread0806.php?fid=25",
        "Proxy-Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.1 10/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }).decode('utf-8')
    return s


def from_local():
    # io = open('C:\\Users\\Administrator\\Desktop\\page1.html')
    io = open('C:\\Users\\Administrator\\Desktop\\dd373-1.html',encoding="utf-8")
    return ''.join([s for s in io.readlines()])


def get_page_html(url):
    if is_from_local:
        return from_local()
    else:
        return from_remote(url)


def handle_single_page(url):
    logging.info(url)
    html = get_page_html(url)
    # print(html)
    reg = r'(?<=<p class="font12 color666 m-t5">1金\=).*(?=元</p>)';
    rr = re.compile(reg, re.M|re.I)
    r = rr.findall(html)
    r.sort()
    print(r)


def run():
    url_base = 'https://www.dd373.com/s-eja7u2-0r2mut-cgkvu7-22bq81-0-0-jk5sj0-0-0-0-0-0-1-0-5-0.html'
    handle_single_page(url_base)
    logging.info("done")


def run2():
    print(range(1, 20))


if __name__ == '__main__':
    run()
    # run2()
