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
        job_elements = driver.find_elements(By.CSS_SELECTOR, "div.flex.flex-row.w-full.justify-between.rounded-[1.5em].border-2.border-solid.border-system-100.bg-system-0.p-[20px]")
        for job_element in job_elements:
            try:
                title_element = job_element.find_element(By.CSS_SELECTOR, "p.font-nexa-bold.text-[2.8em].laptop:text-[2.4em].tablet:text-[2em].font-bold.leading-inherited.w-full.lowercase.text-system-800")
                title = title_element.text.strip() if title_element.text.strip() else title_element.get_attribute('innerHTML').strip()
            except NoSuchElementException:
                title = "No Title Found"

            try:
                url_element = job_element.find_element(By.CSS_SELECTOR, "button.rounded-btn.tablet:rounded-[5px].text-system-0.bg-system-800.font-bold.hover:bg-system-900.whitespace-nowrap.transition-all.duration-200.ease-in-out.h-[50px].px-[25px].tablet:h-[40px].w-[150px].tablet:h-[40px].tablet:w-[130px]")
                url = url_element.get_attribute('href') if url_element.get_attribute('href') else "#"
            except NoSuchElementException:
                url = "#"

            job_listings.append({"Job-title": title, "URL": url})
    except NoSuchElementException:
        pass

    driver.quit()
    return json.dumps(job_listings, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))