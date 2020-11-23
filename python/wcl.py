# coding:utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def document_initialised(driver):
    return driver.execute_script("return initialised")


def run():
    #
    id = "RP4bMYDjNgrx8Jdp"
    # id = "h4CzyDxgVLc87njp"
    url = 'https://classic.warcraftlogs.com/reports/' + id
    suffix = '#boss=-3&difficulty=0&type=damage-done'
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
        driver.get(url + suffix)
        WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(By.ID, 'main-table-0_wrapper'))
        # a = driver.page_source
        # print(a)
        trs = driver.find_elements(By.CSS_SELECTOR, "#main-table-0_wrapper tr.odd,#main-table-0_wrapper tr.even")

        arr = []
        print("排名", "得分", "名字", "总量", "dps")
        for i, tr in enumerate(trs):
            # print(tr.get_attribute('outerHTML'))

            # main-table-performance,main-table-name,main-table-amount,main-per-second-amount
            performance = tr.find_element_by_css_selector('.main-table-performance').text
            name = tr.find_element_by_css_selector('.main-table-name').text
            amount = tr.find_elements_by_css_selector('.main-table-amount>span')[0] \
                .get_attribute("innerText").replace('$', '')
            dps = tr.find_element_by_css_selector('.main-per-second-amount').text
            print((i + 1), performance, name, amount, dps)
            arr.append({
                "performance": performance, "name": name, "amount": amount, "dps": dps
            })

            # print("###################################################################")

        total = sum([int(x['amount']) for x in arr])
        count = [x for x in arr if float(x['dps']) > 60]
        v = total / len(count)
        s = f"人均: {total}/{len(count)}={v}, 80%={v * 0.8}"
        print(s)
    pass


if __name__ == '__main__':
    run()
