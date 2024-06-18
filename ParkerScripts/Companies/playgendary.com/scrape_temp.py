import sys
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape_job_listings(html_file):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = webdriver.ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file}")
    
    job_elements = driver.find_elements(By.CSS_SELECTOR, '._1G_RQ ._3ZuUt')
    job_listings = []

    for job in job_data:
        job_title_element = job.find_element(By.CSS_SELECTOR, 'h4.qRdGj')
        job_title = job_title_element.text.strip() if job_title_element else ""

        job_url = job.get_attribute('href') if job.get_attribute('href') else ""
        job_listings.append({"Job-title": job_title, "URL": job_url})
    
    driver.quit()
    return job_listings

if __name__ == '__main__':
    html_path = sys.argv[1]
    results = scrape_job_listings(html_path)
    print(results)