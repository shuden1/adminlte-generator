import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def scrape_jobs(file_path):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{file_path}")

    job_listings = []

    try:
        job_elements = driver.find_elements(By.CSS_SELECTOR, "div#greenhouse-jobs a.transition-all.group.hover\\:translate-x-1.hover\\:shadow-2xl.hover\\:bg-primary-400.mb-6.flex.items-center.justify-between.bg-white.rounded-2xl.py-6.md\\:py-8.pr-10.md\\:pr-14.md\\:pl-10.pl-8")
        for job_element in job_elements:
            try:
                title_element = job_element.find_element(By.CSS_SELECTOR, "span.block.w-full.text-black.font-semibold.text-2xl.mb-2")
                job_title = title_element.text.strip() if title_element.text.strip() else title_element.get_attribute('innerHTML').strip()
            except NoSuchElementException:
                job_title = "No Title Found"

            job_url = job_element.get_attribute('href') if job_element.get_attribute('href') else "#"

            job_listings.append({"Job-title": job_title, "URL": job_url})
    except NoSuchElementException:
        pass

    driver.quit()
    return json.dumps(job_listings, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))