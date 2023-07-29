import utils
from lxml import etree
import requests.utils
import http.cookiejar
import chardet

site = 'https://www.rourouwu.com'
# 类目首页
cate_home = site + '/sort11/1/'


def get_url(url, data=None, with_cookie=False, cookie_file="", headers=None, **kwargs):
    """
    get请求,返回resp对象
    :return:
    """

    def get():
        if with_cookie:
            session.cookies = http.cookiejar.LWPCookieJar(cookie_file)
            session.cookies.load(ignore_expires=True, ignore_discard=True)
        return session.get(url, params=data, headers=headers)

    def post():
        if with_cookie:
            session.cookies = http.cookiejar.LWPCookieJar(cookie_file)
            session.cookies.load(ignore_expires=True, ignore_discard=True)
        return session.post(url, params=data, headers=headers)

    if url == "":
        raise Exception("no url")

    session = requests.session()
    r = post()
    coding2 = chardet.detect(r.content)['encoding']
    print(coding2)
    if "encoding" in kwargs:
        r.encoding = kwargs['encoding']

    if r.status_code == 403:
        raise Exception("login failed")
    elif r.status_code == 200:
        return r
    else:
        m = "post failed:{}".format(str(r))
        raise Exception(m)


def get_headers():
    return {
        "authority": "www.rourouwu.com",
        "method": "POST",
        "path": "/sort11/1/",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "_ym_d=1652782423; _ym_uid=1652782423915479393; __gads=ID=ee7d213862499663-224b8d9fd4d400e0:T=1659948691:RT=1659948691:S=ALNI_Mbz5Rk93LxFfBg17Qwz8QoFY-HT6Q; __gpi=UID=00000863e8f9b128:T=1659948691:RT=1659948691:S=ALNI_MbckmDef8h6G4qxhfUnESGNi1x-Lw; _ym_isad=2; cf_chl_2=6d24e821ba8a034; cf_chl_prog=x13; cf_clearance=cG6ZNJ5l1Fb7HOjkCkGkhK7YYZYKuofaRRchfoVShxE-1659950886-0-150",
        "origin": "https://www.rourouwu.com",
        "pragma": "no-cache",
        "referer": "https://www.rourouwu.com/sort11/1/?__cf_chl_tk=4ZgduLl7tGy4GqVKjzW4y6zbrqGOo22Chq2Z9pXvM90-1659950881-0-gaNycGzNCv0",
        "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    }


def run():
    resp = utils.get_url('https://m.rourouwu.com/wapsort/11_1.html', encoding='utf-8')
    print(resp.text)
    # resp = get_url(cate_home, headers=get_headers())
    #
    # html = resp.content
    # with open('test5.html', 'wb') as f:
    #     f.write(html)
    #
    # html = etree.HTML(resp.text)
    # book_hrefs = html.xpath('//div[@class="title"]/h2/a/@href')
    # print(book_hrefs)


if __name__ == '__main__':
    run()
