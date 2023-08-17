"""
通用小说爬取
1.网站域名
2.小说目录页地址
  - 获取小说名称的xpath
  - 获取小说作者的xpath
  - 获取每一章节地址的xpath
3.小说章节页
  - 获取章节内容的xpath
"""

# coding:utf8
import io
import logging
import time

import utils
from lxml import etree


# 生命一个对象 param 和init方法
class Param:
    def __init__(self, site_index, novel_list_url, novel_site_encoding, xpath_novel_name, xpath_novel_author,
                 xpath_chapter_url, xpath_chapter_title, xpath_chapter_content):
        self.site_index = site_index
        self.novel_list_url = novel_list_url
        self.novel_site_encoding = novel_site_encoding
        self.xpath_novel_name = xpath_novel_name
        self.xpath_novel_author = xpath_novel_author
        self.xpath_chapter_url = xpath_chapter_url
        self.xpath_chapter_title = xpath_chapter_title
        self.xpath_chapter_content = xpath_chapter_content


# 首页
site_index = 'https://www.rourouwu.net'
# 列表页
novel_list_url = site_index + '/read/117668//'
# 117668
# 字符集
# novel_site_encoding = 'utf-8'
novel_site_encoding = 'gbk'
# 列表页: 小说名称
xpath_novel_name = '//div[@id="srcbox"]/a[3]/@title'
# 列表页: 小说作者
xpath_novel_author = '//div[@class="infotitle"]/span/a/text()'
# 列表页: 小说章节地址
xpath_chapter_url = '//dd[@class="chapter_list"][position() >= 9]/a/@href'
# 内容页: 小说章节标题
xpath_chapter_title = '//a[@class="titlename"]/b/text()'
# 内容页: 小说章节内容
xpath_chapter_content = '//div[@id="main"]/div[2]/div/p/text()'

# 把上面属性放到一个对象里面
param = Param(site_index, novel_list_url, novel_site_encoding, xpath_novel_name, xpath_novel_author, xpath_chapter_url,
              xpath_chapter_title, xpath_chapter_content)

from_remote = True


# from_remote = False


def get_url(url):
    if 'javascript:Chapter' in url:
        # javascript:Chapter(32766046,111845); 获取2个数字
        arr = url.replace('javascript:Chapter(', '').replace(');', '').split(',')
        # /read/111845/32766045/
        return f'{site_index}/read/{arr[1]}/{arr[0]}/'
    else:
        return site_index + url


def xpath_one(html, xpath):
    """
    get tag content from xml using xpath
    :param txt:
    :param xpath:
    :return:
    """
    return html.xpath(xpath)[0]


def write_file(file_name, content):
    out = open(file_name, 'a', encoding='utf8')
    out.write(content)
    out.close()


def clear_file(file_name):
    out = open(file_name, 'w', encoding='utf8')
    out.write('')
    out.close()


def sort_url(list):
    step = 3
    newarr = []
    arr_len = len(list)
    for i in range(0, len(list), step):
        if i + 2 < arr_len:
            newarr.append(list[i + 2])
        if i + 1 < arr_len:
            newarr.append(list[i + 1])
        newarr.append(list[i])
    return newarr


def run():
    txt = ''
    if from_remote:
        r = utils.get_url(novel_list_url, encoding=novel_site_encoding)
        txt = r.text
    else:
        txt = utils.read_file('list.html', encoding=novel_site_encoding)

    html = etree.HTML(txt, etree.HTMLParser(encoding=novel_site_encoding))

    # use xpath to get novel name
    bookname = xpath_one(html, xpath_novel_name)
    logging.info(f'bookname: {bookname}')
    bookauthor = xpath_one(html, xpath_novel_author)
    logging.info(f'bookauthor: {bookauthor}')
    filename = f'{bookauthor} - {bookname}.txt'

    chapter_url_list = html.xpath(xpath_chapter_url)

    list2 = sort_url(chapter_url_list)

    output_str = ''
    clear_file(filename)
    count = 0

    output_str += f'{bookname}\n{bookauthor}\n\n'
    for chapter_url in list2:
        # if count > 0:
        #     break
        r2 = utils.get_url(get_url(chapter_url), encoding=novel_site_encoding)
        count = count + 1
        # logging.info(r2.text)
        html2 = etree.HTML(r2.text, etree.HTMLParser(encoding=novel_site_encoding))
        chapter_title = html2.xpath(xpath_chapter_title)[0]
        output_str += f'第{count}章 ' + chapter_title.strip() + '\n'
        chapter_content = html2.xpath(xpath_chapter_content)
        for line in chapter_content:
            line = line.strip()
            output_str += line.strip() + '\n'
        output_str += '\n\n'
        logging.info(f'processing: {count}/{len(chapter_url_list)}')
        write_file(filename, output_str)
        output_str = ''
        # time.sleep(3)


if __name__ == '__main__':
    utils.setup_logger('novel_crawler')
    run()
