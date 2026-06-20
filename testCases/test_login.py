from selenium import webdriver
import pytest
from pageObjects.LoginPage import LoginPage
from pageObjects.MyProdPage import MyProdPage
from utilities.readProperties import ReadConfig
from selenium.webdriver.common.by import By


class Test_Login:
    baseURL = ReadConfig.getApplicationURL()
    email = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
   
    def test_login(self,driver):        
        try:
            driver.get(self.baseURL)
            login_page = LoginPage(driver)

            login_page.set_user_email(self.email)
            login_page.set_user_password(self.password)
            login_page.click_login()    
           
            my_prod_page = MyProdPage(driver)
            if not my_prod_page.is_loaded():
                pytest.fail("Product detail page not loaded")

        except Exception as e:
            driver.save_screenshot(".\\Screenshots\\test_login_failed.png")
            pytest.fail(f"Login test failed due to exception: {str(e)}") 

      
    