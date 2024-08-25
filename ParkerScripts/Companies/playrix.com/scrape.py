from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import sys
import threading

# Retrieve the target HTML file name from the command line argument
target_html_file = sys.argv[1]

# Setup webdriver
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)
driver.get(target_html_file)

# Scrape job listings using the defined selectors
job_listings = []
jobs_cards = driver.find_elements(By.CSS_SELECTOR, ".jobs-card__section")
for card in jobs_cards:
    job_titles = card.find_elements(By.CSS_SELECTOR, ".jobs-card__name")
    job_links = card.find_elements(By.CSS_SELECTOR, "a.jobs-card__card")

    for title, link in zip(job_titles, job_links):
        job_listings.append({
            "Job-title": title.text,
            "URL": link.get_attribute("href")
        })

# Close the driver
driver.quit()

# Output the scraped data as JSON
print(json.dumps(job_listings))
