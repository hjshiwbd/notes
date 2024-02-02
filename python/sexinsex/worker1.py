# handle special page
import logging
import re

import requests
import utils
from lxml import etree

# url = 'https://sexinsex.net/bbs/viewthread.php?tid=9585015&extra=&authorid=13965764&page=1'
# url = 'https://sexinsex.net/bbs/viewthread.php?tid=9585015&extra=&authorid=13965764&page=2'
# url = 'https://sexinsex.net/bbs/viewthread.php?tid=9585015&extra=&authorid=13965764&page=3'
url = 'https://sexinsex.net/bbs/viewthread.php?tid=9585015&extra=&authorid=13965764&page=4'

from_local = False


def get_html():
    if from_local:
        with open('page1.html', encoding="gbk") as io:
            return ''.join([x for x in io.readlines()])
    else:
        r = requests.get(url)
        r.encoding = 'gbk'
        return r.text


def run():
    s = get_html()
    html = etree.HTML(s, etree.HTMLParser(encoding='gbk'))
    # logging.info(s)
    root_list = html.xpath('//font[@face="宋体 "]/text()')
    str = ''
    for x in root_list:
        if x == '\n' or x == '\r\n':
            str = str + '\n\n'
        # 正则匹配: x的文字是第*章
        elif re.match(r'[\s|\S]*第.*?章.*', x):
            x = x.replace('\n', '').strip()
            x = x.replace('\r\n', '').strip()
            str += '\n\n' + x
        else:
            x = x.replace('\n', '').strip()
            x = x.replace('\r\n', '').strip()
            str += x
    logging.info(str)


def run2():
    s = '\r\n　　　　　　　　　　　　　　　　第一章'
    # 正则判断: s是否是第一章, 第二章, 第三章...etc, 考虑空格和换行符
    if re.match(r'[\s|\S]*第.*?章', s):
        print(123)
    else:
        print(456)


if __name__ == '__main__':
    utils.setup_logger('somename')
    run()
    # run2()
