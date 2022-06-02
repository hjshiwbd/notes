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
"""

import datetime
import time
import logging
import utils
from bs4 import BeautifulSoup
import snowflake.client
import threading
from decimal import Decimal
from dateutil.relativedelta import relativedelta

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d|%(levelname)s|%(process)d|%(filename)s.%(lineno)d|%(message)s',
                    datefmt='%y-%m-%d %H:%M:%S')

mysql_host = '192.168.0.115'
mysql_port = 3306
mysql_user = 'huangj'
mysql_pass = 'hUaNgj_2020'

vehcle_type = {
    "car": "1",
    "suv": "2",
    "mpv": "3"
}
vtype = ['1','2','3']

# from_local = True
from_local = False
snowflake_port = 8910

start = '2022-02'
end = '2022-04'


def get_html(vehicle_type, data_year, data_month):
    if from_local:
        return open("pcauto.html", encoding="gbk")
    else:
        url = f"https://price.pcauto.com.cn/top/sales/s1-t{vehicle_type}-y{data_year}-m{data_month}.html"
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


def handle_one_month(vehicle_type, date):
    html = get_html(vehicle_type, date.year, date.month)
    # print(html)
    # return
    soup = BeautifulSoup(html, features="html5lib")
    level_table = soup.find('div', {'class': 'level-table'})
    level_table = level_table.table.tbody
    all = []
    for tr in level_table.select('tr'):
        td_arr = tr.select('td')
        if len(td_arr) == 0:
            continue
        id = get_id()
        data_date = date.strftime("%Y%m")
        rank = td_arr[0].text
        brand_lv1 = td_arr[3].text
        brand_lv2 = td_arr[1].text
        price_min, price_max = get_price(td_arr[2].text)
        sales_num = td_arr[4].text
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
            "vehicle_type": vehicle_type
        })
    with utils.connect(mysql_host, mysql_port, mysql_user, mysql_pass) as conn:
        sql = "insert into torna.vehicle_sales_pcauto (id, data_date, data_year, data_month, `rank`, brand_lv1, " \
              "brand_lv2, price_min, price_max, sales_num, vehicle_type) values " \
              "(%(id)s, %(data_date)s, %(data_year)s, " \
              "%(data_month)s, %(rank)s, %(brand_lv1)s, %(brand_lv2)s, %(price_min)s, %(price_max)s, " \
              "%(sales_num)s, %(vehicle_type)s)"
        x = utils.update_many(conn, sql, all)
        logging.info(f"{x} inserted")


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


def idserver():
    utils.run_cmd_one2(f"snowflake_start_server --port={snowflake_port}")


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
