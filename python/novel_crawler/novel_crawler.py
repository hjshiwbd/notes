"""
通用小说爬取
1.网站域名
2.小说目录页地址
  - 获取小说名称的xpath
  - 获取小说作者的xpath
  - 获取每一章节地址的xpath
3.小说章节页
  - 获取章节内容的xpath

爬取进度记录
drop table if exists novel_queue;
CREATE TABLE `novel_queue` (
  `id` bigint NOT NULL AUTO_INCREMENT,
    book_id varchar(500),
  `url` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `page` int DEFAULT NULL,
  `status` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ;

"""

# coding:utf8
import logging
import time

import requests
import utils
from lxml import etree
from param import Param, WwwRourouwuNet, Jingshuzhijia

# 把上面属性放到一个对象里面
param = WwwRourouwuNet()
# param = Jingshuzhijia()

# from_remote = False
from_remote = True

conn = None


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


def save_or_query_queue(list2, book_id):
    """
    书id查库,有就接着,没有就插入
    :param list2:
    :param book_id:
    :return:
    """
    arr = []
    sql = 'select url from crawler.novel_queue where book_id = %(bookId)s and status = \'new\''
    list = utils.query_list(conn, sql, {'bookId': book_id})
    if len(list) > 0:
        return [x.url for x in list]
    else:
        for i in range(0, len(list2)):
            # insert 爬取进度表
            o = list2[i]
            param = {
                'page': i + 1,
                'url': str(o),
                'status': 'new',
                'bookId': book_id
            }
            arr.append(param)

        sql = 'insert into crawler.novel_queue(url, page, status,book_id) values(%(url)s, %(page)s, %(status)s,%(bookId)s)'
        utils.update_many(conn, sql, arr)
        return list2


def update_page_ok(novel_list_url, chapter_url):
    sql = 'update crawler.novel_queue set status = \'success\' where url = %(url)s and book_id = %(bookId)s'
    utils.update(conn, sql, {'url': chapter_url, 'bookId': novel_list_url})


def http_get(url, **kwargs):
    proxies = None
    if 'use_proxy' in kwargs and kwargs['use_proxy']:
        proxy_server = 'http://127.0.0.1:7890'
        proxies = {
            'http': proxy_server,
            'https': proxy_server
        }
    logging.info(f"http_get:{param.novel_list_url}")
    r = requests.get(url=url, proxies=proxies, timeout=120)
    r.encoding = param.novel_site_encoding
    return r


def run():
    txt = ''
    if from_remote:
        # proxies = None
        # if param.use_proxy:
        #     proxy_server = 'http://127.0.0.1:7890'
        #     proxies = {
        #         'http': proxy_server,
        #         'https': proxy_server
        #     }
        # logging.info(f"book index:{param.novel_list_url}")
        # r = requests.get(url=param.novel_list_url, proxies=proxies, timeout=120)
        # r.encoding = param.novel_site_encoding
        r = http_get(url=param.novel_list_url, use_proxy=True, encoding=param.novel_site_encoding)
        txt = r.text
    else:
        txt = utils.read_file('list.html', encoding=param.novel_site_encoding)

    html = etree.HTML(txt, etree.HTMLParser(encoding=param.novel_site_encoding))

    # use xpath to get novel name
    bookname = xpath_one(html, param.xpath_novel_name)
    logging.info(f'bookname: {bookname}')
    bookauthor = xpath_one(html, param.xpath_novel_author)
    logging.info(f'bookauthor: {bookauthor}')
    filename = f'{bookauthor} - {bookname}.txt'

    chapter_url_list = html.xpath(param.format_xpath(html))

    list2 = param.sort_url(chapter_url_list)
    list3 = save_or_query_queue(list2, param.novel_list_url)

    output_str = ''
    # clear_file(filename)
    count = 0
    output_str += f'{bookname}\n{bookauthor}\n\n'
    for chapter_url in list3:
        # if count > 0:
        #     break
        # chapter_url = chapter_url if chapter_url.startswith('http') else param.site_index + chapter_url
        r2 = http_get(param.get_url(chapter_url), use_proxy=True, encoding=param.novel_site_encoding)
        count = count + 1
        # logging.info(r2.text)
        html2 = etree.HTML(r2.text, etree.HTMLParser(encoding=param.novel_site_encoding))
        chapter_title = html2.xpath(param.xpath_chapter_title)[0]
        output_str += f'第{count}章 ' + chapter_title.strip() + '\n'
        chapter_content = html2.xpath(param.xpath_chapter_content)
        for line in chapter_content:
            line = line.strip()
            output_str += line.strip() + '\n'
        output_str += '\n\n'
        logging.info(f'processing: {count}/{len(list3)}')
        write_file(filename, output_str)
        output_str = ''

        update_page_ok(param.novel_list_url, chapter_url)
        # time.sleep(3)


if __name__ == '__main__':
    utils.setup_logger('novel_crawler')
    with utils.connect('localhost', 3306, 'root', 'root') as conn:
        run()
