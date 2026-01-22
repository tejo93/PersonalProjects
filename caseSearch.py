from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from tabulate import tabulate
import time


# Prompt user for input
case_number = input("Enter case number (e.g., G-100-12345-123456): ").strip()

# Setup your webdriver (chromedriver should be in your PATH)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Use the options when creating the driver
driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://flag.dol.gov/case-status-search")
    wait = WebDriverWait(driver, 15)

    # Input text in textarea
    # Input text in textarea as before
    textarea = wait.until(EC.visibility_of_element_located((By.ID, "cases-textarea")))
    textarea.clear()
    textarea.send_keys(case_number)

    # Click the button using the given XPath
    search_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[1]/form/section[4]/section/button'))
    )
    search_button.click()

    try:
    # Wait for the tbody to appear
        tbody = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/section/table/tbody'))
        )
        # Now find rows within this tbody
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        table_data = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            table_data.append([col.text for col in cols])
        # Get headers if needed
        thead = driver.find_element(By.XPATH, '//*[@id="root"]/div/section/table/thead')
        headers = [th.text for th in thead.find_elements(By.TAG_NAME, "th")]
        # Print the table
        print(tabulate(table_data, headers=headers, tablefmt="github"))
    except TimeoutException:
        print("No results found Please check the case number.")

finally:
    time.sleep(3) 
    driver.quit()