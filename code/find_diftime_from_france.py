from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def find_time(city):
    destination_country = city
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.zeitverschiebung.net/en/country/fr')

    # fill a from
    input_country = driver.find_element(By.ID, 'diff_second')
    time.sleep(2)
    input_country.send_keys(destination_country)
    time.sleep(2)
    input_country.send_keys(Keys.ENTER)
    result = driver.find_element(By.XPATH, '/html/body/div[1]/section[1]/div/div/div[2]/div')
    result_text = result.text
    return result_text