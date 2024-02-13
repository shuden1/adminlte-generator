from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import json

# Argument from the external source for the HTML filename
html_filename = sys.argv[1]

# Selenium script to scrape job listings and output JSON
def scrape_job_listings(html_filename):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options=options)
    driver.get(f"file:///{html_filename}")

    # Inspecting the provided HTML, the following selectors will extract job titles and URLs.
    # These selectors must be changed if they are not accurate.
    job_block_selector = 'div[id="grnhse_app"]'
    job_listing_selector = 'a'  # This is a speculative selector. It must be determined by inspecting the job listing block element.

    blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    job_listings = []

    for block in blocks:
        job_titles = block.find_elements(By.TAG_NAME, job_listing_selector)
        for title in job_titles:
            job_dict = {
                "Job-title": title.text.strip(),
                "URL": title.get_attribute('href')
            }
            job_listings.append(job_dict)

    driver.quit()

    # Ensuring unique job listings
    job_listings = [dict(t) for t in {tuple(d.items()) for d in job_listings}]
    
    # Output the final result
    return json.dumps(job_listings, indent=2)

# Call the function and print the result
print(scrape_job_listings(html_filename))