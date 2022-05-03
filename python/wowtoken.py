# coding:utf-8
# crawler for dd373, wow gold sale
#
import logging

from bs4 import BeautifulSoup

import utils1
from utils1 import redis_conn_master001

url_base = 'http://www.nfuwow.com/wowtoken/index.html'
# is_from_local = True
is_from_local = False


def from_local():
    io = open('C:\\Users\\Administrator\\Desktop\\dd373-1.html', encoding="utf-8")
    return ''.join([s for s in io.readlines()])


def from_remote(url):
    # s = curl_get(book_index_url).decode('gbk')
    # url = 'http://www.google.com'
    s = utils.curl_get(url, proxy=False, gzip=True, timeout=60, headers={
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


def get_page_html(url):
    if is_from_local:
        return from_local()
    else:
        return from_remote(url)


def resolve_by_bs4(html):
    soup = BeautifulSoup(html, "html.parser")
    # a = soup.find_all(name='div',attrs={'class':'goods-list-item'})
    l1 = soup.select('span.gold-money-scale')[0]
    t = l1['data-scale']
    return t


def save_redis(rate):
    with redis_conn_master001() as r:
        r.set(utils1.redis_w_key, rate)  # save


def handle_single_page(url):
    html = get_page_html(url)
    price = resolve_by_bs4(html)
    logging.info(str(price))
    save_redis(price)


def run():
    handle_single_page(url_base)
    logging.info("done")


if __name__ == '__main__':
    run()
