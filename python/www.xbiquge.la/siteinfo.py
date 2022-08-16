class SiteInfo:
    # 域名
    site_domain = ''
    # 书籍主页
    book_home = ''
    # 书籍名称
    xpath_book_name = ''
    # 作者名字
    xpath_book_author = ''
    # 章节标题
    xpath_chapter_title = ''
    # 章节地址
    xpath_chapter_url = ''
    # 章节内容
    xpath_chapter_content = ''

    def __init__(self, site_domain, xpath_book_name, xpath_book_author, xpath_chapter_title,
                 xpath_chapter_url, xpath_chapter_content):
        self.site_domain = site_domain
        self.xpath_book_name = xpath_book_name
        self.xpath_book_author = xpath_book_author
        self.xpath_chapter_title = xpath_chapter_title
        self.xpath_chapter_url = xpath_chapter_url
        self.xpath_chapter_content = xpath_chapter_content

    def get_book_home(self, home):
        """
        返回书籍首页完整地址,eg: http://xxx.xxx.com/[x/y/z]
        :param home: 中括号部分
        :return:
        """
        return self.site_domain + home
