import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def main():
    if len(sys.argv) != 2:
        print("Usage: script.py <html_file_path>")
        sys.exit(1)

    html_file_path = sys.argv[1]
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{html_file_path}")

    job_openings = driver.find_elements(By.CSS_SELECTOR, "div.openings-section-module--table-row--a9bb9")
    job_list = []

    for job in job_openings:
        title_element = job.find_element(By.CSS_SELECTOR, "a.bb-label.lg.bb-link.underline-always.openings-section-module--item-link--f0dd8.bold")
        title = title_element.get_attribute('innerHTML').strip()
        url = title_element.get_attribute('href') or "#"
        job_list.append({"Job-title": title, "URL": url})

    driver.quit()

    print(json.dumps(job_list, indent=4))

if __name__ == "__main__":
    main()