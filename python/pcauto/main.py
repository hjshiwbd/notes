# coding:utf-8
"""
使用了无头浏览器, 需要有访问Google的能力才能运行本程序
chromedriver下载
https://registry.npmmirror.com/binary.html?path=chrome-for-testing/

CREATE TABLE `vehicle_info` (
  `id` bigint NOT NULL,
  `code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT 'pcauto网站的唯一编码',
  `brand_lv1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '一级品牌',
  `brand_lv2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '二级品牌',
  `price_min` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '最低价',
  `price_max` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '最高价',
  `vehicle_type` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '1car,2suv,3mpv',
  `length` int NOT NULL DEFAULT '-1' COMMENT '长mm',
  `width` int NOT NULL DEFAULT '-1' COMMENT '宽mm',
  `height` int NOT NULL DEFAULT '-1' COMMENT '高mm',
  `wheelbase` int NOT NULL DEFAULT '-1' COMMENT '轴距mm',
  `gate_count` int NOT NULL DEFAULT '-1' COMMENT '车门数',
  `seat_count` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '-1' COMMENT '座位数',
  `energy_type` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '能源类型',
  `weight` int NOT NULL DEFAULT '-1' COMMENT '车身重量kg',
  `displacement` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '排量',
  `inlet` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '进气形式',
  `engine_power` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '-1' COMMENT '发动机功率',
  `motor_power` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '-1' COMMENT '电动机功率',
  `sales_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '详情url',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `cltc` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '纯电续航里程',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='车辆基本信息';

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
  `sales_url` varchar(255) DEFAULT NULL COMMENT '销量详情url',
  `is_ev` varchar(1) DEFAULT NULL COMMENT '是否有电动款',
  `is_ice` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '是否汽油款,ice内燃机',
  `is_fcev` varchar(1) DEFAULT NULL COMMENT '是否有氢燃料电池',
  `displacement` varchar(100) DEFAULT NULL COMMENT '排量',
  `vehicle_id` bigint(20) DEFAULT NULL COMMENT 'vehicle_info的id',
  `code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'pcauto网站的车型唯一值',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

pip:
pip install pysnowflake
pip install BeautifulSoup4
pip install html5lib
pip install python-dateutil
pip install selenium
"""

import os
import datetime
import json
import subprocess
import time
import logging

import dbutils
import requests
import utils
from bs4 import BeautifulSoup
import snowflake.client
import threading
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from lxml import etree
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.firefox.service import Service

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

start = '2025-06'
end = '2025-09'

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

"""
能源可能类型
1 汽油
2 柴油
3 油电混动
4 插电混动
5 纯电动
6 增程式
7 氢燃料电池
"""
ice_types = ['汽油', '柴油', '油电混动']
ev_types = ['插电混动', '纯电动', '增程式']
fcev_types = ['氢燃料电池']

# Chromedirver 禁用下载提示
os.environ['CHROME_DRIVER_DISABLE_DOWNLOAD_PROMPT'] = '1'

options = ChromeOptions()
options.add_argument('--proxy-server=127.0.0.1:7897')  # proxy
options.add_argument('--headless')  # 无头模式
options.add_argument('--disable-gpu')  # 如果没有显卡支持，添加此参数
options.add_argument('--no-sandbox')  # Bypass OS security model
options.add_argument('--disable-dev-shm-usage')  # overcome limited resource problems

# Chrome
web_driver = webdriver.Chrome(options=options)

# vehcile_info更新周期,天
vehcile_info_update_interval = 180


def get_url_headless(url):
    """
    url是脚本处理过的, 用无头浏览器来获取信息
    """
    # 设置选项

    # Chrome
    logging.info(f"loading {url}")

    # firefox
    # "D:\\browser_dirvers\\geckodriver.exe"
    # capabilities2 = webdriver.DesiredCapabilities.FIREFOX
    # service = Service(executable_path="D:\\browser_dirvers\\geckodriver.exe")
    # driver = webdriver.Firefox(options=options)

    try:
        # 加载网页
        web_driver.get(url)

        # 等待页面完全加载
        web_driver.implicitly_wait(3)  # seconds

        # 获取渲染后的HTML
        return web_driver.page_source
    except Exception as e:
        logging.error(f"{url} error: {e}")
        raise e


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
              "displacement,code) " \
              "values " \
              "(%(id)s, %(data_date)s, %(data_year)s, %(data_month)s, %(rank)s, %(brand_lv1)s, %(brand_lv2)s, " \
              "%(price_min)s, %(price_max)s, %(sales_num)s, %(vehicle_type)s, %(is_ev)s, %(is_fcev)s, %(is_ice)s, " \
              "%(sales_url)s, %(displacement)s,%(code)s)"
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


def arr_join(arr1, arr2):
    """
    2个数组求交集
    :return:
    """
    return list(set(arr1) & set(arr2))


def handle_one_month(vehicle_type, date):
    """
    处理一个月的数据
    :param vehicle_type:
    :param date:
    :return:
    """
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
            # 提前停止, 测试用
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
        # 默认值
        energy_type = {
            "is_ev": '',
            "is_ice": '',
            "is_fcev": '',
            "url": '',
            "displacement": ''
        }
        is_ev = energy_type['is_ev']
        is_ice = energy_type['is_ice']
        is_fcev = energy_type['is_fcev']
        sales_url = energy_type['url']
        displacement = energy_type['displacement']
        # 链接信息,/salescar/sg27043/ -> sg27043, 得到唯一值
        code = td_arr[1].a["href"].replace("/salescar/", "").replace("/", "")

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
            "displacement": displacement,
            "code": code,
        })

    logging.info(f'data len: {len(all)}')
    save_db(all)
    save_vehcile_info(all)


def run():
    snowflake_init()
    # 当前时间
    d = datetime.datetime.strptime(start, '%Y-%m')
    while True:
        # 3个车类型: 轿车, suv, mpv
        for i in vtype:
            # 处理一个月的数据
            handle_one_month(i, d)
            logging.info("processing")
            time.sleep(3)
        # 加一个月
        d = d + relativedelta(months=1)
        d2 = d.strftime('%Y-%m')

        if d2 > end:
            break

    web_driver.quit()

    logging.info("finish")
    # 程序不会真的停止,因为cmd开启了一个服务, 需要关闭 subprocess.Popen


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


def query_vehicle_info():
    """
    本地的车辆信息
    todo x天未更新在内存里进行, 不在sql
    :return:
    """
    sql = f"select * from test.vehicle_info"
    with utils.connect(mysql_host, mysql_port, mysql_user, mysql_pass) as conn:
        return dbutils.query_list(conn, sql)


def parse_engergy(content_xpath):
    # 能源类型
    types_raw = content_xpath.xpath('//div[@class="energy-type-item-container"]/span/text()')
    # types 是array 要剔重
    return ','.join(set(types_raw))


def resolve_xpath(content_xpath, value):
    return content_xpath.xpath(value)


def is_number(str):
    return re.match("^[+-]?\d+(\.\d+)?$", str.strip()) is not None


def get_vehicle_info(code):
    """
    获取车辆信息
    :param code:
    :return:
    """

    def get_html_xpath(url):
        """
        获取配置页面里的所有能源类型,剔重
        :param url:
        :return: 剔重set
        """
        # 获取渲染后的HTML
        rendered_html = get_url_headless(url)
        # with open(code + '.html', 'w', encoding='utf-8') as iiio:
        #     iiio.write(rendered_html)

        # rendered_html = ''
        # with open(code + '.html', 'r', encoding='utf-8') as io:
        #     rendered_html = io.read()

        html = etree.HTML(rendered_html, etree.HTMLParser(encoding='utf-8'))
        return html

    # 用selenium爬取页面, 得到页面代码的xpath对象
    url = f'{site_domain}/{code}/config.html'
    content_xpath = get_html_xpath(url)

    # 暂无参培结果
    empty_description = resolve_xpath(content_xpath, '//p[@class="baseEmpty-description"]/text()')
    if len(empty_description) > 0:
        if '暂无' in empty_description[0]:
            logging.info('暂无参数配置')
            return None

    # 能源类型
    energy_type = parse_engergy(content_xpath)
    brand_lv1 = resolve_xpath(content_xpath, '//div[@id="common-breadcrumbs"]/a[3]/text()')[0]
    brand_lv2 = resolve_xpath(content_xpath, '//div[@id="common-breadcrumbs"]/a[last()]/text()')[0]
    price_list = resolve_xpath(content_xpath,
                               '//div[@class="table-wrapper mr-10 w-fit"]/div[1]/div[1]/div[@class="table-cell"]/div[1]/div[@class="official-price"]/span[@class="price"]/text()')
    # price_list过滤掉不是数字的项
    price_list = sorted([x.replace('万', '') for x in price_list])  # 排序
    price_list = list(filter(is_number, price_list))
    price_min = int(Decimal(price_list[0]) * 10000)  # 最低
    price_max = int(Decimal(price_list[-1]) * 10000)  # 最高
    # int(Decimal(x) * 10000)
    length = resolve_xpath(content_xpath,
                           '//div[@data-key="wcLength"]/div[@class="table-cell"]/div[1]/div[1]/text()')[0].strip()
    width = resolve_xpath(content_xpath,
                          '//div[@data-key="wcWidth"]/div[@class="table-cell"]/div[1]/div[1]/text()')[0].strip()
    height = resolve_xpath(content_xpath,
                           '//div[@data-key="wcHeight"]/div[@class="table-cell"]/div[1]/div[1]/text()')[0].strip()
    # 轴距
    wheelbase = resolve_xpath(content_xpath,
                              '//div[@data-key="wcZj"]/div[@class="table-cell"]/div[1]/div[1]/text()')[0].strip()
    # 车门数
    gate_count = resolve_xpath(content_xpath,
                               '//div[@data-key="gateCount"]/div[@class="table-cell"]/div[1]/div[1]/text()')[0].strip()
    # 座位数
    seat_count = resolve_xpath(content_xpath,
                               '//div[@data-key="rjBzzw"]/div[@class="table-cell"]/div[1]/div[1]/text()')[0].strip()
    # 车重kg
    weight = resolve_xpath(content_xpath,
                           '//div[@data-key="wcCszl"]/div[@class="table-cell"]/div[1]/div[1]/text()')
    weight = list(filter(is_number, map(lambda v: v.strip(), weight)))
    if len(weight) > 0:
        weight = weight[0]
    else:
        weight = 0
    # 排量
    displacement = resolve_xpath(content_xpath,
                                 '//div[@data-key="yqPlcc"]/div[@class="table-cell"]/div[1]/div[1]/text()')
    if displacement:
        displacement = ','.join(set([v.strip() for v in displacement]))
    else:
        displacement = ''
    # 进气:自然吸气,涡轮增压
    inlet = resolve_xpath(content_xpath,
                          '//div[@data-key="yqZylx"]/div[@class="table-cell"]/div[1]/div[1]/text()')
    if inlet:
        inlet = inlet[0].strip()
    else:
        inlet = ''
    # 发动机功率
    engine_power = resolve_xpath(content_xpath,
                                 '//div[@data-key="yqGl#1"]/div[@class="table-cell"]/div[1]/div[1]/text()')
    if engine_power:
        engine_power = ','.join(set([v.strip() for v in engine_power]))
    else:
        engine_power = ''
    # 电动机功率
    motor_power = resolve_xpath(content_xpath,
                                '//div[@data-key="ddZdgl#1"]/div[@class="table-cell"]/div[1]/div[1]/text()')
    if motor_power:
        motor_power = ','.join(set([v.strip() for v in motor_power]))
    else:
        motor_power = ''
    # cltc续航
    cltc = resolve_xpath(content_xpath, '//div[@data-key="ddCltc#1"]/div[@class="table-cell"]/div[1]/div[1]/text()')
    if cltc:
        cltc = ','.join(set([v.strip() for v in cltc]))
    else:
        cltc = ''

    # gateCount rjBzzw wcCszl yqZylx
    val = {
        "code": code,
        "brand_lv1": brand_lv1,
        "brand_lv2": brand_lv2,
        "price_min": price_min,
        "price_max": price_max,
        "vehicle_type": '',
        "length": length,
        "width": width,
        "height": height,
        "wheelbase": wheelbase,
        "gate_count": gate_count,
        "seat_count": seat_count,
        "energy_type": energy_type,
        "weight": weight,
        "displacement": displacement,
        "inlet": inlet,
        "engine_power": engine_power,
        "motor_power": motor_power,
        "sales_url": url,
        "cltc": cltc,
    }
    logging.info(val)

    return val


def update_vehcile_info(info):
    with utils.connect(mysql_host, mysql_port, mysql_user, mysql_pass) as conn:
        sql = (
            "UPDATE `test`.`vehicle_info` SET `code` = %(code)s, `brand_lv1` = %(brand_lv1)s, `brand_lv2` = %(brand_lv2)s, "
            "`price_min` = %(price_min)s, `price_max` = %(price_max)s, `vehicle_type` = %(vehicle_type)s, `length` = %(length)s, "
            "`width` = %(width)s, `height` = %(height)s, `wheelbase` = %(wheelbase)s, `gate_count` = %(gate_count)s, `seat_count` = %(seat_count)s, "
            "`energy_type` = %(energy_type)s, `weight` = %(weight)s, `displacement` = %(displacement)s, `inlet` = %(inlet)s, "
            "`engine_power` = %(engine_power)s, `motor_power` = %(motor_power)s, `sales_url` = %(sales_url)s, update_time = now(),cltc = %(cltc)s "
            "WHERE `id` = %(id)s;")
        x = utils.update(conn, sql, info)
        logging.info(f"{x} updated")


def insert_vehcile_info(info):
    with utils.connect(mysql_host, mysql_port, mysql_user, mysql_pass) as conn:
        sql = (
            "INSERT INTO `test`.`vehicle_info` (`id`, `code`, `brand_lv1`, `brand_lv2`, `price_min`, `price_max`, "
            "`vehicle_type`, `length`, `width`, `height`, `wheelbase`, `gate_count`, `seat_count`, `energy_type`, "
            "`weight`, `displacement`, `inlet`, `engine_power`, `motor_power`, `sales_url`,cltc) VALUES (%(id)s, %(code)s, "
            "%(brand_lv1)s, %(brand_lv2)s, %(price_min)s, %(price_max)s, %(vehicle_type)s, %(length)s, %(width)s, "
            "%(height)s, %(wheelbase)s, %(gate_count)s, %(seat_count)s, %(energy_type)s, "
            "%(weight)s, %(displacement)s, %(inlet)s, %(engine_power)s, %(motor_power)s, %(sales_url)s),%(cltc)s;")
        x = utils.update(conn, sql, info)
        logging.info(f"{x} inserted")


def save_vehcile_info(api_list):
    """
    独立存储车辆基本信息
    原有销量表不适合存车辆基本信息,比如能源类型/车辆类型等等
    :param api_list: 爬取到的车辆排名数据
    :return:
    """
    # 本地库的车辆列表, 如果api_list.code不在local_list里, 就为此code去爬取数据, 并写入数据库
    local_list = query_vehicle_info()
    # 需要update的, 单个元素是数据库表对象(tuple)
    fetch_code_list_update = []
    # 需要insert的, 单个元素是dict
    fetch_code_list_insert = []
    # 本地列表, 超过x天未更新就需要获取最新数据更新一下
    index = 0
    for local in local_list:
        update_time = local.update_time
        # update_time是datetime类型 当前时间now()和update_time之间相差的时间
        now_timestamp = int(datetime.datetime.timestamp(datetime.datetime.now()) * 1000)
        update_time_timestamp = int(datetime.datetime.timestamp(update_time) * 1000)
        # 预设值的毫秒
        offset = vehcile_info_update_interval * 86400000
        if now_timestamp - update_time_timestamp > offset:
            # x天未更新过, 需要更新
            index = index + 1
            logging.info(f'{index}/{len(local_list)} update:{local.code}')
            info = get_vehicle_info(local.code)
            if not info:
                continue
            info['id'] = local.id
            info['vehicle_type'] = local.vehicle_type
            update_vehcile_info(info)
    # 排名数据里在本地不存在的code相当于是新车上市,有了销量, 也需要获取车辆信息
    local_code_list = [v.code for v in local_list]
    index2 = 0
    for api in api_list:
        code = api['code']
        if code not in local_code_list:
            index2 = index2 + 1
            logging.info(f'{index2}/{len(api_list)} insert:{code}')
            info = get_vehicle_info(code)
            if not info:
                continue
            info['id'] = get_id()
            info['vehicle_type'] = api['vehicle_type']
            insert_vehcile_info(info)


def run2():
    today = datetime.datetime.now()
    # today - 60 days
    start_time = today - datetime.timedelta(days=180)
    time_d = datetime.datetime.strftime(start_time, "%Y-%m-%d")
    print(time_d)


if __name__ == '__main__':
    # run()

    save_vehcile_info([])
