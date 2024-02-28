import json
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape_job_openings(html_file):
    driver = webdriver.Chrome()
    jobs = []
    
    try:
        driver.get(f"file://{html_file}")
        job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div.css-18r3913')
        
        for job_block in job_blocks:
            job_titles = job_block.find_elements(By.CSS_SELECTOR, 'h4.css-1nnkt6y')
            job_links = job_block.find_elements(By.CSS_SELECTOR, 'a.css-g65o95')

            for title, link in zip(job_titles, job_links):
                jobs.append({
                    "Job-title": title.text,
                    "URL": link.get_attribute('href')
                })
    finally:
        driver.quit()

    return json.dumps(jobs)

if __name__ == "__main__":
    html_file = sys.argv[1]
    print(scrape_job_openings(html_file))