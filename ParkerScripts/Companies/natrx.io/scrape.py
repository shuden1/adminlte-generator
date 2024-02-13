import sys
import json
from selenium import webdriver
from selenium.webdriver.common.by import By

# Selectors based on Step 1 analysis
job_listing_selector = "section.post.type-post.status-publish"
job_title_selector = "h2 a"
job_url_selector = "h2 a"

def scrap_job_listings(html_file):
    # Set up the Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    
    with webdriver.Chrome(options=options) as driver:
        # Load the HTML file
        driver.get(f"file:///{html_file}")

        # Find all job openings
        jobs_data = []
        job_listings = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)

        # Extract job title and URL from each job listing
        for job in job_listings:
            title = job.find_element(By.CSS_SELECTOR, job_title_selector).text.strip()
            url = job.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute('href').strip()
            jobs_data.append({"Job-title": title, "URL": url})

        return jobs_data

# Entry point for the script
if __name__ == "__main__":
    # The target HTML file name should be provided as a command-line argument
    html_file = sys.argv[1]
    job_listings = scrap_job_listings(html_file)
    print(json.dumps(job_listings))