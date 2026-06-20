import pytest
from selenium import webdriver
from pageObjects.AccSettingsPage import AccSettingsPage
from pageObjects.MyProdPage import MyProdPage
from utilities.readProperties import ReadConfig
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Test_Update_User:
    baseURL = ReadConfig.getApplicationURL()   
    def test_update_user(self,login_driver):       
               
        try: 
            driver = login_driver 
            my_prod_page = MyProdPage(driver)
            my_prod_page.go_to_account_settings()                      

            #Updated Data
            user_data = {
                "first_name": "Jack",
                "last_name": "John",
                "address": "House#14,Valley City, New York",
                "email": "jack13@gmail.com",
                "phone": "0123456789"                
            }
            
            acc_page = AccSettingsPage(driver)

            acc_page.set_first_name(user_data["first_name"])
            acc_page.set_last_name(user_data["last_name"])
            acc_page.set_address(user_data["address"])
            acc_page.set_email(user_data["email"])
            acc_page.set_phone(user_data["phone"])            

            acc_page.click_update()           

            text = acc_page.get_toast_message()
            
            if "error" in text:
                driver.save_screenshot("Screenshots/update_failed.png")
                pytest.fail(f"Account update failed: {text}")
            assert "updated" in text 

        except Exception as e:
            driver.save_screenshot("Screenshots/user_update_failed.png")
            pytest.fail(f"user Update failed due to: {str(e)}")