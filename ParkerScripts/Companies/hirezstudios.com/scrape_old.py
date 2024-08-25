import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import threading
import json

def main(file_path):
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{file_path}")

    job_blocks = driver.find_elements(By.CSS_SELECTOR, ".JobBlockcss__ContainerWrapper-sc-6e8iiq-0.crSpzV.g-JobBlock")
    jobs = []
    for block in job_blocks:
        title = block.find_element(By.CSS_SELECTOR, ".job-title").text
        url_element = block.find_element(By.XPATH, ".//ancestor::a[contains(@href, 'http')]")
        url = url_element.get_attribute('href')
        jobs.append({"Job-title": title, "URL": url})

    driver.quit()
    print(json.dumps(jobs, indent=2))

if __name__ == "__main__":
    main(sys.argv[1])
