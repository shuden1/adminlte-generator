from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import sys

# The target HTML file name will be provided as a command line argument
file_name = sys.argv[1]

# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(options=options)

# Open local HTML file
driver.get(f"file:///{file_name}")

# Define the selectors based on observed HTML patterns
job_block_selector = ".mx-8.border-b.py-8.last\\:border-0"
job_title_selector = ".text-2xl.font-medium.text-berry-900"
apply_link_selector = ".flex.h-[40px].items-center.justify-center.rounded-[4px].px-4"

# Scrape job listings
job_data = []
job_blocks = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, job_block_selector))
)

for job_block in job_blocks:
    title = job_block.find_element(By.CSS_SELECTOR, job_title_selector).text.strip()
    link_element = WebDriverWait(job_block, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, apply_link_selector))
    )
    link = link_element.get_attribute('href').strip()
    job_data.append({'Job-title': title, 'URL': link})

# Output the results as JSON
print(json.dumps(job_data))

# Close the WebDriver
driver.quit()