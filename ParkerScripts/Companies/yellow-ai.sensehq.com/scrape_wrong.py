import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import shutil

# Get the target HTML file name from the command line argument
target_html_file_name = sys.argv[1]

profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--no-sandbox")
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")

driver = webdriver.Chrome(service=service, options=options)

# Access the local HTML file
driver.get(f"file://{target_html_file_name}")

# Wait for the elements to be present
wait = WebDriverWait(driver, 10)
job_listings = []

# Locate job listing elements
blocks = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.css-1tk7xz5")))

for block in blocks:
    try:
        title_element = block.find_element(By.CSS_SELECTOR, ".css-beqgbl .css-8qk9uv")
        button_element = block.find_element(By.CSS_SELECTOR, "div.css-1lnmtqu > div > div > a")
        title = title_element.text.strip()
        job_url = button_element.get_attribute('href')
        if not job_url:
            onclick_script = button_element.get_attribute('onclick')
            job_url = onclick_script.split("'")[1] if onclick_script and onclick_script.startswith("location.href=") else None
        job_listings.append({"Job-title": title, "URL": job_url})
    except Exception as e:
        continue

driver.quit()
# Clean up the profile directory
# shutil.rmtree(profile_folder_path, ignore_errors=True)

# Output the result
result_json = json.dumps(job_listings)
print(result_json)
