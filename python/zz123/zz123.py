# help zmj to get https://zz123.com/duanju/eezc.htm content
import logging

import utils
from lxml import etree

from_local = True


def get_list_page():
    if from_local:
        with open('list.html', encoding="utf-8") as io:
            return ''.join([x for x in io.readlines()])
    else:
        list_url = 'https://zz123.com/duanju/eezc.htm'
        return utils.get_url(list_url, encoding='utf-8')


def run():
    s1 = get_list_page()
    # xpath
    html = etree.HTML(s1, etree.HTMLParser(encoding='utf-8'))
    a_list = html.xpath('//ul[@class="playYuan clearfix"]/li/a')
    pages = []
    for a in a_list:
        title = a.xpath('./text()')
        url = a.xpath('./@href')
        pages.append({'title': title[0], 'url': url[0]})

    for p in pages:
        title = p['title']
        url = p['url']
        logging.info(f'{title} {url}')
        # get content
        s2 = utils.get_url(url, encoding='utf-8')
        html2 = etree.HTML(s2, etree.HTMLParser(encoding='utf-8'))
        content = html2.xpath('//div[@class="article"]/text()')
        logging.info(content)
        # save to file


# xpath to get chapter url and title
if __name__ == '__main__':
    utils.setup_logger('zz123')
    run()
