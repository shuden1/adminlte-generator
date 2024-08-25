import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def main():
    if len(sys.argv) != 2:
        print("Usage: script.py <html_file_path>")
        sys.exit(1)

    html_file_path = sys.argv[1]
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{html_file_path}")

    job_openings = driver.find_elements(By.CSS_SELECTOR, "div.rt-list__offer-item[data-offer-id]")
    job_list = []

    for job in job_openings:
        title_element = job.find_element(By.CSS_SELECTOR, "span.rt-list__offer-title.rt__text.rt__text--secondary.rt__link")
        title = title_element.get_attribute('innerHTML').strip()
        url = "#"

        job_list.append({"Job-title": title, "URL": url})

    driver.quit()

    print(json.dumps(job_list, indent=4))

if __name__ == "__main__":
    main()
