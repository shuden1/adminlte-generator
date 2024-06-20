import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def main():
    # Get the HTML file name from the command line argument
    html_file = sys.argv[1]

    # Initialize the Chrome WebDriver in headless mode with the specified profile path
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    # Load the HTML file
    driver.get(f"file:///{html_file}")

    # Define the selectors for job blocks, titles, and URLs
    job_blocks_selector = 'div[class*="MuiGrid-root"]'
    job_title_selector = 'h6[class*="MuiTypography-root"] a'

    # Find job postings using the defined selectors
    job_postings = []
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
    for block in job_blocks:
        title_elements = block.find_elements(By.CSS_SELECTOR, job_title_selector)
        for title_element in title_elements:
            job_title = title_element.text.strip()
            job_url = title_element.get_attribute('href')
            job_postings.append({"Job-title": job_title, "URL": job_url})

    # Close the WebDriver
    driver.quit()

    # Return the job postings as JSON
    print(json.dumps(job_postings, indent=4))

if __name__ == "__main__":
    main()
