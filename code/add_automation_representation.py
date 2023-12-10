import time
import TarsAutomation as ta
from TarsAutomation import driver, logger

def add(hotel_rid):
    ta.get('https://dataweb.accor.net/dotw-trans/displayHotelAutomation!input.action')
    ta.wait_for_element(element='automationTabs')
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
        ta.get_response(hotel_rid, code=item)

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
    ta.get_response(hotel_rid, code=item)

    logger.info(f'{hotel_rid} : ALL MANDATORY AUTOMATION SYSTEMS HAS BEEN ADDED')



