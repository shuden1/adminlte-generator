import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import shutil
import threading
import json

# Step 2: Use the correct CSS selectors based on BeautifulSoup analysis
job_block_selector = "div.row-fluid-wrapper.row-depth-1"
job_title_selector = "h2"
job_apply_button_selector = "a[href*='recruitment/vacancies']"

def scrape_jobs(html_file_name):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file://{html_file_name}")

    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    job_listings = []

    for job_block in job_blocks:
        title_elements = job_block.find_elements(By.CSS_SELECTOR, job_title_selector)
        apply_buttons = job_block.find_elements(By.CSS_SELECTOR, job_apply_button_selector)

        # Filter out non-job titles and pair with apply buttons
        for title_element, apply_button in zip(title_elements, apply_buttons):
            job_title = title_element.text.strip()
            job_url = apply_button.get_attribute('href').strip()

            # Exclude headers that are not job titles
            if "Job" not in job_title and job_title != "JOIN OUR TEAM" and job_title != "OUR LATEST":
                job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()


    return json.dumps(job_listings)

# The filename is the first command line argument
if __name__ == "__main__":
    html_file_name = sys.argv[1]
    print(scrape_jobs(html_file_name))
