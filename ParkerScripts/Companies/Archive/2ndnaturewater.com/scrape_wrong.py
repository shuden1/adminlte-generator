from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import sys

# Define the selectors based on visual inspection of the HTML structure
job_listings_selector = '.fact-card-section'
job_title_selector = '.fact-card .fact-card-text-wrapper .fact-card-title'
job_link_selector = '.fact-card .fact-card-text-wrapper a'

# Get the HTML file path from the command line argument
html_file_path = sys.argv[1]

def extract_job_listings(driver, job_listings_selector, job_title_selector, job_link_selector):
    driver.get(f"file:///{html_file_path}")

    # Find job listings section
    job_listings_section = driver.find_element(By.CSS_SELECTOR, job_listings_selector)

    job_data = []
    job_cards = job_listings_section.find_elements(By.CSS_SELECTOR, '.fact-card')
    for job_card in job_cards:
        title_element = job_card.find_element(By.CSS_SELECTOR, job_title_selector)
        link_element = job_card.find_element(By.CSS_SELECTOR, job_link_selector)
        job_data.append({
            "Job-title": title_element.text,
            "URL": link_element.get_attribute("href")
        })

    return job_data

# Set up Chrome options for Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

# Set path to chromedriver as per your configuration
webdriver_service = Service(ChromeDriverManager().install())

# Set up driver
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

try:
    job_listings = extract_job_listings(driver, job_listings_selector, job_title_selector, job_link_selector)
    print(json.dumps(job_listings))
finally:
    driver.quit()
