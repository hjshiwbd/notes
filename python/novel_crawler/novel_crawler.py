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

import utils
from lxml import etree

novel_list_url = 'https://www.285b.com/index/49910'
novel_site_encoding = 'utf-8'
xpath_novel_name = '//div[@class="atitle"]/text()'
xpath_novel_author = '//div[@class="ainfo"]/a/text()'

xpath_chapter_url = '//dl[@class="index"]/dd/a/@href'

xpath_chapter_title = '//div[@class="atitle"]/text()'
xpath_chapter_content = '//div[@id="acontent"]/text()'

from_remote = True


def xpath_one(html, xpath):
    """
    get tag content from xml using xpath
    :param txt:
    :param xpath:
    :return:
    """
    return html.xpath(xpath)[0]


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
    bookauthor = xpath_one(html, xpath_novel_author)

    logging.info(f'bookname: {bookname}, bookauthor: {bookauthor}')

    chapter_url_list = html.xpath(xpath_chapter_url)

    output_str = ''
    count = 0

    output_str += f'{bookname}\n{bookauthor}\n\n'
    for chapter_url in chapter_url_list:
        # if count > 0:
        #     break
        r2 = utils.get_url(chapter_url, encoding=novel_site_encoding)
        count = count + 1
        html2 = etree.HTML(r2.text, etree.HTMLParser(encoding=novel_site_encoding))
        chapter_title = html2.xpath(xpath_chapter_title)[0]
        output_str += f'第{count}章 ' + chapter_title.strip() + '\n'
        chapter_content = html2.xpath(xpath_chapter_content)
        for line in chapter_content:
            line = line.strip()
            output_str += line.strip() + '\n'
        output_str += '\n\n'
        logging.info(f'processing: {count}/{len(chapter_url_list)}')

    out = io.open(f'{bookauthor} - {bookname}.txt', 'w', encoding='utf8')
    out.write(output_str)
    out.close()


if __name__ == '__main__':
    utils.setup_logger('novel_crawler')
    run()
