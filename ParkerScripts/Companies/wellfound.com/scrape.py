from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Step 1 Results
job_listing_container_selector = "div.styles_jobList__5MFDX"
job_listing_selector = "a.styles_component__UCLp3.styles_defaultLink__eZMqw.styles_anchor__aTiEC.styles_body__KvYlr"
job_title_selector = "h4.styles-module_component__3ZI84.styles-module_flow__FV70c.styles_jobTitle__01EmE"
job_url_attribute = "href"

# Step 2 Code
def scrape_job_listings(html_file):
    driver = webdriver.Chrome()
    driver.get(f"file:///{html_file}")
    
    job_listings = []
    for job_el in driver.find_elements(By.CSS_SELECTOR, job_listing_selector):
        job_title = job_el.find_element(By.CSS_SELECTOR, job_title_selector).text
        job_url = job_el.get_attribute(job_url_attribute)
        job_listings.append({"Job-title": job_title, "URL": job_url})
    
    driver.quit()
    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file = sys.argv[1]  # e.g., '/path/to/the/html_file.html'
    print(scrape_job_listings(html_file))