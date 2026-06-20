import pytest

from selenium import webdriver
from pageObjects.RegistrationPage import RegistrationPage
from pageObjects.LoginPage import LoginPage
from utilities.readProperties import ReadConfig
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Test_Add_User_01:
    baseURL = ReadConfig.getApplicationURL()   
    def test_Add_User(self,driver):   
        
        driver.get(self.baseURL)
        try:
            login_page = LoginPage(driver)
            login_page.click_sign_up()

            #New User Data
            user_data = {
                "first_name": "Nate",
                "last_name": "Mathew",
                "address": "House#123,Valley City, New York",
                "email": "nate@gmail.com",
                "phone": "0123456789",
                "password": "123456"
            }

            reg_page = RegistrationPage(driver)

            reg_page.set_first_name(user_data["first_name"])
            reg_page.set_last_name(user_data["last_name"])
            reg_page.set_address(user_data["address"])
            reg_page.set_email(user_data["email"])
            reg_page.set_phone(user_data["phone"])
            reg_page.set_password(user_data["password"])
            reg_page.set_confirm_password(user_data["password"])

            reg_page.click_register()           

            text = reg_page.get_toast_message()
            
            if "error" in text:
                driver.save_screenshot("Screenshots/register_failed.png")
                pytest.fail(f"Registration failed: {text}")
            assert "registered" in text 

        except Exception as e:
            driver.save_screenshot("Screenshots/user_register_failed.png")
            pytest.fail(f"Registration failed due to: {str(e)}")