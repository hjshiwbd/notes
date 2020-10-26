# coding:utf-8
# crawler for dd373, wow gold sale
#
import re
import traceback
import utils
import logging
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from bs4 import BeautifulSoup

# reload(sys)
# sys.setdefaultencoding('utf-8')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s|%(levelname)s|%(process)d|%(filename)s.%(lineno)d|%(message)s',
                    datefmt='%y-%m-%d %H:%M:%S')

# is_from_local = True
is_from_local = False


# toggle_price1 = 0.01


# def curl_get(url, timeout=5, proxy=False, headers=None, gzip=False):
#     if headers is None:
#         headers = {}
#     opener = urllib.request.build_opener()
#     if proxy:
#         proxy_info = {'host': '127.0.0.1',
#                       'port': 7890}
#         proxy_support = urllib.ProxyHandler(
#             {"http": "http://%(host)s:%(port)d" % proxy_info})
#         opener = urllib.build_opener(proxy_support)
#
#     request = urllib.request.Request(url, headers=headers)
#
#     resp = opener.open(request, timeout=timeout)
#     resp_html = resp.read()
#     if gzip:
#         resp_html = zlib.decompress(resp_html, 16 + zlib.MAX_WBITS)
#     return resp_html


def from_remote(url):
    # s = curl_get(book_index_url).decode('gbk')
    # url = 'http://www.google.com'
    s = utils.curl_get(url, proxy=False, gzip=True, timeout=60, headers={
        "authority": "t66y.com",
        "method": "GET",
        "path": "/thread0806.php?fid=25",
        "Proxy-Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.1 10/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }).decode('utf-8')
    return s


def from_local():
    # io = open('C:\\Users\\Administrator\\Desktop\\page1.html')
    io = open('C:\\Users\\Administrator\\Desktop\\dd373-1.html', encoding="utf-8")
    return ''.join([s for s in io.readlines()])


def get_page_html(url):
    if is_from_local:
        return from_local()
    else:
        return from_remote(url)


def get_toggle_price1():
    return utils.get_token_rate() * 0.85


def resolve_by_regex(html):
    reg = r'(?<=<p class="font12 color666 m-t5">1金\=).*(?=元</p>)'
    rr = re.compile(reg, re.M | re.I)
    r = rr.findall(html)
    r2 = []
    for x in r:
        r2.append(float(x))
    r2.sort()
    if r2[0] < get_toggle_price1():
        send_mail(str(r2[0]), str(r2[0]))
    logging.info(r2)


def resolve_by_bs4(html):
    soup = BeautifulSoup(html, "html.parser")
    # a = soup.find_all(name='div',attrs={'class':'goods-list-item'})
    l1 = soup.select('div.goods-list-item')
    l2 = []
    for x in l1:
        price = x.select('div.game-account-flag')[0].text.strip()
        id_ = x.select('a.font16')[0]['href'][1:-5]
        rate = x.select('p.m-t5')[0].text.split('=')[1][:-1]
        l2.append({
            "price": price,
            "id": id_,
            "rate": float(rate)
        })
    l2.sort(key=lambda x: x['rate'])
    logging.info(l2)
    rate = get_toggle_price1()
    logging.info(rate)
    if l2[0]['rate'] < rate:
        send_mail(str(l2[0]), str(l2[0]))


def handle_single_page(url):
    # logging.info(url)
    html = get_page_html(url)
    # print(html)
    # resolve_by_regex(html)
    resolve_by_bs4(html)


def run():
    url_base = 'https://www.dd373.com/s-eja7u2-0r2mut-cgkvu7-22bq81-0-0-jk5sj0-0-0-0-0-0-1-0-5-0.html'
    handle_single_page(url_base)
    logging.info("done")


def run2():
    print(range(1, 20))


def send_mail(title, content):
    my_sender = 'hjshiwbd@163.com'  # 发件人邮箱账号
    my_pass = 'EJZSGXNJGAVHMUAI'  # 发件人邮箱密码
    my_user = '34489659@qq.com'  # 收件人邮箱账号，我这边发送给自己
    smtp_server = 'smtp.163.com'

    def mail():
        ret = True
        try:
            msg = MIMEText('cheaper found:' + title, 'plain', 'utf-8')
            # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['From'] = formataddr(["gold spider", my_sender])
            # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['To'] = formataddr(["hjin", my_user])
            msg['Subject'] = "cheaper found:" + content  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL(smtp_server, 465)  # 发件人邮箱中的SMTP服务器，端口是25
            # server.set_debuglevel(1)
            server.helo(smtp_server)
            server.ehlo(smtp_server)
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.sendmail(my_sender, [my_user, ], msg.as_string())
            server.quit()  # 关闭连接
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            traceback.print_exc()
            ret = False
        return ret

    ret = mail()
    if ret:
        print("send mail success")
    else:
        print("send mail fail")


if __name__ == '__main__':
    run()
    # run2()
