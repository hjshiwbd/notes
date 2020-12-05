#  -*- coding:utf-8 -*-  
import logging
import utils
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s|%(levelname)s|%(process)d|%(filename)s.%(lineno)d|%(message)s',
                    datefmt='%y-%m-%d %H:%M:%S')


class ReportDetail:
    report = None
    report_url_domain = 'https://classic.warcraftlogs.com/'

    def __init__(self, report):
        self.report = report
        pass

    def damage(self):
        dmg_url = self.report_url_domain + self.report.link + '#boss=-3&difficulty=0&type=damage-done'

        ops = Options()
        ops.add_argument('--proxy-server=http://127.0.0.1:7890')
        ops.add_argument('headless')
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "permissions.default.stylesheet": 2
        }
        ops.add_experimental_option("prefs", prefs)
        # This example requires Selenium WebDriver 3.13 or newer
        with webdriver.Chrome(options=ops) as driver:
            logging.info(dmg_url)
            driver.get(dmg_url)
            WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(By.ID, 'main-table-0_wrapper'))
            # a = driver.page_source
            # print(a)
            trs = driver.find_elements(By.CSS_SELECTOR, "#main-table-0_wrapper tr.odd,#main-table-0_wrapper tr.even")

            arr = []
            # print("排名", "得分", "名字", "总量", "dps")
            for i, tr in enumerate(trs):
                # print(tr.get_attribute('outerHTML'))

                # main-table-performance,main-table-name,main-table-amount,main-per-second-amount
                performance = tr.find_element_by_css_selector('.main-table-performance').text
                name = tr.find_element_by_css_selector('.main-table-name').text
                player_class = tr.find_element_by_css_selector('.main-table-name .main-table-link a') \
                    .get_attribute("class").strip().lower()
                amount = tr.find_elements_by_css_selector('.main-table-amount>span')[0] \
                    .get_attribute("innerText").replace('$', '')
                dps = tr.find_element_by_css_selector('.main-per-second-amount').text
                # print((i + 1), performance, name, amount, dps)
                arr.append({
                    "performance": performance,
                    "name": name,
                    "amount": amount,
                    "dps": dps,
                    "class": player_class
                })

        # total = sum([int(x['amount']) for x in arr])
        # count = [x for x in arr if float(x['dps']) > 60]
        # v = total / len(count)
        # s = f"人均: {total}/{len(count)}={v}, 80%={v * 0.8}"
        # print(s)
        self.save_player_data(arr)
        self.save_report_player_data(arr, 'dmg')

    def heal(self):
        dmg_url = self.report_url_domain + self.report.link + '#type=healing&boss=-3&difficulty=0'

        ops = Options()
        ops.add_argument('--proxy-server=http://127.0.0.1:7890')
        ops.add_argument('headless')
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "permissions.default.stylesheet": 2
        }
        ops.add_experimental_option("prefs", prefs)
        # This example requires Selenium WebDriver 3.13 or newer
        with webdriver.Chrome(options=ops) as driver:
            logging.info(dmg_url)
            driver.get(dmg_url)
            WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(By.ID, 'main-table-0_wrapper'))
            # a = driver.page_source
            # print(a)
            trs = driver.find_elements(By.CSS_SELECTOR, "#main-table-0_wrapper tr.odd,#main-table-0_wrapper tr.even")

            arr = []
            # print("排名", "得分", "名字", "总量", "dps")
            for i, tr in enumerate(trs):
                # print(tr.get_attribute('outerHTML'))

                # main-table-performance,main-table-name,main-table-amount,main-per-second-amount
                performance = tr.find_element_by_css_selector('.main-table-performance').text
                name = tr.find_element_by_css_selector('.main-table-name').text
                player_class = tr.find_element_by_css_selector('.main-table-name .main-table-link a') \
                    .get_attribute("class").strip().lower()
                amount = tr.find_elements_by_css_selector('.main-table-amount>span')[0] \
                    .get_attribute("innerText").replace('$', '')
                hps = tr.find_element_by_css_selector('.main-per-second-amount').text
                # print((i + 1), performance, name, amount, dps)
                arr.append({
                    "performance": performance,
                    "name": name,
                    "amount": amount,
                    "dps": hps,
                    "class": player_class
                })

        # total = sum([int(x['amount']) for x in arr])
        # count = [x for x in arr if float(x['dps']) > 60]
        # v = total / len(count)
        # s = f"人均: {total}/{len(count)}={v}, 80%={v * 0.8}"
        # print(s)
        self.save_player_data(arr)
        self.save_report_player_data(arr, 'heal')

    def run(self):
        logging.info(self.report)
        # self.clear()
        self.damage()
        self.heal()

        pass

    def save_report_player_data(self, arr, report_type):
        count_sql = "select count(*) cc from test.wcl_report_player where report_id = %(report_id)s " \
                    "and player_name = %(player_name)s and report_type = %(report_type)s"
        sql = "insert into test.wcl_report_player (report_id,report_type,player_rank,player_name," \
              "player_amount,player_per_second,player_performance) values " \
              "(%(report_id)s, %(report_type)s, %(player_rank)s, %(player_name)s, " \
              "%(player_amount)s, %(player_per_second)s, %(player_performance)s)"
        with utils.connect_by_code('test001') as conn:
            for i, o in enumerate(arr):
                x = utils.query_one(conn, count_sql, {
                    "report_id": self.report.id,
                    "player_name": o['name'],
                    "report_type": report_type
                })
                if x.cc == 0:
                    utils.update(conn, sql, {
                        "report_id": self.report.id,
                        "report_type": report_type,
                        "player_rank": i + 1,
                        "player_name": o['name'],
                        "player_amount": o['amount'],
                        "player_per_second": o['dps'],
                        "player_performance": o['performance'],
                    })

        pass

    def save_player_data(self, arr):
        count_sql = 'select count(*) cc from test.wcl_player where name = %(name)s and class = %(class)s'
        insert_sql = 'insert into test.wcl_player (`name`,`class`) values (%(name)s,%(class)s)'
        with utils.connect_by_code('test001') as conn:
            for i, o in enumerate(arr):
                x = utils.query_one(conn, count_sql, {
                    "name": o['name'],
                    "class": o['class']
                })
                if x.cc == 0:
                    utils.update(conn, insert_sql, {
                        "name": o['name'],
                        "class": o['class']
                    })
        pass

    def clear(self):
        sql = 'delete FROM `wcl_report_player` where report_id =' + str(self.report.id)
        with utils.connect_by_code('test001') as conn:
            utils.update(conn, sql)
