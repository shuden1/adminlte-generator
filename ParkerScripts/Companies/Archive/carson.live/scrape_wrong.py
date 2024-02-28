from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Step 2: Python + Selenium scraper script using corrected selectors from BeautifulSoup analysis
def scrape_job_listings(html_file):
    # Setup WebDriver
    driver = webdriver.Chrome()
    
    try:
        # Open the local HTML file
        driver.get(f"file://{html_file}")

        # Find job listings blocks with selector refined from BeautifulSoup analysis
        job_listings_blocks = driver.find_elements(By.CSS_SELECTOR, 'ul[aria-hidden="true"] li')

        # Scrape job titles and associated URLs
        jobs = []
        for job_block in job_listings_blocks:
            title_element = job_block.find_element(By.CSS_SELECTOR, 'a')
            job_title = title_element.text.strip()
            job_url = title_element.get_attribute('href')
            jobs.append({"Job-title": job_title, "URL": job_url})

        # Return job listings as JSON
        return json.dumps(jobs)

    finally:
        # Close the WebDriver
        driver.quit()

# Entry point of the script
if __name__ == "__main__":
    # Accept HTML file name from the external argument
    html_file_name = sys.argv[1]
    print(scrape_job_listings(html_file_name))