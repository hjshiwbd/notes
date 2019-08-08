# coding:utf-8
import urllib2
import traceback
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

site = 'http://www.doushuge.com'

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


def get_homepage():
    s = curl_get(book_index_url).decode('gbk')
    return s


def resolve_html(page_obj):
    content_div = page_obj.find_all(id="content")[0]
    txt = content_div.get_text()

    title = page_obj.find_all(id="bgdiv")[0].h2.get_text()
    return title + '\n' * 2 + txt + '\n' * 2


def run():
    homepage = get_homepage()
    # homepage = html2
    index_page = BeautifulSoup(homepage, "html.parser")

    # title
    div1 = index_page.find_all('div', 'kfml')[0]
    bookname = div1.div.h1.get_text()
    print bookname
    book_txt = open(bookname + '.txt', 'a')

    # page links
    liebiao = index_page.find_all('div', 'liebiao')[0].find_all('a')
    n = 0
    for a in liebiao:
        # if n > 0:
        #     break
        n = n + 1
        href = a['href']
        url = book_index_url + href
        html = curl_get(url)
        # html = html1
        html = html.replace("&nbsp;", "").replace('&#16o;', '').replace('<br />','\n')
        page_obj = BeautifulSoup(html, "html.parser")
        content = resolve_html(page_obj)
        book_txt.write(content)
        print 'page done: %d/%d' % (n, len(liebiao))

    book_txt.close()


def run2():
    s = '   s   1'
    print s.replace(' ', '')


if __name__ == '__main__':
    run()
    # run2()
