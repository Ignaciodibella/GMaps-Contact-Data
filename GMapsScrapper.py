from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Configure Browser
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)  # Other versions use chrome_options instead of options
    return driver

# Extract Information
def extract_info_from_place_id(driver, place_id):
    url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
    driver.get(url)
    time.sleep(5)  # Adjust depending on internet conection

    info = {}
    
    try:
        # Place Name
        name_element = driver.find_element(By.XPATH, '//h1[contains(@class, "DUwDvf lfPIob") or contains(@class, "gm2-headline-5")]')
        info['name'] = name_element.text
    except:
        info['name'] = None

    try:
        # Phone Number
        phone_element = driver.find_element(By.XPATH, '//button[contains(@data-item-id, "phone:tel")]/div/div[2]/div[1]')
        info['phone'] = phone_element.text
    except:
        info['phone'] = None

    try:
        # Website
        website_element = driver.find_element(By.XPATH, '//a[@data-item-id="authority"]')
        info['website'] = website_element.get_attribute('href')
    except:
        info['website'] = None

    return info

# CSV with place_ids to process
places_id = pd.read_csv('places_id.csv')

final_data = pd.DataFrame(columns=['place_id', 'info'])

# Start scraping
driver = setup_driver()

rows = [{'place_id':place, 'info':extract_info_from_place_id(driver, place)} for place in places_id['Place Id']]
final_data = pd.concat([final_data, pd.DataFrame(rows)], ignore_index = True)

# Export to CSV
final_data.to_csv('places_with_contact_data.csv', index=False)

print("Data has been exported to output.csv")

driver.quit()
