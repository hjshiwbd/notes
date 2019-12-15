# coding:utf-8
"""
中国证券投资基金业协会
http://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html
"""

import urllib
import urllib2
import traceback
from bs4 import BeautifulSoup
import requests
import sys
import time
import dbutils

reload(sys)
sys.setdefaultencoding('utf-8')
conn = None

cols = ["id", "managerName", "artificialPersonName", "registerNo", "establishDate", "managerHasProduct", "url",
        "registerDate", "registerAddress", "registerProvince", "registerCity", "regAdrAgg", "fundCount", "fundScale",
        "paidInCapital", "subscribedCapital", "hasSpecialTips", "inBlacklist", "hasCreditTips", "regCoordinate",
        "officeCoordinate", "officeAddress", "officeProvince", "officeCity", "primaryInvestType"]

sql = """INSERT INTO `test`.`amac1`(`id`, `managerName`, `artificialPersonName`, `registerNo`, `establishDate`, `managerHasProduct`, `url`, `registerDate`, `registerAddress`, `registerProvince`, `registerCity`, `regAdrAgg`, `fundCount`, `fundScale`, `paidInCapital`, `subscribedCapital`, `hasSpecialTips`, `inBlacklist`, `hasCreditTips`, `regCoordinate`, `officeCoordinate`, `officeAddress`, `officeProvince`, `officeCity`, `primaryInvestType`) VALUES (%s);
"""

file = open("d:\\amac.sql", "w+")


def curl_get(url, timeout=5):
    try:
        resp = urllib2.urlopen(url, timeout=timeout)
        # return resp.read().decode('gbk')
        return resp.read()
    except urllib2.URLError, e:
        # raise Exception("curl_get error:%r"%e)
        traceback.print_exc()


def curl_post(url):
    try:
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Host": "gs.amac.org.cn",
            "Referer": "http://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }

        resp = requests.post(url, "{}", headers=headers)

        return resp.text
    except urllib2.URLError, e:
        print e.code, e.reason
        traceback.print_exc()


def savedb(o):
    values = ''
    for col in cols:
        values += ",'%s'" % o[col]
    execsql = sql % values[1:]
    print execsql

    file.write(execsql)
    # dbutils.update(conn, execsql)
    pass


def get_homepage():
    conn = dbutils.get_conn_ocmp()
    for a in range(0, 245):
        url = 'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.039604630225410054&page=%s&size=100' % str(a)
        s = curl_post(url)  # .decode('gbk')
        s = s.replace("null", "None").replace("true", "True").replace("false", "False")
        all = eval(s)

        for o in all['content']:
            savedb(o)


def run():
    print "start"
    homepage = get_homepage()
    print "all finish"


if __name__ == '__main__':
    run()
    # run2()
