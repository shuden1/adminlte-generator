from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import sys
import json

# STEP 1 OUTPUT: SELECTORS (based on analysis)
job_block_selector = 'div.alcm-clickable.slot-container'
job_title_selector = 'p.alcm-text'
# Since no URL is directly associated, using JavaScript to click the job block.
job_link_selector = 'a'  # This is a placeholder since JavaScript click will be used.

# STEP 2: SELENIUM SCRIPT
if len(sys.argv) > 1:
    target_html_file = sys.argv[1]
    
    # Initialize WebDriver
    service = Service()
    driver = webdriver.Chrome(service=service)

    # Open the local HTML file
    driver.get(f"file://{target_html_file}")
    
    # Find all job listing blocks
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    
    # Process job listings
    job_listings = []
    for job_block in job_blocks:
        job_title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = job_title_element.get_attribute('textContent').strip()

        # Since URLs are not provided, simulate a click and get the resulting URL
        # Note: Depending on the webpage, this might navigate away or open a new tab/window.
        # This should be adjusted based on the actual behavior of the job blocks.
        original_window = driver.current_window_handle
        job_block.click()  # Simulate a click on the job block
        new_window_handles = [handle for handle in driver.window_handles if handle != original_window]
        job_url = driver.current_url  # Current URL after click
        if new_window_handles:
            driver.switch_to.window(new_window_handles[0])
            job_url = driver.current_url
            driver.close()
            driver.switch_to.window(original_window)

        job_listings.append({"Job-title": job_title, "URL": job_url})
    
    driver.quit()
    
    # Output result as JSON
    print(json.dumps(job_listings))