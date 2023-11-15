from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


ieOptions = webdriver.IeOptions()
ieOptions.add_additional_option("ie.edgechromium", True)
ieOptions.add_additional_option("ie.edgepath",'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
driver = webdriver.Ie(options=ieOptions)

def login():
        # Navigate to the login page
    driver.get("https://dataweb.accor.net/dotw-trans/login!input.action")

    # Wait for an element to be visible
    try:
        username_field = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.NAME, "login"))
        )
            # Find the username and password input fields and enter your credentials
        username_field = driver.find_element(By.ID, "loginField")
        password_field = driver.find_element(By.NAME, "password")

        username = "NANSAN"
        password = "Welcome@2023"
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
        element = WebDriverWait(driver, 5).until(
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
                hotel_name = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'hotelNameClass'))
            )
                hotel_name = driver.find_element(By.CLASS_NAME, 'hotelNameClass')
                text = hotel_name.text
                print(f'Selected Hotel: {text}')
                break
            elif count == 5:
                print('No Hotel Found!')
                break
            else:
                print('No Hotel Found!')
                break
            
    except ValueError as e:
        print(e)
        
def add(hotel_rid):
    driver.get('https://dataweb.accor.net/dotw-trans/displayHotelAutomation!input.action')
    time.sleep(5)
    # ready to roll!!
    automation_list = ['RT', 'DQ', 'GG', 'HO', 'TE']

    for item in automation_list:
        # pass value to type
        add = 'addGDSElement();'
        code = f'var inputElement = document.getElementById("system.systemCode"); inputElement.value = "{item}";'
        search = 'searchGDS();'
        hrid = f'var inputElement = document.getElementById("externalCode"); inputElement.value = "{hotel_rid}";'
        save = 'addHotelGDS();'
        
        order = [add, code, search, hrid, save]
        for i in order:
            driver.execute_script(i)
            time.sleep(0.75)
    # for DHISCO
    add = 'addGDSElement();'
    code = 'var inputElement = document.getElementById("system.systemCode"); inputElement.value = "WB";'
    search = 'searchGDS();'
    insert = 'var inputElement = document.getElementById("associatedSystList"); inputElement.value = "WB";'
    hrid = f'var inputElement = document.getElementById("externalCode"); inputElement.value = "{hotel_rid}";'
    save = 'addHotelGDS();'

    order = [add, code, search, insert, hrid, save]
    for i in order:
        driver.execute_script(i)
        time.sleep(0.75)

    print(f'ALL MANDATORY AUTOMATION SYSTEMS HAS BEEN ADDED TO {hotel_rid}')


login()
time.sleep(5)
hotel_search('B682')
time.sleep(5)
add('B682')
time.sleep(5)



driver.quit()

