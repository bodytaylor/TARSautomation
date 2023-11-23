import time
from web_driver_init import driver

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



