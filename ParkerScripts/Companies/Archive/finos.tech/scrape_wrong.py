from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import sys
import json

def scrape_job_listings(html_file):
    # Initialize a Chrome WebDriver
    driver = webdriver.Chrome()

    # Open the HTML file using the WebDriver
    driver.get(f"file://{html_file}")

    # Define the selectors for job titles and URLs based on BeautifulSoup analysis
    job_title_selector = 'p + p > a'

    # Find all job titles using the selector
    job_titles_elements = driver.find_elements(By.CSS_SELECTOR, job_title_selector)

    # Initialize a list to hold the job postings
    job_listings = []

    # Loop over each job title element and extract the text and the URL
    for job_title_element in job_titles_elements:
        title = job_title_element.text
        url = job_title_element.get_attribute('href')

        # Add the job listing to the list
        job_listings.append({"Job-title": title, "URL": url})

    # Close the WebDriver
    driver.quit()

    # Return the job listings as JSON
    return job_listings

# Entry point for the script
if __name__ == "__main__":
    # Get the target HTML file name from the command line argument
    target_html_file = sys.argv[1]

    # Call the function and print out the result in the required format
    job_listings = scrape_job_listings(target_html_file)
    print(json.dumps(job_listings))
