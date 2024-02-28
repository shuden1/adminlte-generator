from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Step 1: Identifying the EXACT HTML selectors
job_block_selector = "ul.ant-list-items > li.ant-list-item"
job_title_selector = "h4.ant-list-item-meta-title > p"
job_url_selector = "div.ant-list-item-meta-avatar > a"

# Step 2: Create a Python + Selenium script
def scrape_job_listings(html_file_path):
    driver = webdriver.Chrome()
    driver.get(f"file:///{html_file_path}")
    
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    job_listings = []

    for block in job_blocks:
        job_title_element = block.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = job_title_element.text.strip().replace('\n', ' ')
        job_url_element = block.find_element(By.CSS_SELECTOR, job_url_selector)
        job_url = job_url_element.get_attribute('href')

        job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file = sys.argv[1]
    print(scrape_job_listings(html_file))