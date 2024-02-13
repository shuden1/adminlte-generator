from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys


def scrape_job_listings(html_file):
    driver = webdriver.Chrome()
    driver.get(f"file:///{html_file}")

    job_listings = []

    # Use the exact selectors as identified in the previous steps (STEP 1)
    job_blocks = driver.find_elements(By.CSS_SELECTOR, '.b-jobs-container .w-dyn-item')
    for job_block in job_blocks:
        title_element = job_block.find_element(By.CSS_SELECTOR, '.b-job-title div')
        link_element = job_block.find_element(By.CSS_SELECTOR, 'a.b-job-row')
        job_listings.append({"Job-title": title_element.text, "URL": link_element.get_attribute('href')})

    driver.quit()

    return json.dumps(job_listings)


if __name__ == "__main__":
    html_file = sys.argv[1]
    print(scrape_job_listings(html_file))