# coding:utf-8
import urllib2
import traceback
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

site = 'http://www.515fa.com'

# book_index_url = site + '/145/145496/index.html'
# book_index_url = site + '/108/108747/index.html'
# book_index_url = site + '/148/148560/index.html'
book_index_url = site + '/8/8216/'


def curl_get(url, timeout=5):
    try:
        resp = urllib2.urlopen(url, timeout=timeout)
        # return resp.read().decode('gbk')
        return resp.read()
    except urllib2.URLError, e:
        # raise Exception("curl_get error:%r"%e)
        traceback.print_exc()


def get_page():
    # html = curl_get(url).decode('utf-8')
    html = """

    """
    return html


def resolve_html(page_obj):
    content_div = page_obj.find_all(id="content")[0]
    txt = content_div.get_text()

    title = page_obj.find_all(id="bgdiv")[0].h2.get_text()
    return title + '\n' * 2 + txt + '\n' * 2


def run():
    url = site + '/che_21256.html';

    html = curl_get(url).decode('utf-8')
    print html
    # page = BeautifulSoup(url, "html.parser")

def run2():
    s = '   s   1'
    print s.replace(' ', '')


if __name__ == '__main__':
    run()
    # run2()
