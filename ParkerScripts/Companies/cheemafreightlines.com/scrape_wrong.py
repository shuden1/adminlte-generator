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
        job_elements = driver.find_elements(By.CSS_SELECTOR, 'div.col-md-12.innerContent.col_left[data-animate="fade"][data-col="full"][data-delay="500"][data-title="1st column"][data-trigger="none"][id="col-full-146"][style="outline: none;"]')
        for job_element in job_elements:
            try:
                title_element = job_element.find_element(By.CSS_SELECTOR, 'h1.ne.elHeadline.hsSize3.lh4.elMargin0.elBGStyle0.hsTextShadow0.deneg1pxLetterSpacing.mfs_20[contenteditable="false"][data-bold="inherit"][data-gramm="false"][style="text-align: left; font-size: 32px;"]')
                title = title_element.text.strip() if title_element.text.strip() else title_element.get_attribute('innerHTML').strip()
            except NoSuchElementException:
                title = "No Title Found"

            try:
                url_element = job_element.find_element(By.CSS_SELECTOR, 'a[href][id="link-64790-131"][rel="noopener noreferrer"][style="color: rgb(47, 47, 47);"][target="_parent"]')
                url = url_element.get_attribute('href').strip() if url_element.get_attribute('href').strip() else "#"
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