import re
import utils
from bs4 import BeautifulSoup
import time
import logging
from reportdetail import ReportDetail
from reportplayer import ReportPlayer
from reportaward import ReportAward

report_url = 'https://classic.warcraftlogs.com/guild/reports-list/491598?page='
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s|%(levelname)s|%(process)d|%(filename)s.%(lineno)d|%(message)s',
                    datefmt='%y-%m-%d %H:%M:%S')
# is_get_from_local = True
is_get_from_local = False


def get_from_local():
    with open('C:\\Users\\Administrator\\Desktop\\wcl\\python\\wcl1.html', encoding="utf-8") as io:
        return "\n".join([x.strip() for x in io.readlines()])


def get_from_remote(url):
    r = utils.get_url(url)
    return r.text


def get_html(url):
    if is_get_from_local:
        return get_from_local()
    else:
        return get_from_remote(url)


def save_report(report_list):
    count_sql = "select count(*) cc from test.wcl_report where report_id = %(report_id)s"
    sql = "insert into test.wcl_report (report_id,title,report_date,link) values (%(report_id)s,%(title)s,%(report_date)s,%(link)s)"
    with utils.connect_by_code('test001') as conn:
        for o in report_list:
            x = utils.query_one(conn, count_sql, o)
            if x.cc == 0:
                utils.update(conn, sql, o)


def get_report_date(td3):
    td3_text = "".join([str(x).strip() for x in td3.contents]).replace("\n", "")
    td3_text = re.findall(r"new.Date\(.*?\)", td3_text)
    n2 = re.findall(r"\d{10}", td3_text[0])
    d = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(n2[0])))
    return d


def get_report_list(soup):
    report_list = []
    table = soup.select('#reports-table')[0]
    trs = table.select('tr')
    for tr in trs:
        tds = tr.select('td')
        if len(tds) > 0:
            td1 = tds[0]
            title = td1.text.strip()
            link = td1.select('a')[0]['href']
            report_id = link[link.rindex("/") + 1:]

            td3 = tds[2]
            report_date = get_report_date(td3)

            report_list.append({
                "report_id": report_id,
                "link": link,
                "title": title,
                "report_date": report_date,
            })

    return report_list


def run_report_list():
    for i in range(1, 2):
        html = get_html(report_url + str(i))
        # soup = BeautifulSoup(html, "html.parser")
        # print(html)
        soup = BeautifulSoup(html, "html5lib")
        report_list = get_report_list(soup)
        save_report(report_list)


def run2():
    # s = """<script>var reportDate = new Date(1603296286 * 1000);var dateWrapper = moment(reportDate);document.write(dateWrapper.format("LLL"))</script>"""
    # n = re.findall(r"new.Date\(.*?\)", s)
    # n2 = re.findall(r"\d{10}", n[0])
    # print(n2[0])

    s = '/reports/7yGfn1hCgFZ3MPNp'
    print(s[s.rindex('/') + 1:])

    pass


def get_db_reportlist():
    # sql = "select * from test.wcl_report where title like '2团%' and id between 254 and 277"
    sql = "SELECT * FROM test.wcl_report WHERE title LIKE '2团%naxx%'and id not in " \
          "(select distinct  report_id from test.wcl_report_player) and report_date > '2020-10-01'ORDER BY id DESC"
    with utils.connect_by_code('test001') as conn:
        return utils.query_list(conn, sql)


def run_report_detail():
    # url = 'https://classic.warcraftlogs.com/reports/1wC7My3JdxTnkXhA'
    # report_id = '1wC7My3JdxTnkXhA'
    list = get_db_reportlist()
    for x in list:
        report_detail = ReportDetail(x)
        report_detail.run()
    pass


def run_export():
    """
    导出数据
    :return:
    """
    report_player = ReportPlayer()
    report_player.run()
    pass


def get_award_list():
    sql = "select * from test.wcl_report where id = 428"
    with utils.connect_by_code('test001') as conn:
        return utils.query_list(conn, sql)


def run_award():
    # award_list = get_award_list()
    # for report in award_list:
    report_award = ReportAward(428)
    report_award.run()


if __name__ == '__main__':
    # run_report_list()
    # run_report_detail()
    # run_export()
    run_award()
    # run2()
