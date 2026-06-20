import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageObjects.MyProdPage import MyProdPage
from pageObjects.AddProdPage import AddProdPage
from pageObjects.EditProdPage import EditProdPage
import time

class Test_Crud_Prod:

    # CREATE 
    def test_create_product(self, login_driver):
        
        try:
            driver = login_driver
            my_prod_page = MyProdPage(driver)
            my_prod_page.click_add()

            add_page = AddProdPage(driver)
            if not add_page.is_loaded():
                pytest.fail("Add product page not loaded")
            prod_data = {
                "title": "Test Title",
                "categories": ["Electronics","Toys"],
                "description": "Test Description",
                "price": "600",
                "rent_price": "50",
                "freq": "Hourly"
            }
            add_page.set_title(prod_data["title"])
            add_page.set_description(prod_data["description"])
            add_page.set_price(prod_data["price"])
            add_page.set_rent_price(prod_data["rent_price"])
            add_page.select_categories(prod_data["categories"])
            add_page.select_frequency(prod_data["freq"])

            add_page.click_add_prod()
            toast_text = my_prod_page.get_toast_message()

            assert "added" in toast_text          

        except Exception as e:
            driver.save_screenshot(".\\Screenshots\\product_add_failed.png")
            pytest.fail(f"Produt add validation failed: {str(e)}")

    # READ 
    def test_read_products(self, login_driver):        
        try:
            driver = login_driver
            my_prod_page = MyProdPage(driver)         
            assert my_prod_page.is_products_visible()
            assert len(my_prod_page.get_products()) > 0
        except Exception as e:
            driver.save_screenshot(".\\Screenshots\\my_prod_page_failed.png")
            pytest.fail(f"Produt details validation failed: {str(e)}")     

    def test_open_edit_page(self, login_driver):
        
        try:
            driver = login_driver
            my_prod_page = MyProdPage(driver)
            my_prod_page.click_first_product()

            edit_prod_page=EditProdPage(driver)

            assert "edit" in edit_prod_page.is_loaded().text.lower()
        except Exception as e:
            driver.save_screenshot(".\\Screenshots\\edit_prod_page_failed.png")
            pytest.fail(f"Edit Product Page validation failed: {str(e)}")


    # UPDATE 
    def test_update_product(self, login_driver):        

        try:
            driver = login_driver
            my_prod_page = MyProdPage(driver)
            my_prod_page.click_first_product()

            edit_prod_page = EditProdPage(driver)
            update_data = {
                "title": "Updated Test Title",
                "categories": ["Electronics"],
                "description": "Edited Test Description",
                "price": "700",
                "rent_price": "250",
                "freq": "Weekly"
            }
            edit_prod_page.set_title(update_data["title"])
            edit_prod_page.set_description(update_data["description"])
            edit_prod_page.set_price(update_data["price"])
            edit_prod_page.set_rent_price(update_data["rent_price"])
            edit_prod_page.select_categories(update_data["categories"])
            edit_prod_page.select_frequency(update_data["freq"])

            edit_prod_page.click_edit()
            
            updated_product = my_prod_page.get_product_by_title(update_data["title"])
            assert updated_product is not None

            text = updated_product.text.lower()

            assert update_data["title"].lower() in text
            assert update_data["description"].lower() in text
            assert update_data["price"] in text
            assert update_data["rent_price"] in text
            assert update_data["freq"].lower() in text

            for cat in update_data["categories"]:
                assert cat.lower() in text

        except Exception as e:
            driver.save_screenshot(".\\Screenshots\\product_update_failed.png")
            pytest.fail(f"Produt update validation failed: {str(e)}")  
        

    # DELETE
    def test_delete_product(self, login_driver):        
        try:
            driver=login_driver
            my_prod_page = MyProdPage(driver)
            before_del = len(my_prod_page.get_products())

            my_prod_page.delete_first()

            after = len(my_prod_page.get_products())

            assert after == before_del - 1
        except Exception as e:
            driver.save_screenshot(".\\Screenshots\\product_delete_failed.png")
            pytest.fail(f"Produt delete validation failed: {str(e)}")
        