import sys
import json
import shutil
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService

def main(target_html_file):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{target_html_file}")

    job_selector = ".card-content"
    title_selector = "h2"
    link_selector = "a"

    job_elements = driver.find_elements(By.CSS_SELECTOR, job_selector)
    job_listings = []

    for element in job_elements:
        title_element = element.find_element(By.CSS_SELECTOR, title_selector)
        link_element = element.find_element(By.CSS_SELECTOR, link_selector)
        title = title_element.text.strip()
        link = link_element.get_attribute('href').strip()

        job_listings.append({"Job-title": title, "URL": link})

    driver.quit()


    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file = sys.argv[1]
    print(main(html_file))
