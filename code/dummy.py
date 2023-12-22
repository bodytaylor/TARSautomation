import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
# Create a session
session = requests.Session()

url_login = 'https://myaccor.service-now.com/login.do'
username = 'nantawat.sangkarn@accor.com'
password = 'Ink295*968KK'

# Login to ServiceNow
login_payload = {
    'user': username,
    'password': password,
    'sysparm_login': 'Log in',
}

login_response = session.post(url_login, data=login_payload)

# Check if login was successful (you might need to inspect the response content or status code)
if login_response.ok:
    print("Login successful!")
    # Now you can make requests with the authenticated session

    # Example: Get data from a ServiceNow page
    url_target = 'https://myaccor.service-now.com/sys_report_display.do?sysparm_report_id=33d66650871f7d9c97d7b9d09bbb35c8'
    response = session.get(url_target)

    if response.ok:
        print("Request successful!")
    else:
        print(f"Failed to retrieve the target webpage. Status code: {response.status_code}")
else:
    print(f"Login failed. Status code: {login_response.status_code}")
    
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')
report_content_element = soup.find('div', class_='report_content list_report_content')
report = report_content_element.text.strip()

print(report)