import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageObjects.MyProdPage import MyProdPage
from pageObjects.BrowseProdPage import BrowseProdPage
from pageObjects.ProdDetailPage import ProdDetailPage
import time

class Test_Prod_Det:    

    # Buy products
    def test_purchase_check(self,login_driver):
        try:
            driver = login_driver

            dashboard = MyProdPage(driver)
            dashboard.go_to_browse_product()

            browse_page = BrowseProdPage(driver)
            detail_page = ProdDetailPage(driver)
            
            browse_page.open_product_by_title("Blender")
            time.sleep(1)
            
            if not detail_page.is_loaded():
                pytest.fail("Product detail page not loaded")
            time.sleep(1)
            
            status = detail_page.get_status()
            if status != "available":
                pytest.fail(f"Product not available for purchase. Current status: {status}")
                
            if not detail_page.is_buy_visible():
                pytest.fail("Buy button not visible")                

            detail_page.click_buy()
            time.sleep(2)

            if not detail_page.wait_for_modal():
                pytest.fail("Buy confirmation popup not displayed")

            detail_page.confirm_buy()
            time.sleep(1)

            final_status = detail_page.get_status().lower()
            print("STAUS", final_status)

            if final_status != "sold":
                pytest.fail(f"Product status not updated. Status: '{final_status}'")                     
            
        except Exception as e:
            driver.save_screenshot(".\\Screenshots\\buy failed.png")
            pytest.fail(f"Product purchase failed: {str(e)}")

    def test_rent(self, login_driver):
        try:
            driver = login_driver

            dashboard = MyProdPage(driver)
            dashboard.go_to_browse_product()

            browse = BrowseProdPage(driver)
            detail = ProdDetailPage(driver)

            browse.open_product_by_title("Blender")

            if not detail.is_loaded():
                pytest.fail("Product detail page not loaded")

            status = detail.get_status()
            if status != "available":
                pytest.fail(f"Expected available but got {status}")

            if not detail.is_rent_visible():
                pytest.fail("Rent button not visible")
            
            detail.open_rent()
            
            detail.set_rent_dates("2026-06-01", "2026-06-10")
            
            detail.confirm_rent()
            time.sleep(2)
            
            history = detail.get_rent_history()

            if "Jul 1st 2026" not in history:
                pytest.fail("Start date not found in rent history")

            if "Jul 10th 2026" not in history:
                pytest.fail("End date not found in rent history")
                
        except Exception as e:
            driver.save_screenshot(".\\Screenshots\\rent_failed.png")
            pytest.fail(f"Rent failed due to: {str(e)}")

    


    
        