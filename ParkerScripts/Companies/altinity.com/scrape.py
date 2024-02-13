from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# The target HTML file name is an argument sent from an external source through the console command.
target_html_file = sys.argv[1]

driver = webdriver.Chrome()
driver.get(f"file://{target_html_file}")

# Use the selectors identified from BeautifulSoup analysis (Step 1)
# job_listings is the class for ul containing all the job blocks
# each li with class 'job_listing' is a block for a single job opening
# job title is within h3 tag inside the block
# the URL can be found in the 'href' attribute of the anchor (a) tag wrapping the job title

job_openings = driver.find_elements(By.CSS_SELECTOR, '.job_listings > .job_listing')
jobs_data = []

for job in job_openings:
    title_element = job.find_element(By.CSS_SELECTOR, 'h3')
    job_title = title_element.text
    job_url = job.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

    jobs_data.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Convert the list to JSON format
json_data = json.dumps(jobs_data)
print(json_data)