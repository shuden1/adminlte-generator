from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# The target HTML file name is taken from the console command as a parameter
html_file_path = sys.argv[1]
driver = webdriver.Chrome()

try:
    driver.get(f"file://{html_file_path}")

    # Selectors as identified after analyzing the HTML structure
    jobs_selector = "#current-openings .e-con-inner .elementor-widget-container a"
    
    # Find job listings
    job_elements = driver.find_elements(By.CSS_SELECTOR, jobs_selector)
    jobs = [{"Job-title": job_element.text.strip(), "URL": job_element.get_attribute('href')} for job_element in job_elements]

finally:
    driver.quit()

# Output the jobs list in JSON format
print(json.dumps(jobs))