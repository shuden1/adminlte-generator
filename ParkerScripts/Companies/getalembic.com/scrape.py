from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Extract the filename from the command line argument
target_html = sys.argv[1]

# Start the main script
if __name__ == '__main__':
    # Set up the Chrome webdriver
    driver = webdriver.Chrome()

    # Open the target HTML file
    driver.get(f"file:///{target_html}")

    # Find job listings elements
    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div.elementor-widget-container')

    # Scrape job listings
    job_listings = []
    for job_block in job_blocks:
        job_links = job_block.find_elements(By.CSS_SELECTOR, 'a')
        for job_link in job_links:
            job_text = job_link.text
            job_url = job_link.get_attribute('href')
            if any(word in job_text for word in ["Senior", "Developer", "Engineer", "Specialist", "Manager", "Director"]):
                job_listings.append({"Job-title": job_text, "URL": job_url})

    # Serialize job listings to JSON
    job_listings_json = json.dumps(job_listings)

    # Print out the JSON - do not write to file
    print(job_listings_json)

    # Quit the driver
    driver.quit()