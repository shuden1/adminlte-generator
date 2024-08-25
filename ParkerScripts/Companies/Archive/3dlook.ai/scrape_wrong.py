from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import sys
import json

# Selenium script to scrape job listings
def scrape_jobs(html_file):
    driver = webdriver.Chrome()

    driver.get(f"file://{html_file}")

    # Scrape the job opportunities
    job_listings = driver.find_elements(By.CSS_SELECTOR, "#opportunities + .elementor-container .elementor-text-editor > ul > li")
    jobs_data = []

    for listing in job_listings:
        title_element = listing.find_element(By.CSS_SELECTOR, "a")
        title = title_element.text
        link = title_element.get_attribute("href")

        jobs_data.append({
            "Job-title": title,
            "URL": link
        })

    driver.quit()
    return json.dumps(jobs_data)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(scrape_jobs(html_file_path))
