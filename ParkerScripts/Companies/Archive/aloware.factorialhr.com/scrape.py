from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import json

# Retrieve the target HTML file name from the argument sent via the console command
target_html_file = sys.argv[1]

# Start a new Chrome session
driver = webdriver.Chrome()
driver.get(f"file://{target_html_file}")

# Use BeautifulSoup selectors from STEP 1 to find job listings
job_offers = driver.find_elements(By.CSS_SELECTOR, '.job-offer-item')

# Scrape job titles and URLs
jobs_data = []
for offer in job_offers:
    title_element = offer.find_element(By.CSS_SELECTOR, '.factorial__headingFontFamily')
    url_element = offer.find_element(By.CSS_SELECTOR, 'a.buttonSecondary')
    
    job_title = title_element.text.strip()
    job_url = url_element.get_attribute('href').strip()
    
    jobs_data.append({"Job-title": job_title, "URL": job_url})

# Close the driver
driver.quit()

# Print the jobs data in JSON format
print(json.dumps(jobs_data))