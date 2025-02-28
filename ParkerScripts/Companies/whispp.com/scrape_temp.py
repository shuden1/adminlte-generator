STEP 2: Create a Python + Selenium script using the latest best practices for ChromeDriver 120.0.6099.109.
            1. This script will be launched externally in a settled-up environment, DO NOT TEST THIS SCRIPT, CREATE IT:
            THE TARGET HTML FILE NAME SHOULD BE AN ARGUMENT SENT FROM AN EXTERNAL SOURCE THROUGH THE CONSOLE COMMAND AS THE SINGLE INPUT PARAMETER. DO NOT PUT ANY PLACEHOLDERS OR EXAMPLES!
            2. Initialise a headless webdriver, with this profile path, do not forget to create a relevant folder: profile_folder_path="D:\Mind\CRA\AI_Experiments\Job_Crawlers\Peter\adminlte-generator\chrome_profile\"+str(threading.get_ident()) use this service:
            service=service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"") add these options: options.add_argument(f"user-data-dir={profile_folder_path}") options.add_argument("--headless") options.add_argument("--disable-gpu") options.add_argument("--no-sandbox")
            3. USE THE SELECTORS DEFINED IN STEP 1!!! and scrape all job listings. REMEMBER!!!! instead of an old find_elements_by_css_selector, you should use the find_elements method with By.CSS_SELECTOR
            4. NEVER IMPLEMENT EXAMPLE USAGE PARAMETERS AND SELECTORS
            5. Return a JSON with all job postings in the following format, DO NOT WRITE RESULT TO ANY FILE: { ["Job-title" :"title1", "URL":"url1"], ["Job-title" :"title2", "URL":"url2"], }
