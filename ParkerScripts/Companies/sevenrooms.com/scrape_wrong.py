import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def scrape_jobs(file_path):
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{str(threading.get_ident())}"
    service = Service(executable_path=r"C:\\Python3\\chromedriver.exe")
    
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    job_opening_selector = "div[class*='job'], ul[class*='job'], div[class*='career'], ul[class*='career'], div[class*='opening'], ul[class*='opening']"
    job_title_selector = "a"
    
    job_blocks = soup.select(job_opening_selector)
    
    job_openings = []
    for job_block in job_blocks:
        title_tag = job_block.select_one(job_title_selector)
        if title_tag:
            job_title = title_tag.get_text(strip=True)
            job_url = title_tag['href']
            job_openings.append({"Job-title": job_title, "URL": job_url})
    
    driver.quit()
    
    return json.dumps(job_openings, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))