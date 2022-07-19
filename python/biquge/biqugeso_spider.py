"""
https://www.xbiquge.so/的爬虫
"""

# coding:utf-8
import utils
from bs4 import BeautifulSoup

use_local_file = False
book_index = 'https://www.xbiquge.so/book/1037'


def get_chatper_html(url):
    s = ''
    if use_local_file:
        io = open('content.html')
        arr = [x.strip() for x in io.readlines()]
        s = "".join(arr)
    else:
        r = utils.get_url(url, encoding="gbk")
        s = r.text
    return s


def get_chatpter_content(chapter_url, index):
    page_html = get_chatper_html(chapter_url)
    arr = []
    bs = BeautifulSoup(page_html, 'html.parser')
    d1 = bs.select('.bookname h1')
    d2 = bs.select('#content')
    chapter_name = d1[0].text
    arr.append(f'第{index + 1}章 ' + chapter_name)

    content = d2[0].decode_contents()
    content = content.replace('<br>', '<br/>').replace('</br>', '<br/>')
    arr = arr + [s1.strip() for s1 in content.split('<br/>')]
    return arr


def get_index_html():
    if use_local_file:
        io = open('index.html', encoding='utf-8')
        arr = [x.strip() for x in io.readlines()]
        return "".join(arr)
    else:
        r = utils.get_url(book_index)
        return r.text


def get_book_info():
    """
    书籍信息,书名,作者,每章节url
    :return:
    """
    html = get_index_html()
    bs = BeautifulSoup(html, 'html.parser')
    book_title = bs.select('div#info h1')[0].text
    book_author = bs.select('div#info p')[0].select('a')[0].text
    children = bs.select('div#list dl')[0].contents
    is_text_start = False
    book_pages = []
    for c in children:
        if is_text_start:
            # book_pages.append(c)
            a = c.select('a')
            if len(a) > 0:
                href = a[0]['href']
                book_pages.append(f'{book_index}/{href}')
        else:
            if c.name == 'center':
                is_text_start = True
    return book_title, book_author, book_pages


def run():
    (book_title, book_author, book_pages) = get_book_info()
    output = open(f"{book_author} - {book_title}.txt", "w+", encoding='utf-8')
    output.write("作者：%s\r\n" % book_author)

    ll = len(book_pages)
    for index, chapter_url in enumerate(book_pages):
        text_arr = get_chatpter_content(chapter_url, index)
        output.write("\n".join(text_arr))
        output.write("\n")
        output.write("\n")
        print(f'{index + 1}/{ll} done')

    output.close()
    print('all finish')


if __name__ == '__main__':
    run()
