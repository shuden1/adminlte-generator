import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By

def main():
    html_file_path = sys.argv[1]
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = webdriver.chrome.service.Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_path}")

    job_listings = []
    # Placeholder selectors, modify based on actual selectors from the HTML file's analysis
    elements = driver.find_elements(By.CSS_SELECTOR, "[INSERT_CSS_SELECTOR_FOR_JOB_LISTINGS_HERE]")
    for element in elements:
        title = element.find_element(By.CSS_SELECTOR, "[INSERT_CSS_SELECTOR_FOR_JOB_TITLE_HERE]").text
        url = element.find_element(By.CSS_SELECTOR, "[INSERT_CSS_SELECTOR_FOR_JOB_URL_HERE]").get_attribute('href')
        job_listings.append({"Job-title": title, "URL": url})

    driver.quit()

    print(json.dumps(job_listings))

if __name__ == "__main__":
    main()