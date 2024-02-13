from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# The selectors from Step 1
job_container_selector = '.comp-lcp8476v'  # The div that wraps job listings
job_title_and_url_selector = 'a'           # The a tag that contains job title and url

def scrape_jobs(html_file_path):
    driver = webdriver.Chrome()
    driver.get(f"file:///{html_file_path}")

    # Find the job listings container
    job_containers = driver.find_elements(By.CSS_SELECTOR, job_container_selector)
    
    # Extract job titles and URLs
    jobs = []
    for container in job_containers:
        job_links = container.find_elements(By.CSS_SELECTOR, job_title_and_url_selector)
        for link in job_links:
            job_title = link.text.strip()
            job_url = link.get_attribute('href').strip()
            if job_title and job_url:
                jobs.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    return json.dumps(jobs)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(scrape_jobs(html_file_path))