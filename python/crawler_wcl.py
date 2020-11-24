from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(executable_path="E:\\webdrivers\\chromedriver.exe",)

url = '''
https://classic.warcraftlogs.com/reports/h4CzyDxgVLc87njp#boss=-3&difficulty=0&type=damage-done
'''.strip()
browser.get(url)
div = browser.find_elements_by_class_name('qc-cmp2-summary-buttons')
print(div)
btns = div[0].find_element_by_tag_name('button')
print(btns)
# browser.find_element_by_id("kw").send_keys("selenium")
# browser.find_element_by_id("su").click()
