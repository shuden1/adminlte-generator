from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import sys
import json

# Job opening block selector
job_block_selector = 'a[style*="border: 1px solid rgba(255, 255, 255, 0.13); border-radius: 4px;"]'

# Job title and URL selector inside the block
job_title_selector = 'div[style*="flex: 4 1 180px;"] > div[style*="font-size: 14px;"]'
job_url_selector = 'div[style*="margin-top: 6px;"] > div'

# Scrape job listings
def scrape_job_listings(filename):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(options=options) as driver:
        driver.get(f'file:///{filename}')

        job_listings = []
        job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
        for job_element in job_elements:
            title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
            url_element = job_element.find_element(By.CSS_SELECTOR, job_url_selector)
            job_listings.append({
                'Job-title': title_element.text.strip(),
                'URL': url_element.text.strip(),
            })
        return job_listings

if __name__ == '__main__':
    target_html_file = sys.argv[1]
    job_listings = scrape_job_listings(target_html_file)
    print(json.dumps(job_listings))
