from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

def scrape_job_listings(html_file_path):
    # Initialize the Chrome driver
    driver = webdriver.Chrome()
    # Open the HTML file in the browser
    driver.get(f"file://{html_file_path}")

    # Selectors based on the given HTML file structure
    job_blocks_selector = ".job-item.w-dyn-item"
    job_title_selector = "h5._20-27.left"
    job_url_selector = "a.button-navigation.jobs.w-button"

    # Find all job blocks
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
    
    # List to hold the job data
    job_listings = []

    # Extract job title and URL from each job block
    for job_block in job_blocks:
        job_title = job_block.find_element(By.CSS_SELECTOR, job_title_selector).text.strip()
        job_url = job_block.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute('href').strip()
        job_listings.append({"Job-title": job_title, "URL": job_url})

    # The driver is no longer needed at this point
    driver.quit()

    # Return the job data as a JSON string
    return json.dumps(job_listings)

# The main entry point for the script
if __name__ == "__main__":
    # The script expects a single command-line argument which is the file name of the HTML file
    filename = sys.argv[1]
    # Print out the job data in JSON format
    print(scrape_job_listings(filename))