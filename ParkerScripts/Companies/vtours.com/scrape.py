import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_jobs(file_path):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(f"file:///{file_path}")
    
    job_openings = []
    
    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div.dvinci-job-widget')
    for job_block in job_blocks:
        title_tags = job_block.find_elements(By.CSS_SELECTOR, 'a')
        for title_tag in title_tags:
            title = title_tag.get_attribute('innerText').strip()
            url = title_tag.get_attribute('href')
            if title:  # Ensure the title is not empty
                job_openings.append({"Job-title": title, "URL": url})
    
    driver.quit()
    
    return json.dumps(job_openings, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))