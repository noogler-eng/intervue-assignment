from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
import time


# Setup Chrome options
options = Options()
options.add_argument("--start-maximized")
load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
LOGIN_URL = os.getenv("LOGIN_URL")

# Start browser
driver = webdriver.Chrome(service=Service(), options=options)

try:
    driver.get(LOGIN_URL)

    wait = WebDriverWait(driver, 30)

    # Step 1: Click on Login button (top-right)
    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Login']")))
    login_btn.click()

    driver.switch_to.window(driver.window_handles[-1])


    # time.sleep(1)
    # print("Looking for the close button...")
    # close_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//svg[@class='conversations-visitor-close-icon']")))
    # close_button.click()
    # print("Close button clicked.")


    login_button_1 = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "AccessAccount-ColoredButton-Text")))
    login_button_1.click()
    
    # Take screenshot for visual debugging
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    driver.save_screenshot("screenshots/debug_login_page.png")


    # Step 3: Enter email and password
    email_input = wait.until(EC.visibility_of_element_located((By.ID, "login_email")))
    password_input = driver.find_element(By.ID, "login_password")
    login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")


    email_input.send_keys(EMAIL)
    password_input.send_keys(PASSWORD)
    login_btn.click()
    time.sleep(2)  # Wait for page to load

    # here we have to add the search functionality 
    # Step 1: Click on the search placeholder to activate input field
    time.sleep(2)
    search_placeholder = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "search_placeholder")))
    search_placeholder.click()

    time.sleep(2)
    # Step 2: Now locate the input (usually appears after clicking)
    search_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "SearchBox__StyledInput-ctnsh0-4")))

# Step 3: Clear existing value and type new query (or re-type "hello")
    search_input.clear()
    search_input.send_keys("hello")
    time.sleep(2)


    search_result = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'style__Wrapper-pqpu-0')]//span[contains(text(), 'hello')]")))
    search_result.click()


    time.sleep(2)    

    # Step 4: Check if login succeeded by checking for profile/dropdown
    try:
        profile_dropdown_trigger = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-dropdown-link ProfileHeader__StyedDropdownHoverLink-sc-1gwp6c1-3 cwhrSp']//i[@class='anticon'])")))
        profile_dropdown_trigger.click()

        time.sleep(2);
        # Step 3: Locate and click the 'Logout' link inside the dropdown menu
        logout_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Logout']")))
        logout_link.click()
        print("Successfully logged out and redirected to login page.")
    except TimeoutException:
        print("Login failed. Taking screenshot.")
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        driver.save_screenshot("screenshots/login_failed.png")

finally:
    time.sleep(2)
    driver.quit()
