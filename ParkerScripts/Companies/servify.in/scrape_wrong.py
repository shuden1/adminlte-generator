import sys
import shutil
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

# The target HTML file name is an argument sent from an external source through the console command
target_html_file = sys.argv[1]

# Initialising a headless webdriver
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Open the target HTML file
driver.get(f"file:///{target_html_file}")

# Scrape all job listings using the selectors defined
job_listings = []

try:
    job_cards = driver.find_elements(By.CSS_SELECTOR, ".card .card-header")
    for job_card in job_cards:
        job_title_element = job_card.find_element(By.CSS_SELECTOR, "button")
        job_title = job_title_element.text
        job_url = "mailto:careers@servify.tech"
        if job_title:
            job_listings.append({"Job-title": job_title, "URL": job_url})
except NoSuchElementException:
    pass

# Output the job listings in JSON format
print(job_listings)

# Close the driver
driver.quit()

# Remove the folder profile_folder_path using # shutil.rmtree()
# shutil.rmtree(profile_folder_path, ignore_errors=True)
