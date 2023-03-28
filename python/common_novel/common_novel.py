import logging

import utils
from lxml import etree

conf = {
    'site_domain': 'https://www.ibiquge.la',
    'bookname': '星河长明',
    'author': '金陵城中鱼',
    'list_page': 'https://www.ibiquge.la/106/106650/',
    'pages_url_xpath': '/html/body//div[@id="list"]//dd/a/@href',
    'content_page': 'https://www.jkdyf01.com/book/5155/2039611.html',
    'content_start_index': 0
}


def run():
    a = utils.get_url(conf['list_page'])
    a.encoding = 'utf-8'

    list_html = a.text
    # logging.info('\n'+list_html)

    html = etree.HTML(list_html)
    chapter_urls = html.xpath(conf['pages_url_xpath'])
    # logging.info(chapter_urls)
    for i, url in enumerate(chapter_urls):
        url = str(url)
        logging.info(url)

        if not url.startswith('http'):
            url = conf['site_domain'] + url
        if i > 0:
            break
        c = utils.get_url(url)
        c.encoding = 'utf-8'
        content = c.text
        logging.info('\n' + content)


if __name__ == '__main__':
    utils.setup_logger('cnovel')
    run()
