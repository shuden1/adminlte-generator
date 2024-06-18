import sys
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def main(html_file):
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_profile_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file}")
    
    job_listings = []
    # Assuming the corrected selectors based on the previously discussed guidelines:
    for job in driver.find_elements(By.CSS_SELECTOR, ".job-listing a"):
        job_title = job.text.strip()
        job_url = job.get_attribute("href").strip()
        job_listings.append({"Job-title": job_title, "URL": job_url})
    
    driver.quit()
    print(job_listings)

if __name__ == "__main__":
    file_path = sys.argv[1]
    main(file_path)