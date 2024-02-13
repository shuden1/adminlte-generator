from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import json

# Input file path from the command line argument
html_file_path = sys.argv[1]

# Define the CSS selectors based on the previous analysis
job_blocks_selector = ".media"
job_title_selector = ".media-body h5"
job_url_selector = ".media-body a"

# Start the Selenium script
def main():
    # Initialize Chrome WebDriver
    with webdriver.Chrome() as driver:
        driver.get(f"file://{html_file_path}")

        # Find all job listing elements
        job_elements = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
        jobs_list = []

        # Gather job titles and URLs
        for element in job_elements:
            title_element = element.find_element(By.CSS_SELECTOR, job_title_selector)
            url_element = element.find_element(By.CSS_SELECTOR, job_url_selector)
            job_title = title_element.text.strip()
            job_url = url_element.get_attribute('href')
            jobs_list.append({"Job-title": job_title, "URL": job_url})
        
        # Output the JSON result
        print(json.dumps(jobs_list))

if __name__ == "__main__":
    main()