from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

def scrape_job_listings(html_file):
    driver = webdriver.Chrome()
    
    try:
        driver.get(f"file:///{html_file}")
        
        # Selector for job title blocks
        job_title_block_selector = ".elementor-element.elementor-element-e4ebc7c .elementor-widget-wrap"
        # Selector for job titles and URLs
        job_title_selector = ".elementor-heading-title.elementor-size-default a"
        
        # Get all job listing blocks
        job_title_blocks = driver.find_elements(By.CSS_SELECTOR, job_title_block_selector)
        
        # List to hold all jobs
        jobs = []
        for block in job_title_blocks:
            # Find job titles within the blocks
            job_titles = block.find_elements(By.CSS_SELECTOR, job_title_selector)
            for job_title in job_titles:
                title_text = job_title.text
                title_url = job_title.get_attribute('href')
                if title_text and title_url:
                    job_data = {"Job-title": title_text, "URL": title_url}
                    jobs.append(job_data)
        
        # Convert to JSON and print
        jobs_json = json.dumps(jobs)
        print(jobs_json)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    html_file = sys.argv[1]
    scrape_job_listings(html_file)