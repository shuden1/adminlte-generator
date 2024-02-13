from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import json

# Step 2 Selenium script
def main(filename):
    # The function reads an HTML file and scrapes job titles and URLs.

    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    # Read the HTML content
    with open(filename, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Set up the driver with the HTML content
    driver.get("data:text/html;charset=utf-8," + html_content)

    # Scrape the job titles and URLs
    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'article.job')
    jobs_json = []

    for job_block in job_blocks:
        title_element = job_block.find_element(By.CSS_SELECTOR, 'h2')
        url_element = job_block.find_element(By.CSS_SELECTOR, 'a')
        jobs_json.append({"Job-title": title_element.text, "URL": url_element.get_attribute('href')})

    # Output the jobs in JSON format
    print(json.dumps(jobs_json))

    # Clean up the driver
    driver.quit()

if __name__ == "__main__":
    # The target HTML filename should be an argument sent from an external source through the console command
    html_filename = sys.argv[1]
    main(html_filename)