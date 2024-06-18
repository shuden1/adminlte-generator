import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import threading
import json

# No file analysis is possible as the browsing tool doesn't support direct analysis of user-uploaded files not accessed via URL. 
# Therefore, assuming corrections based on common issues that could cause previous failures:

def main(html_file):
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Add this to prevent logging messages in the output
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_ file}")

    # Attempt to correct CSS selectors for job titles and URLs
    # Focusing on generic patterns that might have been missed
    jobs_elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='vacancy']")
    jobs = [{"Job-title": job_element.text, "URL": job_element.get_attribute("href")} for job_element in jobs_elements if job_element.text]

    driver.quit()
    return json.dumps(jobs, indent=2)

if __name__ == "__main__":
    html_file = sys.argv[1]
    print(main(html_file))