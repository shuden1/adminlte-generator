from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# STEP 2
def scrape_job_listings(html_file):
    # Set up the Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    # Open the local HTML file
    driver.get(f"file://{html_file}")

    # Scrape all job listings
    job_blocks = driver.find_elements(By.CSS_SELECTOR, "[class*='items-center bg-']")
    job_listings = []

    for job_block in job_blocks:
        title_element = job_block.find_element(By.CSS_SELECTOR, "[class*='font-semibold']:not([class*='text-right'])")
        url_element = job_block.find_element(By.CSS_SELECTOR, "[class*='text-right']")
        job_listings.append({
            "Job-title": title_element.text.strip(),
            "URL": url_element.get_attribute('href').strip()
        })

    driver.quit()

    # Return the results as JSON
    return json.dumps(job_listings)

if __name__ == "__main__":
    # Get the target HTML file name from the arguments
    if len(sys.argv) > 1:
        html_filename = sys.argv[1]
        print(scrape_job_listings(html_filename))