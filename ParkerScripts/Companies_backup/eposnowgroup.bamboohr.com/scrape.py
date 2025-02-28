import json
import shutil
import sys
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as service
from selenium.webdriver.common.by import By

# The target HTML file name should be an argument sent from the external source through the console command
html_file = sys.argv[1]

# Initialize a headless webdriver with the specified profile folder path
profile_folder_path = (
    "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\"
    + str(threading.get_ident())
)
options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument(f"user-data-dir={profile_folder_path}")
service = service(executable_path=r"C:\Python3\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# Load the HTML file into the webdriver
driver.get(f"file://{html_file}")

# Use the EXACT selectors defined for job titles and URLs in STEP 1
selectors = {
    "job_list": "ul > div",
    "job_title": ".jss-f63",
    "job_url": "a",
}

# Scrape all job listings
jobs = []
job_blocks = driver.find_elements(By.CSS_SELECTOR, selectors["job_list"])
for job_block in job_blocks:
    title_element = job_block.find_element(By.CSS_SELECTOR, selectors["job_title"])
    url_element = job_block.find_element(By.CSS_SELECTOR, selectors["job_url"])
    jobs.append({
        "Job-title": title_element.text,
        "URL": url_element.get_attribute("href"),
    })

# Close the webdriver
driver.quit()

# Remove the folder profile_folder_path
shutil.rmtree(profile_folder_path)

# Return a JSON in the specified format
print(json.dumps(jobs))