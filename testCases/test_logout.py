from selenium import webdriver
import pytest
from pageObjects.LoginPage import LoginPage
from pageObjects.MyProdPage import MyProdPage
from utilities.readProperties import ReadConfig
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class Test_Logout:   
   
    def test_logout(self,login_driver):        
        
        try:
            driver = login_driver            
            my_prod_page = MyProdPage(driver)
            if not my_prod_page.is_loaded():
                pytest.fail("Product detail page not loaded")

            my_prod_page.click_logout()
            message=my_prod_page.get_popup_message().lower()
            assert "log out" in message
            my_prod_page.confirm_logout()            

        except Exception as e:
            driver.save_screenshot(".\\Screenshots\\test_login_failed.png")
            pytest.fail(f"Login test failed due to exception: {str(e)}")   
    