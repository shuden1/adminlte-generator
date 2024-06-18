from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading, json, sys

def scrape_job_listings(html_file_path):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_path}")

    job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-listing .job-title a")
    job_listings = []

    for job_element in job_elements:
        job_title = job_element.text.strip()
        job_url = job_element.get_attribute("href")
        job_listings.append({"Job-title": job_title, "URL": job_url})
    
    driver.quit()
    
    return json.dumps(job_listings, indent=2)

if __name__ == "__main__":
    target_html_file_name = sys.argv[1]
    print(scrape_job_listings(target_html_file_name))