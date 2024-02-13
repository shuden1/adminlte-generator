from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
import time

from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection

def get_dynamic_html(url, output_file):
    options = Options()

    SBR_WEBDRIVER = 'https://brd-customer-hl_e45aadc0-zone-scraping_browser:m6mv09htx0f2@brd.superproxy.io:9515'

    options.add_argument(r"--user-data-dir=D:\Mind\CRA\AI_Experiments\Job_Crawlers\Peter\adminlte-generator\chrome_profile")

    service = Service()

    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    browser = Remote(sbr_connection, options=ChromeOptions())

    try:
        print('Waiting captcha to solve...')
        solve_res = browser.execute('executeCdpCommand', {
            'cmd': 'Captcha.waitForSolve',
            'params': {'detectTimeout': 10000},
        })
        print('Captcha solve status:', solve_res['value']['status'])

        browser.get(url)
        time.sleep(8)
        html_content = browser.page_source

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(html_content)
    finally:
        browser.quit()

if __name__ == "__main__":
    url = sys.argv[1]
    output_filename = sys.argv[2]
    get_dynamic_html(url, output_filename)
