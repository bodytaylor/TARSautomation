from selenium import webdriver

# Set the path to the Chrome WebDriver executable
chrome_driver_path = "TARSautomation\web_driver\chromedriver.exe"

# Create ChromeOptions object
chrome_options = webdriver.ChromeOptions()

# Pass the debuggerAddress and port along with host
chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")

# Create a ChromeDriver instance with ChromeOptions
driver = webdriver.Chrome(options=chrome_options)

# Now you can use the existing Chrome browser
driver.get("http://facebook.com")

# Perform actions on the webpage or continue with your test logic

# Close the browser window when you're done
driver.quit()
