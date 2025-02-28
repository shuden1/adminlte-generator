import sys
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
import threading
from selenium.webdriver.common.by import By
import json

# The target HTML file name is passed as an argument from the external source
target_html_file = sys.argv[1]

# Initialise a headless webdriver
service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = ChromeOptions()
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep+str(threading.get_ident())
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = Chrome(service=service, options=options)

# Scrape all job listings using the selectors defined in STEP 1
driver.get(f"file:///{target_html_file}")
job_cards = driver.find_elements(By.CSS_SELECTOR, ".VacancyCard")
jobs_list = []

for card in job_cards:
    title_element = card.find_element(By.CSS_SELECTOR, ".VacancyCard-Title h3")
    title = title_element.text
    url = card.find_element(By.CSS_SELECTOR, ".VacancyCard-Link").get_attribute('href')
    jobs_list.append({"Job-title": title, "URL": url})

# Return JSON format
print(json.dumps(jobs_list))
