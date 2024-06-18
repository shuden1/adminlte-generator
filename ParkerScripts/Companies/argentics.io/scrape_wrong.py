import sys
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

def main(html_file):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file}")

    jobs_list = []

    # The actual selectors need to be defined based on the analysis of the HTML structure
    job_opening_blocks_selector = '.job-opening-block'  # Placeholder for actual job opening block selector
    job_title_selector = '.job-title a'  # Placeholder for actual job title selector

    # Find all job opening blocks and extract titles and URLs
    job_opening_blocks = driver.find_elements(By.CSS_SELECTOR, job_opening_blocks_selector)
    
    for job_block in job_opening_blocks:
        job_titles = job_block.find_elements(By.CSS_SELECTOR, job_title_selector)
        for job_title in job_titles:
            title = job_title.text
            url = job_title.get_attribute('href')
            jobs_list.append({"Job-title": title, "URL": url})
    
    driver.quit()
    
    return jobs_list

if __name__ == "__main__":
    html_file_path = sys.argv[1]  # The HTML file path is expected to be the first argument
    jobs = main(html_file_path)
    print(jobs)