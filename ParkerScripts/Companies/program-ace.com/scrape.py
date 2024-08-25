import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# The target HTML file name comes from an external source (console command as a single input parameter)
target_html_file = sys.argv[1]

# Initialise a headless webdriver
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Start the driver
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the local HTML file
driver.get(f"file:///{target_html_file}")

# Scrape all job listings using the defined selectors
job_listings = []
for job_element in driver.find_elements(By.CSS_SELECTOR, ".career-post-item .testimonial-single"):
    title = job_element.find_element(By.CSS_SELECTOR, ".testimonials-title").text
    url = job_element.get_attribute("href")  # Corrected variable name from job_panel to job_element
    job_listings.append({"Job-title": title, "URL": url})

# Print the JSON result
print(json.dumps(job_listings))

# Quit the driver
driver.quit()
