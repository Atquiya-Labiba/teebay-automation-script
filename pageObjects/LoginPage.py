from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    useremail = (By.NAME, "email")
    password = (By.NAME, "password")
    login_btn = (By.XPATH, "//button[contains(text(),'Sign In')]")
    sign_up_link = (By.CSS_SELECTOR, "a[href='/register']")   

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def set_user_email(self, email):
        email_field = self.wait.until(EC.visibility_of_element_located(self.useremail))
        email_field.clear()
        email_field.send_keys(email)

    def set_user_password(self, password):
        password_field = self.wait.until(EC.visibility_of_element_located(self.password))
        password_field.clear()
        password_field.send_keys(password)

    def login(self, email, password):
        self.set_user_email(email)
        self.set_user_password(password)
        self.click_login()

    def click_login(self):
        login_button = self.wait.until(EC.element_to_be_clickable(self.login_btn))
        login_button.click()


    def click_sign_up(self):
        self.driver.find_element(*self.sign_up_link).click()