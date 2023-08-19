# 声明一个对象 param 和init方法
class Param:
    xpath_chapter_url = ''

    def __init__(self):
        pass

    def sort_url(self, list):
        return list

    def format_xpath(self, html):
        return self.xpath_chapter_url

    def get_url(self, url):
        return url


class WwwRourouwuNet(Param):
    """
    https://www.rourouwu.net
    """
    # 首页
    site_index = 'https://www.rourouwu.net'
    # 列表页
    novel_list_url = site_index + '/read/92607//'
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
