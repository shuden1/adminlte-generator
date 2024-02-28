import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

# Step 1 results (the selectors from BeautifulSoup)
job_block_selector = ".comp-lq20isp5-container"
job_title_selector = ".comp-lq20ispm4 h3.font_4"
job_url_selector = ".comp-lq20ispb a"

# Step 2: Selenium script
def scrape_jobs(html_file):
    # Initialize the Chrome Webdriver
    driver = webdriver.Chrome()

    try:
        # Open the local HTML file
        driver.get(f"file://{html_file}")

        # Find all job blocks
        job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
        jobs = []

        # Iterate over the job blocks and extract the title and URL
        for job_block in job_blocks:
            job_title_elem = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
            job_url_elem = job_block.find_element(By.CSS_SELECTOR, job_url_selector)
            job_title = job_title_elem.text.strip()
            job_url = job_url_elem.get_attribute('href').strip()
            if job_title and job_url:
                jobs.append({"Job-title": job_title, "URL": job_url})

        # Return the jobs in JSON format
        return json.dumps(jobs)
    finally:
        # Close the driver
        driver.quit()

if __name__ == "__main__":
    # The target HTML filename should be an argument sent from an external source
    html_filename = sys.argv[1]
    # Output the results
    print(scrape_jobs(html_filename))