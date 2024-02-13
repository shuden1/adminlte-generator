import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys

# Set up the Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument("--disable-extensions")
options.add_argument("--disable-dev-shm-usage")

# Script to scrape the job openings
def scrape_job_openings(file_path):
    # Initialize the driver
    driver = webdriver.Chrome(options=options)
    jobs = []
    
    try:
        # Open the local HTML file
        driver.get(f"file:///{file_path}")
        
        # Selectors based on the structure of the HTML content
        openings_selector = '.career-collection-item.w-dyn-item'
        title_selector = '.carrer-title'
        link_selector = 'a.career-item.w-inline-block'
        
        # Find job openings blocks
        openings = driver.find_elements(By.CSS_SELECTOR, openings_selector)
        
        # Iterate over job openings to extract titles and URLs
        for opening in openings:
            title_element = opening.find_element(By.CSS_SELECTOR, title_selector)
            link_element = opening.find_element(By.CSS_SELECTOR, link_selector)
            
            # Extract text and href attributes
            title = title_element.text.strip()
            link = link_element.get_attribute('href').strip()
            
            # Ignore list items without titles
            if title:
                job = {'Job-title': title, 'URL': link}
                jobs.append(job)
        
        return json.dumps(jobs)
    
    finally:
        # Quit the driver session gracefully
        driver.quit()

if __name__ == '__main__':
    # Accept the HTML file as a command line argument
    html_file_path = sys.argv[1]
    scraped_jobs = scrape_job_openings(html_file_path)
    print(scraped_jobs)