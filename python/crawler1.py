# coding:utf-8
# crawler for t66y, get the basic info of the posts
"""
create database crawler;
CREATE TABLE `t66y_article` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `original_id` bigint(20) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `author_name` varchar(100) DEFAULT NULL,
  `post_date` datetime DEFAULT NULL,
  `link` varchar(255) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

import logging
import time
import traceback

import requests
from bs4 import BeautifulSoup
from jputils import dbutils

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s|%(levelname)s|%(process)d|%(filename)s.%(lineno)d|%(message)s',
                    datefmt='%y-%m-%d %H:%M:%S')

# 69c.org
domain = "t66y.com"
# domain = "cl.2790x.xyz"

# is_from_local = True
is_from_local = False

today = time.strftime('%Y-%m-%d', time.localtime())
yesterday = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60))
fid = 0
# 15亚有 25国 2亚无 中文26 欧美4 http21 动画5
fids = [26, 25, 15, 2, 21, 4, 5]
# 爬取起始页
crawler_page_start = 1
# 爬取终止页
crawler_page_length = 100
# 获取0则停止当前fid
break_on_count0 = True


def get_url(url, data=None, with_cookie=False, cookie_file="", headers=None, proxy=False):
    """
    get请求
    :return:
    """

    def get():
        if with_cookie:
            session.cookies = http.cookiejar.LWPCookieJar(cookie_file)
            session.cookies.load(ignore_expires=True, ignore_discard=True)

        proxies = None
        if proxy:
            proxies = {
                'http': 'http://127.0.0.1:7890'
            }
        return session.get(url, params=data, headers=headers, proxies=proxies, timeout=20)

    if url == "":
        raise Exception("no url")

    logging.info(f"{url},{data}")
    session = requests.session()
    r = get()

    if r.status_code == 403:
        raise Exception("login failed")
    elif r.status_code == 200:
        return r
    else:
        m = f"post failed:{str(r)}"
        raise Exception(m)


def from_remote(url):
    # s = curl_get(book_index_url).decode('gbk')
    # url = 'http://www.google.com'
    r = get_url(url, proxy=True, headers={
        "authority": domain,
        "method": "GET",
        "path": "/thread0806.php?fid=25",
        "Proxy-Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.1 10/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    })

    r.encoding = 'utf-8'
    return r.text
    # return s


def from_local():
    # io = open('C:\\Users\\Administrator\\Desktop\\page1.html')
    io = open('C:\\Users\\Administrator\\Desktop\\assdf.txt', encoding="utf-8")
    return ''.join([s for s in io.readlines()])


def get_page_html(url):
    if is_from_local:
        return from_local()
    else:
        return from_remote(url)


def resolve_html(page_obj):
    content_div = page_obj.find_all(id="content")[0]
    txt = content_div.get_text()

    title = page_obj.find_all(id="bgdiv")[0].h2.get_text()
    return title + '\n' * 2 + txt + '\n' * 2


def get_conn():
    return dbutils.get_conn('root', 'root', 'localhost', 3306, 'crawler');


def save_my_db(sqls):
    conn = get_conn()
    count = 0
    for sql in sqls:
        # print sql
        try:
            dbutils.update(conn, sql)
        except Exception as e:
            logging.info(sql)
            traceback.print_exc()
        count += 1
    logging.info("%d inserted" % count)
    conn.close()
    return count


def get_sql(exist_id_list, articles):
    result = []
    for o in articles:
        if int(o['id']) not in exist_id_list:
            sql = """
                INSERT INTO `crawler`.`t66y_article` (`fid`,`original_id`, `title`, `author_name`, `post_date`, `link` )
            VALUES	( '%s','%s','%s','%s','%s','%s');
                """.strip().replace("\n", "") % (
                str(fid), o['id'], o['title'], o['author'], o['create_date'], o['href'])
            result.append(sql)
    return result


def query_exist(articles):
    ids = ",".join([f"'{str(o['id'])}'" for o in articles])
    if ids == '':
        raise 'article ids is empty'

    sql = """
SELECT * FROM `t66y_article` where original_id in (%s)
    """ % ids

    conn = get_conn()
    exist_list = dbutils.query_list(conn, sql)
    conn.close()
    return [o.original_id for o in exist_list]


def get_id_from_href(href):
    # https://t66y.com/htm_data/1908/25/3618874.html
    # https://t66y.com/read.php?tid=3618875
    if href.startswith('htm_data'):
        # "/"到".html"之间的数字,即其原文id)
        return href.split("/")[3][0:-5]
    else:
        key = "tid="
        start = href.index(key) + len(key)
        end = start + 7
        return href[start:end]

    # id = get_id_from_href(href.split("/")[3][0:-5]  # "/"到".html"之间的数字,即其原文id)


def get_create_date(tds):
    dom_date = tds[2].div
    if not dom_date.span:
        return dom_date.get_text() + ' 00:00:00'
    if dom_date.get_text() == 'Top-marks':
        return dom_date.span['title'].replace('置顶主题：', '')
    dates = dom_date.get_text().split(' ')
    if len(dates) == 2:
        date1 = ''
        if dates[0] == '今天':
            date1 = today
        elif dates[0] == '昨天':
            date1 = yesterday
        create_date = date1 + ' ' + dates[1]
    else:
        create_date = dates[0] + ' 00:00:00'
    return create_date


def is_ignore(tr):
    ignores = ['來訪者必看的內容 - 使你更快速上手', '草榴官方客戶端', '注意事項', '关于用Bitcomet']
    txt = tr.get_text()
    flag = False
    for s in ignores:
        if s in txt:
            flag = True
    return flag


def handle_single_page(url):
    html = get_page_html(url)
    index_page = BeautifulSoup(html, "html.parser")
    trs = index_page.find_all('tr', class_='tr3 t_one tac')
    articles = []
    for tr in trs:
        flag = is_ignore(tr)
        if flag:
            continue
        # 2种情况
        # 0赞 1标题(id,链接) 2作者&创建时间 3回复数量 4下载 5最后回复
        # 0赞 1标题(id,链接) 2作者&创建时间 3回复数量 4最后回复
        tds = tr.find_all('td')
        dom_link = tds[1].h3.a
        href = dom_link['href']
        id = get_id_from_href(href)
        title = dom_link.get_text().replace("'", "''").replace("\\", "\\\\")
        # print(len(tds[1]))
        author = tds[2].a.get_text()
        create_date = get_create_date(tds)
        # print(create_date)
        o = {
            "id": id,
            "href": href,
            "title": title,
            "author": author,
            'create_date': create_date
        }
        articles.append(o)

    exist_id_list = query_exist(articles)
    sqls = get_sql(exist_id_list, articles)
    return save_my_db(sqls)


def get_queue():
    """
    当本日的队列
    不存在,生成带爬取数据,爬取.并写入mysql,类似于队列
    存在,取到队列,爬取
    """
    date = time.strftime("%y%m%d", time.localtime())
    # sql = "select * from crawler_queue where date = %(date)s"
    # cc = dbutils.query_list(conn, sql, params={"date": date})
    # if len(cc) == 0:
    arr = []
    for id in fids:
        for n in range(crawler_page_start, crawler_page_length + 1):
            arr.append({
                "fid": id,
                "page": n,
                "date": date,
            })  # 子栏目id, 爬前n页数

    sql_count = "select count(*) cc from crawler_queue where date = %(date)s and fid = %(fid)s and page =%(page)s"
    sql_insert = "INSERT INTO `crawler_queue`(`date`, `fid`, `page`) VALUES ( %(date)s, %(fid)s, %(page)s) "
    for one in arr:
        v = dbutils.query_one(conn, sql_count, one)
        if v.cc == 0:
            dbutils.update(conn, sql_insert, one)
    sql = "select * from crawler_queue where date = %(date)s and status='new'"
    cc = dbutils.query_list(conn, sql, {"date": date})
    return [k for k in cc if k.status == 'new']


def run():
    global fid, conn
    conn = get_conn()

    queue_list = get_queue()

    stopped = {}
    for id in fids:
        stopped[f'fid{id}'] = ''

    if len(queue_list) == 0:
        logging.info("queue_list is empty")

    for one in queue_list:
        fid = one.fid
        n = one.page
        key = 'fid' + str(fid)
        url = f'http://{domain}/thread0806.php?fid={str(fid)}&search=&page={str(n)}'
        count = -1
        if break_on_count0 and stopped[key] == '111':
            continue
        if stopped[key] != '111':
            count = handle_single_page(url)
            time.sleep(3)
        if count == 0:
            stopped[key] = stopped[key] + '1'
        else:
            stopped[key] = ''
        sql = f"update crawler_queue set status = 'done', get_count = {count} where id = {one.id}"
        dbutils.update(conn, sql)
    conn.close()
    logging.info("done")


def run2():
    s = 'read.php?tid=4250878&fpage=13'
    key = "tid="
    start = s.index(key) + len(key)
    end = start + 7


if __name__ == '__main__':
    run()
    # run2()
