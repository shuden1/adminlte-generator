import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
import threading
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

# The target HTML file name is passed as a command-line argument
html_file_path = sys.argv[1]

# Setup and options for headless ChromeDriver
profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{str(threading.get_ident())}"
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the local HTML file
    driver.get(f"file:///{html_file_path}")

    # Correct the script to convert file:///D:/ URLs into valid HTTP URLs if necessary
    job_cards = driver.find_elements(By.CSS_SELECTOR, "div.featuredPositions_card__Wft_R")
    job_listings = []

    for card in job_cards:
        # Extract job title
        title_element = card.find_element(By.CSS_SELECTOR, ".featuredPositions_title__6h9QL")
        title = title_element.text
        # Extract and correct URL
        apply_button = card.find_element(By.CSS_SELECTOR, "a.featuredPositions_applyButton__YuXoU")
        url = apply_button.get_attribute('href')
        corrected_url = url.replace("file:///D:/", "http://example.com/")

        job_listings.append({"Job-title": title, "URL": corrected_url})

    # Format and print the job listings in JSON
    print(job_listings)
finally:
    # Quit the WebDriver
    driver.quit()
