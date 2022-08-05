import time

import utils
from lxml import etree

# 域名
site_domain = 'https://www.xbiquge.la'
# 书籍主页
book_home = site_domain + '/19/19711/'
# 书籍名称
xpath_book_name = '//div[@id="info"]/h1/text()'
# 作者名字
xpath_book_author = '//div[@id="info"]/p/text()'
# 章节标题
xpath_chapter_title = '//div[@id="list"]//dd/a/text()'
# 章节地址
xpath_chapter_url = '//div[@id="list"]//dd/a/@href'
# 章节内容
xpath_chapter_content = '//div[@id="content"]/text()'
# 恢复下载
is_resume = False
# 恢复下载的章节数
resume_index = 0

is_local = False


def get_author(author):
    """
    作者名字dom的txt->解析作者名字
    :param author:
    :return:
    """
    return author.split('：')[1].strip()


def get_book_home():
    if is_local:
        f = open('1.html', encoding="utf-8")
        return ''.join([x.strip() for x in f.readlines()])
    else:
        s = utils.get_url(book_home, encoding='utf-8')
        return s.text


def run():
    book_home = get_book_home()
    book_home = etree.HTML(book_home)

    book_name = book_home.xpath('//div[@id="info"]/h1/text()')[0]
    author = book_home.xpath('//div[@id="info"]/p/text()')[0]
    author = get_author(author)
    chapter_title = book_home.xpath('//div[@id="list"]//dd/a/text()')
    chapter_url = book_home.xpath('//div[@id="list"]//dd/a/@href')
    list = []
    for i in range(len(chapter_title)):
        url = chapter_url[i]
        if not url.startswith('http'):
            url = site_domain + url
        list.append({'title': chapter_title[i], 'url': url})

    mode = 'a' if is_resume else 'w'
    fw = open(f'{author} - {book_name}.txt', mode, encoding='utf-8')
    ll = len(list)
    for i in range(ll):
        if is_resume and i < resume_index:
            continue
        c = list[i]
        url = c['url']
        title = c['title']
        s = utils.get_url(url, encoding='utf-8')
        html = etree.HTML(s.text)
        content = html.xpath('//div[@id="content"]/text()')

        title_txt = f'第{i + 1}章 {title}'
        content_txt = '\n'.join([x.strip() for x in content])
        fw.write(title_txt + '\n' * 2)
        fw.write(content_txt + '\n' * 2)
        print(f'{i}/{ll} done')
        time.sleep(1)

    fw.close()
    print('finish')


if __name__ == '__main__':
    run()
