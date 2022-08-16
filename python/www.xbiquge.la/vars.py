from siteinfo import SiteInfo

# 笔趣阁(1)
www_xbiquge_la = SiteInfo(site_domain='https://www.xbiquge.la',
                          xpath_book_name='//div[@id="info"]/h1/text()',
                          xpath_book_author='//div[@id="info"]/p/text()',
                          xpath_chapter_title='//div[@id="list"]//dd/a/text()',
                          xpath_chapter_url='//div[@id="list"]//dd/a/@href',
                          xpath_chapter_content='//div[@id="content"]/text()')

# 我要看书
www_51kanshu_cc = SiteInfo(site_domain='https://www.51kanshu.cc',
                           xpath_book_name='//div[@id="info"]/h1/text()',
                           xpath_book_author='//div[@id="info"]/p/text()',
                           xpath_chapter_title='//div[@class="listmain"]//dd/a/text()',
                           xpath_chapter_url='//div[@class="listmain"]//dd/a/@href',
                           xpath_chapter_content='//div[@id="content"]/p/text()')
