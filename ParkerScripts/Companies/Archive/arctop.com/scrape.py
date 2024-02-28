from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Fetch the target HTML file name from the argument sent from the external source
target_html_file_name = sys.argv[1]

# Set up the Chrome WebDriver
driver = webdriver.Chrome()

try:
    # Open the local HTML file in Chrome
    driver.get(f"file://{target_html_file_name}")

    # Define the selectors based on Step 1 analysis
    job_blocks_selector = "div.news-collection"
    job_titles_selector = "div.news-collection .w-dyn-item a"

    # Initialize an empty list to store job listings or news articles
    listings = []

    # Find all job listing or news article elements using the defined selectors
    elements = driver.find_elements(By.CSS_SELECTOR, job_titles_selector)

    # Extract job details and add to the list
    for element in elements:
        title = element.find_element(By.CSS_SELECTOR, 'h3').text
        url = element.get_attribute('href')
        listings.append({"Job-title": title, "URL": url})

    # Output the job listings or news articles as JSON
    print(json.dumps(listings))

finally:
    # Close the WebDriver
    driver.quit()