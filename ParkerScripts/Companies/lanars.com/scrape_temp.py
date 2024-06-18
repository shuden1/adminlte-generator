import sys
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# The filename should be an argument sent from an external source through the console command
html_file_name = sys.argv[1]

# Setting up the Chrome webdriver with specified options and profile path
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
service = Service(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initializing the webdriver
driver = webdriver.Chrome(service=service, options=options)

# Opening the target HTML file
driver.get("file:///" + html_file_name)

# Identifying job listings using the selectors from STEP 1
job_openings_blocks = driver.find_elements(By.CSS_SELECTOR, "div.LayoutContainer_container__SqT4a.PageCareersPositionsBrowse_vacanciesBlock__hAA7e")

# Extracting job titles and their URLs
jobs = []

# Assuming job titles and URLs are within <a> tags for simplicity in demonstration
for block in job_openings_blocks:
    job_links = block.find_elements(By.CSS_SELECTOR, "a")
    for link in job_links:
        job_title = link.text  # Assuming the job title is the text of the <a> tag
        job_url = link.get_attribute("href")
        jobs.append({"Job-title": job_title, "URL": job_url})

# Closing the driver
driver.quit()

# Printing the job listings as JSON
print(jobs)