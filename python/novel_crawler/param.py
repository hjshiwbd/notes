# 声明一个对象 param 和init方法
class Param:
    use_proxy = False
    xpath_chapter_url = ''

    def __init__(self):
        pass

    def sort_url(self, list):
        """
        显示顺序和实际顺序不一样,调整
        :param list:
        :return:
        """
        return list

    def format_xpath(self, html):
        """
        获取所有章节目录. 在所有章节目录里, 有一部分是不需要的(比如某些站的排序规则是最新的10章+从1开始的章节), 在此处处理
        :param html:
        :return:
        """
        return self.xpath_chapter_url

    def get_url(self, url):
        """
        每一章节的url的处理. 有的没有http开头, 有的不是url是js方法
        :param url:
        :return:
        """
        return url

    def get_chapter_title(self, str):
        """
        通过xpath获取到内容后,二次处理
        :param str:
        :return:
        """
        return str


class WwwRourouwuNet(Param):
    """
    https://www.rourouwu.net
    """
    use_proxy = True
    # 首页
    site_index = 'https://www.rourouwu.net'
    # 列表页
    novel_list_url = site_index + '/read/111845/'
    # 117668
    # 字符集
    # novel_site_encoding = 'utf-8'
    novel_site_encoding = 'gbk'
    # 列表页: 小说名称
    xpath_novel_name = '//div[@id="srcbox"]/a[3]/@title'
    # 列表页: 小说作者
    xpath_novel_author = '//div[@class="infotitle"]/span/a/text()'
    # 列表页: 小说章节地址
    xpath_chapter_url = '//dd[@class="chapter_list"][position() > {count}]/a/@href'
    # 内容页: 小说章节标题
    xpath_chapter_title = '//div[@id="main"]/h1/text()'
    # 内容页: 小说章节内容
    xpath_chapter_content = '//div[@id="main"]/div[2]/div/p/text()'

    def sort_url(self, list):
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

    def format_xpath(self, html):
        a = html.xpath('//div[@class="zjbox"]/dl/*')
        can_increase = False
        count = -1
        start_tag = 'dt'
        end_tag = 'dt'
        for x in a:
            if x.tag == end_tag and can_increase:
                break
            if x.tag == start_tag and not can_increase:
                can_increase = True
            if can_increase:
                count = count + 1
        self.xpath_chapter_url = self.xpath_chapter_url.replace("{count}", str(count))

        return self.xpath_chapter_url

    def get_url(self, url):
        if 'javascript:Chapter' in url:
            # javascript:Chapter(32766046,111845); 获取2个数字
            arr = url.replace('javascript:Chapter(', '').replace(');', '').split(',')
            # /read/111845/32766045/
            return f'{self.site_index}/read/{arr[1]}/{arr[0]}/'
        else:
            return self.site_index + url


class BeqegeCc(Param):
    """
    https://www.beqege.cc/75040/
    """
    # 代理
    use_proxy = False
    # 首页
    site_index = 'https://www.beqege.cc'
    # 列表页
    novel_list_url = site_index + '/16279/'
    # 117668
    # 字符集
    novel_site_encoding = 'utf-8'
    # novel_site_encoding = 'gbk'
    # 列表页: 小说名称
    xpath_novel_name = '//div[@id="srcbox"]/a[3]/@title'
    # 列表页: 小说作者
    xpath_novel_author = '//div[@class="infotitle"]/span/a/text()'
    # 列表页: 小说章节地址
    xpath_chapter_url = '//dd[@class="chapter_list"][position() > {count}]/a/@href'
    # 内容页: 小说章节标题
    xpath_chapter_title = '//div[@id="main"]/h1/text()'
    # 内容页: 小说章节内容
    xpath_chapter_content = '//div[@id="main"]/div[2]/div/p/text()'
    # headers
    headers = {
        # "cookie": "SL_G_WPT_TO=eo; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; __gads=ID=bfcb8ff05366b808-22848cb49ae4006a:T=1697520476:RT=1709004343:S=ALNI_MZUhxtcq3PQcXjyJc09sQW_VycXmw; __gpi=UID=00000c64f8a5c905:T=1697520476:RT=1709004343:S=ALNI_MZupImck36lbeC1f5aGnndfECvGSg; __eoi=ID=8a4dfb112901d52a:T=1709004036:RT=1709004343:S=AA-AfjYl2Km7_KTEQhsj71oLHorQ; cf_clearance=qp7DthumHoD9I0_UNCZe1z0L2RlGqQvKQR17wiLvAQM-1709004434-1.0-AYtFwayrEpAfLrwjhLpXZd5QcWgAFk2hFZrBPhJwPoHEKxROrzdbFRWvfBYlBByvLtmfp2rNLebNCaVxcZgmi+Q=",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    cookie = {
        "SL_G_WPT_TO": "eo",
        "SL_GWPT_Show_Hide_tmp": "1",
        "SL_wptGlobTipTmp": "1",
        "__gads": "ID=bfcb8ff05366b808-22848cb49ae4006a:T=1697520476:RT=1709004343:S=ALNI_MZUhxtcq3PQcXjyJc09sQW_VycXmw",
        "__gpi": "UID=00000c64f8a5c905:T=1697520476:RT=1709004343:S=ALNI_MZupImck36lbeC1f5aGnndfECvGSg",
        "__eoi": "ID=8a4dfb112901d52a:T=1709004036:RT=1709004343:S=AA-AfjYl2Km7_KTEQhsj71oLHorQ",
        "cf_clearance": "qp7DthumHoD9I0_UNCZe1z0L2RlGqQvKQR17wiLvAQM-1709004434-1.0-AYtFwayrEpAfLrwjhLpXZd5QcWgAFk2hFZrBPhJwPoHEKxROrzdbFRWvfBYlBByvLtmfp2rNLebNCaVxcZgmi+Q=",
    }


class Jingshuzhijia(Param):
    """
https://jinshuzhijia.com/index.php/book/info/lutoujin
    """
    # 代理访问
    use_proxy = True
    # 首页
    site_index = 'https://jinshuzhijia.com'
    # 列表页
    # https://jinshuzhijia.com/index.php/book/info/chenlunyinyudejiaoqu
    novel_list_url = site_index + '/index.php/book/info/chenlunyinyudejiaoqu'
    # 117668
    # 字符集
    novel_site_encoding = 'utf-8'
    # novel_site_encoding = 'gbk'
    # 列表页: 小说名称
    xpath_novel_name = '//meta[@name="DC.title"]/@content'
    # 列表页: 小说作者
    xpath_novel_author = '//meta[@name="DC.creator"]/@content'
    # 列表页: 小说章节地址
    xpath_chapter_url = '//ul[@class="tjzl"]/li/a/@href'
    # 内容页: 小说章节标题
    xpath_chapter_title = '//div[@class="rtj-title"]/h1/text()'
    # 内容页: 小说章节内容
    xpath_chapter_content = '//div[@class="tjc-cot"]/p/text()'

    def get_url(self, url):
        url = url if url.startswith('http') else self.site_index + url
        return url


class BiquxsCom(Param):
    """
    http://www.biquxs.com/book/1040/
    """
    use_proxy = False
    site_index = "http://www.biquxs.com"
    # 列表页
    # https://jinshuzhijia.com/index.php/book/info/chenlunyinyudejiaoqu
    novel_list_url = site_index + '/book/13993/'
    # 117668
    # 字符集
    novel_site_encoding = 'utf-8'
    # novel_site_encoding = 'gbk'
    # 列表页: 小说名称
    xpath_novel_name = '//meta[@property="og:title"]/@content'
    # 列表页: 小说作者
    xpath_novel_author = '//meta[@property="og:book:author"]/@content'
    # 列表页: 小说章节地址
    xpath_chapter_url = '//div[@class="listmain"]/dl/dd[position() > 5]/a//@href'
    # 内容页: 小说章节标题
    xpath_chapter_title = '//title/text()'
    # 内容页: 小说章节内容
    xpath_chapter_content = '//div[@id="content"]/p/text()'

    def get_url(self, url):
        return self.site_index + url

    def get_chapter_title(self, str):
        arr = str.split('_')
        return arr[0]
