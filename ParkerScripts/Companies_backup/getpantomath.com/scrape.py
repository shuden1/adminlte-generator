from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import json

# STEP 1: Identifying job listings selectors
job_listing_block_selector = "div.f-career__item.w-dyn-item"
job_title_selector = "div.f-blog__content-wr > div"
job_url_selector = "div.f-blog__content-wr > a"

# STEP 2: Create a Selenium script to scrape job listings
def scrape_job_listings(html_file):
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()

    # Open the local HTML file
    driver.get(f"file:///{html_file}")

    # Find job listing elements
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_listing_block_selector)

    # Extract job titles and URLs
    jobs = []
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        url_element = job_element.find_element(By.CSS_SELECTOR, job_url_selector)

        # Ensure that the job title is present
        if title_element.text:
            jobs.append({
                "Job-title": title_element.text,
                "URL": url_element.get_attribute('href'),
            })

    # Close the WebDriver
    driver.quit()

    # Return the jobs as JSON
    return json.dumps(jobs)

if __name__ == "__main__":
    target_html_file = sys.argv[1]
    print(scrape_job_listings(target_html_file))