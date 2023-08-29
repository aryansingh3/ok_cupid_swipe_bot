import time
import pickle
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.alert import Alert
import undetected_chromedriver as uc
from xpath_store import LOGIN_LINK_XPATH, EMAIL_FIELD_XPATH, PASSWORD_FIELD_XPATH, LOGIN_BUTTON_XPATH,SEND_CODE_BUTTON_XPATH
from credentials import email, password,like_probability,pass_probability,swipes
driver = uc.Chrome(use_subprocess=True)


# Initialize an undetected ChromeDriver
options = uc.ChromeOptions()
 # Run Chrome in headless mode (no GUI)
#options.add_argument('--disable-gpu')  # Disable GPU acceleration
 # Disable sandbox mode (Linux)
 # Disable /dev/shm usage (Linux)
 # Disable Chrome extensions
options.add_argument('--start-maximized')  # Maximize the browser window

# Create a ChromeService to specify driver settings
service = ChromeService(executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", enable_verbose_logging=True)

driver = uc.Chrome(options=options, service=service)


url = "https://www.okcupid.com/"  # Replace with the URL of the website you want to automate
#driver.get(url)
#time.sleep(10)

try:
    driver.get(url)
    with open('cookies.pkl', 'rb') as cookies_file:
        cookies = pickle.load(cookies_file)
        for cookie in cookies:
            driver.add_cookie(cookie)
except FileNotFoundError:
    # If cookies file doesn't exist, perform the login
    driver.get(url)

time.sleep(10)

# Locate and click on the login link (you'll need to inspect the webpage to find the correct element)
try:
    login_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, LOGIN_LINK_XPATH)))
    login_link.click()
except Exception as e:
    print("Login link not found or clickable:", str(e))

# Wait for the login page to load (adjust the time as needed)
try:
    email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, EMAIL_FIELD_XPATH)))
    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, PASSWORD_FIELD_XPATH)))
    email_field.send_keys(email)
    password_field.send_keys(password)
except Exception as e:
    print("Email or password field not found:", str(e))




try:
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, LOGIN_BUTTON_XPATH)))
    login_button.click()
except Exception as e:
    print("Login button not found or clickable:", str(e))

try:
    send_code_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, SEND_CODE_BUTTON_XPATH)))
    send_code_button.click()
except Exception as e:
    print("Send Code button not found or clickable:", str(e))


# Submit the login form (you may need to find the login button and click it)
try:
    WebDriverWait(driver, 10).until(EC.url_contains("https://www.okcupid.com/discover"))  # Replace with the URL of the logged-in page
except Exception as e:
    print("Login did not complete:", str(e))

with open('cookies.pkl', 'wb') as cookies_file:
    pickle.dump(driver.get_cookies(), cookies_file)






for _ in range(swipes):  # You can adjust the number of profiles to swipe
    try:
        # Randomly choose to "Like" or "Pass" based on probabilities
        action = random.choices(["like", "pass"], weights=[like_probability, pass_probability])[0]
        if action == "like":
            # Find the "Like" button by aria-label
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Like and view the next profile"]'))
            )
        else:
            # Find the "Pass" button by aria-label
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Pass and view the next profile"]'))
            )
        button.click()
    except Exception as e:
        print("Failed to click button:", str(e))

    # Add a random delay between 2 and 5 seconds
    random_delay = random.uniform(2, 5)
    time.sleep(random_delay)

# Wait for the login to complete (you may need to wait for a specific element on the logged-in page)



# Save the current session for next time
driver.quit()
