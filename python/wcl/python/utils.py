#  -*- coding:utf-8 -*-  

import shlex
import subprocess
import logging
import requests
import http.cookiejar
import mysql.connector
import time

conns = {
    "115": {
        "host": "192.168.0.115",
        "port": 3306,
        "user": "huangj",
        "password": "hUaNgj_2020",
    },
    "test001": {
        "host": "test001.yz",
        "port": 11017,
        "user": "huangj",
        "password": "hUaNgj_2020",
    }
}


def post_url(url, data=None, with_cookie=False, cookie_file="", headers=None):
    """
    post请求
    :return:
    """

    def post():
        if with_cookie:
            session.cookies = http.cookiejar.LWPCookieJar(cookie_file)
            session.cookies.load(ignore_expires=True, ignore_discard=True)
        return session.post(url, data, headers=headers)

    if url == "":
        raise Exception("no url")

    logging.info("{},{}".format(url, data))
    session = requests.session()
    # data = urllib.parse.urlencode(data).encode('utf-8')
    r = post()

    if r.status_code == 403:
        raise Exception("login failed")
    elif r.status_code == 200:
        return r
    else:
        raise Exception("post failed:{}".format(r.status_code))


def get_url(url, data=None, with_cookie=False, cookie_file="", headers=None):
    """
    get请求
    :return:
    """

    def get():
        if with_cookie:
            session.cookies = http.cookiejar.LWPCookieJar(cookie_file)
            session.cookies.load(ignore_expires=True, ignore_discard=True)
        return session.get(url, params=data, headers=headers)

    if url == "":
        raise Exception("no url")

    logging.info("{},{}".format(url, data))
    session = requests.session()
    r = get()

    if r.status_code == 403:
        raise Exception("login failed")
    elif r.status_code == 200:
        return r
    else:
        m = "post failed:{}".format(str(r))
        raise Exception(m)


def connect(host, port, user, password):
    cnx = mysql.connector.connect(user=user, password=password,
                                  host=host, port=port)
    return cnx


def connect_by_code(code):
    conn = conns[code]
    return connect(conn['host'], conn['port'], conn['user'], conn['password'])


def query_list(conn, sql, param=None):
    """
    eg1:
        sql = "select * from tbl where userid = %(userid)s and username = %(user_name)s"
        param={"userid": "xxx", "user_name": "yyy"}
    eg2:
        sql = "select * from tbl where userid = %s and user_name = %s"
        param=("xxx", "yyy")
    :param conn:
    :param sql:
    :param param:
    :return:
    """
    cursor = conn.cursor(named_tuple=True)
    logging.info(sql + ", param=" + str(param))
    cursor.execute(sql, param)
    result = []
    for o in cursor:
        result.append(o)
    cursor.close()
    return result


def query_one(conn, sql, param=None):
    """
    eg1:
        sql = "select * from tbl where userid = %(userid)s and username = %(user_name)s"
        param={"userid": "xxx", "user_name": "yyy"}
    eg2:
        sql = "select * from tbl where userid = %s and user_name = %s"
        param=("xxx", "yyy")
    :param conn:
    :param sql:
    :param param:
    :return:
    """
    list = query_list(conn, sql, param)
    if len(list) == 1:
        return list[0]
    elif len(list) == 0:
        return None
    else:
        raise Exception("more than 2 rows found, but except 1")


def update(conn, sql, param=None):
    """
    eg1:
        sql = "select * from tbl where userid = %(userid)s and username = %(user_name)s"
        param={"userid": "xxx", "user_name": "yyy"}
    eg2:
        sql = "select * from tbl where userid = %s and user_name = %s"
        param=("xxx", "yyy")
    :param conn:
    :param sql:
    :param param:
    :return:
    """
    cursor = conn.cursor()
    logging.info(sql + ", param=" + str(param))
    cursor.execute(sql, param)
    conn.commit()


def run_cmd(cmd, err_stop=True, encoding="gbk", print_log=True, **kwargs):
    list = cmd.split("\n")
    result = []
    flag = 0
    for c in list:
        r = run_cmd_one(c, encoding, print_log, **kwargs)
        result.append((r[1], r[2]))
        if r[0] != 0 and err_stop:
            flag = r[0]
            break
    return flag, result


def run_cmd_one(cmd, encoding="utf-8", print_log=True, timeout=None, **kwargs):
    logging.info(cmd)
    args = shlex.split(cmd)
    popen = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding=encoding,
                             **kwargs)

    while popen.poll() is None:
        line = popen.stdout.readline()
        line = line.strip()
        if line:
            logging.info(line)
    return popen.poll(), popen.stdout, popen.stderr


def run_cmd_one2(cmd, encoding="utf-8", print_log=True, timeout=None, **kwargs):
    logging.info(cmd)
    popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding=encoding,
                             **kwargs)

    while popen.poll() is None:
        line = popen.stdout.readline()
        line = line.strip()
        if line:
            logging.info(line)
    return popen.poll(), popen.stdout, popen.stderr


def str2date(str, pattern="%Y-%m-%d %H:%M:%S"):
    return time.strptime(str, pattern)


def date2str(date, pattern="%Y-%m-%d %H:%M:%S"):
    return time.strftime(pattern, date)


def print_stdout(stdout):
    for line in stdout.readlines():
        line = line.strip()
        print(line)
