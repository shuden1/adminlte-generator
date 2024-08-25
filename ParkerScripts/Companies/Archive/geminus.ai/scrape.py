from bs4 import BeautifulSoup
import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
import json

# Step 1
job_listing_selector = ".jet-listing-grid__item"
job_title_selector = ".elementor-widget-theme-post-title"
job_url_selector = ".elementor-widget-theme-post-title a"

# Step 2
def main(html_file):
    # Setup Driver
    driver = webdriver.Chrome()
    driver.get(f"file://{html_file}")

    # Parse the HTML content
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find job listing elements
    job_listings = soup.select(job_listing_selector)

    # Extract job titles and URLs
    jobs_data = []
    for job in job_listings:
        title_element = job.select_one(job_title_selector)
        url_element = title_element.select_one(job_url_selector) if title_element else None
        title = title_element.get_text(strip=True) if title_element else ""
        url = url_element['href'] if url_element and url_element.has_attr('href') else ""
        jobs_data.append({"Job-title": title, "URL": url})

    driver.quit()

    # Return jobs data as JSON
    return json.dumps(jobs_data)

if __name__ == "__main__":
    html_file = sys.argv[1]
    print(main(html_file))
