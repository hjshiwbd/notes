# coding:utf-8
"""
CREATE TABLE `vehicle_sales_pcauto` (
  `id` bigint(20) NOT NULL,
  `data_date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '日期',
  `data_year` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '年',
  `data_month` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '月',
  `rank` int(11) DEFAULT NULL COMMENT '排名',
  `brand_lv1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '一级品牌',
  `brand_lv2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '二级品牌',
  `price_min` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '最低价',
  `price_max` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '最高价',
  `sales_num` int(10) DEFAULT NULL COMMENT '销量',
  `vehicle_type` varchar(2) DEFAULT NULL COMMENT '1car,2suv',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 231007加字段
alter table vehicle_sales_pcauto add sales_url varchar(255) comment '销量详情url';
alter table vehicle_sales_pcauto add is_ev varchar(1) comment '是否有电动款';
alter table vehicle_sales_pcauto add is_ice varchar(1) comment '是否有汽油款,ice内燃机';
alter table vehicle_sales_pcauto add is_fcev varchar(1) comment '是否有氢燃料电池';
alter table vehicle_sales_pcauto add displacement varchar(100) comment '排量';

pip:
pip install pysnowflake
pip install BeautifulSoup4
pip install html5lib
pip install python-dateutil
"""

import datetime
import json
import subprocess
import time
import logging
import utils
from bs4 import BeautifulSoup
import snowflake.client
import threading
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from lxml import etree
import re

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d|%(levelname)s|%(process)d|%(filename)s.%(lineno)d|%(message)s',
                    datefmt='%y-%m-%d %H:%M:%S')

# 启动雪花数服务的进程命令行
popen = None

mysql_host = 'slave001.yz'
mysql_port = 11502
mysql_user = 'huangj'
mysql_pass = 'hH01KgJMPbVJcYbNAzp@oVe9DdbL4Usg'

site_domain = 'https://price.pcauto.com.cn'

start = '2023-12'
end = '2023-12'

# vehcle_type = {
#     "car": "1",
#     "suv": "2",
#     "mpv": "3"
# }
vtype = ['1', '2', '3']
# vtype = ['2', '3']
# vtype = ['1']

# from_local = True
from_local = False
snowflake_port = 8910

# Set
all_type = set()


def get_html(vehicle_type, data_year, data_month):
    if from_local:
        return open("pcauto.html", encoding="gbk")
    else:
        url = f"{site_domain}/top/sales/s1-t{vehicle_type}-y{data_year}-m{data_month}.html"
        r = utils.get_url(url)
        return r.text


def snowflake_init():
    threading.Thread(target=idserver).start()
    time.sleep(1)
    snowflake.client.setup("localhost", snowflake_port)


def get_price(text):
    if text == '暂无报价':
        return "", ""
    else:
        text = text.replace('万', '')
        arr = text.split('-') if '-' in text else [text, text]
        return tuple(map(lambda x: int(Decimal(x) * 10000), arr))


def save_db(data_arr):
    with utils.connect(mysql_host, mysql_port, mysql_user, mysql_pass) as conn:
        sql = "insert into test.vehicle_sales_pcauto (id, data_date, data_year, data_month, `rank`, brand_lv1, " \
              "brand_lv2, price_min, price_max, sales_num, vehicle_type, is_ev, is_fcev, is_ice, sales_url, " \
              "displacement) " \
              "values " \
              "(%(id)s, %(data_date)s, %(data_year)s, %(data_month)s, %(rank)s, %(brand_lv1)s, %(brand_lv2)s, " \
              "%(price_min)s, %(price_max)s, %(sales_num)s, %(vehicle_type)s, %(is_ev)s, %(is_fcev)s, %(is_ice)s, " \
              "%(sales_url)s, %(displacement)s)"
        x = utils.update_many(conn, sql, data_arr)
        logging.info(f"{x} inserted")


def get_sales_detail_html(url):
    if from_local:
        a = open("sales_detail.html", encoding="utf-8")
        return "".join([x for x in a.readlines()])
    else:
        r = None
        for i in range(3):
            try:
                r = utils.get_url(url)
                break
            except Exception as e:
                logging.error(f"get_sales_detail_html error: {e}")
                time.sleep(3)
        return r.text


def get_energy_type(td_arr):
    """
    获取能源类型
    todo 如果一次获取多个月的数据, 这个方法会重复执行, 需要建立缓存
    :param td_arr:
    :return:
    """
    td = td_arr[1]
    url = f'{site_domain}{td.a["href"]}'
    raw = get_sales_detail_html(url)
    # time.sleep(3)
    html = etree.HTML(raw, etree.HTMLParser(encoding='utf-8'))
    # 排量
    types = html.xpath('//div[@class="fl s-data-l"]/p[1]/em/a/text()')
    # 电动, 燃油, 氢燃料
    is_ev = '0'
    is_ice = '0'
    is_fcev = '0'
    for v in types:
        if '氢燃料' in v:
            is_fcev = '1'
        elif '电动' in v:
            is_ev = '1'
        elif re.match(r'^\d+\.\d+[TLtl]$', v):
            # v满足正则 1.0T 或者 1.0L
            is_ice = '1'
    # print(types)
    # all_type.update(types)
    return {
        "is_ev": is_ev,
        "is_ice": is_ice,
        "is_fcev": is_fcev,
        "url": url,
        "displacement": json.dumps(types, ensure_ascii=False)
    }


def handle_one_month(vehicle_type, date):
    html = get_html(vehicle_type, date.year, date.month)
    # print(html)
    # return
    soup = BeautifulSoup(html, features="html5lib")
    level_table = soup.find('div', {'class': 'level-table'})
    level_table = level_table.table.tbody
    all = []
    n = 0
    trs = level_table.select('tr')
    for tr in trs:
        n = n + 1
        if n > 10000:
            break
        td_arr = tr.select('td')
        if len(td_arr) == 0:
            continue
        logging.info(f'{n}/{len(trs)}')
        id = get_id()
        data_date = date.strftime("%Y%m")
        rank = td_arr[0].text
        brand_lv1 = td_arr[3].text
        brand_lv2 = td_arr[1].text
        price_min, price_max = get_price(td_arr[2].text)
        sales_num = td_arr[4].text
        energy_type = get_energy_type(td_arr)
        is_ev = energy_type['is_ev']
        is_ice = energy_type['is_ice']
        is_fcev = energy_type['is_fcev']
        sales_url = energy_type['url']
        displacement = energy_type['displacement']

        # logging.info(f'{id}, {rank}, {brand_lv1}, {brand_lv2}, {price_min},
        # {price_max}, {sales_num}')
        all.append({
            "id": id,
            "data_year": date.year,
            "data_month": date.month,
            "data_date": data_date,
            "rank": rank,
            "brand_lv1": brand_lv1,
            "brand_lv2": brand_lv2,
            "price_min": price_min,
            "price_max": price_max,
            "sales_num": sales_num,
            "vehicle_type": vehicle_type,
            "is_ev": is_ev,
            "is_ice": is_ice,
            "is_fcev": is_fcev,
            "sales_url": sales_url,
            "displacement": displacement
        })

    logging.info(f'data len: {len(all)}')
    save_db(all)


def run():
    snowflake_init()
    d = datetime.datetime.strptime(start, '%Y-%m')
    while True:
        for i in vtype:
            handle_one_month(i, d)
            logging.info("processing")
            time.sleep(3)
        d = d + relativedelta(months=1)
        d2 = d.strftime('%Y-%m')

        if d2 > end:
            break
    logging.info("finish")
    # 程序不会真的停止,因为cmd开启了一个服务
    global popen
    popen.terminate()


def idserver():
    run_cmd_one2(f"snowflake_start_server --port={snowflake_port}")


def run_cmd_one2(cmd, encoding="utf-8", print_log=True, **kwargs):
    logging.info(cmd)
    global popen
    popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding=encoding,
                             **kwargs)

    while popen.poll() is None:
        if print_log:
            line = popen.stdout.readline()
            line = line.strip()
            if line:
                logging.info(line)
            # time.sleep(0.1)
    return popen


def get_id():
    return snowflake.client.get_guid()


class MysqlProp:

    def __init__(self, **kwargs):
        self.mysql_host = kwargs['mysql_host']
        self.mysql_port = kwargs['mysql_port']
        self.mysql_user = kwargs['mysql_user']
        self.mysql_pass = kwargs['mysql_pass']


if __name__ == '__main__':
    run()
