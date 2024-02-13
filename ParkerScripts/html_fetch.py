from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
import time


def get_dynamic_html(url, output_file, scrolls = 0):
    options = Options()
    options.headless = True  # Run in headless mode
    # Specify the path to chromedriver.exe

    options.add_argument(r"--user-data-dir=D:\Mind\CRA\AI_Experiments\Job_Crawlers\Peter\adminlte-generator\chrome_profile")

    service = Service(executable_path=r"C:\Python3\chromedriver.exe")

    # Use the 'service' argument to specify the ChromeDriver path
    browser = webdriver.Chrome(service=service, options=options)

    try:
        browser.get(url)
        time.sleep(8)
        for i in range(scrolls):  # Determines how many times we scroll
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Wait 3 seconds between scrolls

        html_content = browser.page_source

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(html_content)
    finally:
        browser.quit()

if __name__ == "__main__":
    url = sys.argv[1]
    output_filename = sys.argv[2]
    get_dynamic_html(url, output_filename)
