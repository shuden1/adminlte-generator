from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import sys
import time
import os
import shutil

import threading


def remove_script_tags(input_html_file):
    """
    Remove all <script> tags from the input HTML file and update the file.

    Parameters:
    input_html_file (str): Path to the HTML file to be processed.
    """
    with open(input_html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    for script in soup.find_all('script'):
        script.decompose()

    with open(input_html_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))

def get_dynamic_html(url, output_file, scrolls=4):
    options = Options()
    options.headless = True  # Run in headless mode
    options.add_argument("--no-sandbox")  # Recommended for running in headless mode in certain environments
    options.add_argument("--disable-gpu")  # Recommended for running in headless mode

    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\"+str(threading.get_ident())

    os.makedirs(profile_folder_path, exist_ok=True)
    options.add_argument(f"--user-data-dir={profile_folder_path}")
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")

    browser = webdriver.Chrome(service=service, options=options)

    try:
        browser.get(url)
        time.sleep(8)  # Wait for the initial page to load
        for i in range(scrolls):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait 2 seconds between scrolls

        # Get main page source
        html_content = browser.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Fetch and replace content in iframes
        iframe_elements = browser.find_elements(By.TAG_NAME, "iframe")
        for index, iframe in enumerate(iframe_elements):
            # Switch to the iframe
            try:
                browser.switch_to.frame(iframe)
                iframe_content = browser.page_source
                iframe_soup = BeautifulSoup('<div class="replaced-iframe">' + iframe_content + '</div>', 'html.parser')

                # Locate the original iframe in the soup and replace it
                original_iframe = soup.find_all('iframe')[index]
                original_iframe.replace_with(iframe_soup)

                # Switch back to the main document context
                browser.switch_to.default_content()
            except Exception as e:
                print(f"Error processing iframe {index}: {e}")

        # Write the modified HTML content to a file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(str(soup))

    finally:
        browser.quit()
        remove_script_tags(output_filename)
        if os.path.exists(profile_folder_path) and os.path.isdir(profile_folder_path):
            shutil.rmtree(profile_folder_path)

if __name__ == "__main__":

    url = sys.argv[1]
    output_filename = sys.argv[2]

    get_dynamic_html(url, output_filename)
