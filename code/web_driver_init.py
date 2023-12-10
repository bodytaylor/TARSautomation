from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import requests



ieOptions = webdriver.IeOptions()
ieOptions.add_additional_option("ie.edgechromium", True)
ieOptions.add_additional_option("ie.edgepath",'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
driver = webdriver.Ie(options=ieOptions)

def get_response_time(url):
    try:
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        response_time = end_time - start_time
        return response_time
    except requests.RequestException as e:
        return None, str(e)
    
a = get_response_time('https://dataweb.accor.net')
print(a)
def wait_for_element(element=str):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, 'element'))
        )
    time.sleep(0.15)
    
def login(username, password):
        # Navigate to the login page
    driver.get("https://dataweb.accor.net/dotw-trans/login!input.action")

    # Wait for an element to be visible
    try:
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "login"))
        )
            # Find the username and password input fields and enter your credentials
        username_field = driver.find_element(By.ID, "loginField")
        password_field = driver.find_element(By.NAME, "password")


        driver.execute_script("arguments[0].value = '';", username_field)
        username_field.send_keys(username)
        driver.execute_script("arguments[0].value = arguments[1];", password_field, password)

        # Submit the login form
        submit_button = driver.find_element(By.CSS_SELECTOR, 'input#login_0[value="Submit"].submit')

        # Click the button
        submit_button.click()
        password_field.send_keys(Keys.RETURN)
    except ValueError as e:
        print(e)

def response():
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="actionmessage"]/ul/li/span'))
        )
        span_element = element.find_element(By.XPATH, '//*[@id="actionmessage"]/ul/li/span')
        span_text = span_element.text
        return span_text
    except:
        return None
    
def hotel_search(hotel_rid):
    driver.get('https://dataweb.accor.net/dotw-trans/selectHotelInput.action')
    time.sleep(2)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="keyword"]'))
        )
        element = driver.find_element(By.XPATH, '//*[@id="keyword"]')
        element.clear()
        element.send_keys(f'{hotel_rid}')
        search_button = driver.find_element(By.ID, 'searchButton')
        count = 0
        
        while True:
            search_button.send_keys(Keys.RETURN)
            action_res = response()
            time.sleep(2)
            count += 1
            
            if action_res is None:
                hotel_name = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'hotelNameClass'))
            )
                hotel_name = driver.find_element(By.CLASS_NAME, 'hotelNameClass')
                text = hotel_name.text
                print(f'Selected Hotel: {text}')
                break
            elif count == 5:
                print('No Hotel Found!')
                break
            
    except ValueError as e:
        print(e)
    

