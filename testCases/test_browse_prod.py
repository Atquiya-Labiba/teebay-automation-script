import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageObjects.MyProdPage import MyProdPage
from pageObjects.BrowseProdPage import BrowseProdPage
from pageObjects.ProdDetailPage import ProdDetailPage
import time

class Test_Browse_Prod:
    # READ 
    def test_browse_products(self, login_driver):        
        try:
            driver = login_driver
            dashboard = MyProdPage(driver)
            dashboard.go_to_browse_product()

            page = BrowseProdPage(driver) 
            time.sleep(2)        
            assert page.is_products_visible()
            assert len(page.get_products()) > 0

        except Exception as e:
            driver.save_screenshot(".\\Screenshots\\browse_prod_page_failed.png")
            pytest.fail(f"Browse products validation failed: {str(e)}")     

    def test_filter_title_cat(self, login_driver):       
        
        filter_data={
            "title":"Iphone 16",
            "category": "Electronics"
        }
        try:
            driver = login_driver
            dashboard = MyProdPage(driver)
            dashboard.go_to_browse_product()

            page = BrowseProdPage(driver)
            
            page.filter_by_title(filter_data["title"])
            page.filter_by_category(filter_data["category"])
            page.apply_filter()           

            
            products = page.get_all_product_det()            

            assert len(products) > 0, "No products found after filtering"

            for product in products:
                assert filter_data["category"].lower() in product["categories"].lower()

                
                assert filter_data["title"].lower() in product["title"].lower()
        
        except Exception as e:
            driver.save_screenshot(".\\Screenshots\\browse_prod_filter_failed.png")
            pytest.fail(f"Browse product filtering validation failed: {str(e)}")
    #Apply Filter
    def test_filter_buy(self, login_driver):        
        min_price=40
        max_price=500
        try:
            driver = login_driver
            dashboard = MyProdPage(driver)
            dashboard.go_to_browse_product()

            page = BrowseProdPage(driver)
            
            page.set_buy_filter(True,40,500)            
            page.apply_filter()

            
            products = page.get_all_product_det()

            assert len(products) > 0, "No products found after filtering"

            for product in products:
            # price validation
                price_text = product["price"]
                price = int(price_text.split("$")[1].strip())
                assert min_price <= price <= max_price
        
        except Exception as e:
            driver.save_screenshot(".\\Screenshots\\buy_filter_failed.png")
            pytest.fail(f"Browse product buy filtering validation failed: {str(e)}")

    def test_filter_rent(self, login_driver):        
        min_price=10
        max_price=50
        freq="Daily"
        try:
            driver = login_driver
            dashboard = MyProdPage(driver)
            dashboard.go_to_browse_product()

            page = BrowseProdPage(driver)
            
            page.set_rent_filter(True,min_price,max_price,freq)            
            page.apply_filter()

            
            products = page.get_all_product_det()

            assert len(products) > 0, "No products found after filtering"

            for product in products:
                rent_text = product["rent"].lower()

                rent_amount = int(rent_text.split("$")[1].split()[0])
                frequency = rent_text.split()[-1]
                assert min_price <= rent_amount <= max_price
                assert frequency == freq.lower()
        
        except Exception as e:
            driver.save_screenshot(".\\Screenshots\\buy_filter_failed.png")
            pytest.fail(f"Browse product buy filtering validation failed: {str(e)}")

    def test_clear_filter(self, login_driver):
        try:
            driver = login_driver
            dashboard = MyProdPage(driver)
            dashboard.go_to_browse_product()

            page = BrowseProdPage(driver)       
            
            default_products = page.get_all_product_det()  
            
            page.filter_by_title("Game")
            page.filter_by_category("Outdoor")
            page.set_buy_filter(True, 20, 50)
            page.apply_filter() 

            filtered_products = page.get_all_product_det()     

            assert len(filtered_products) <= len(default_products) 
            
            page.clear_filter()            
            
            time.sleep(1)             
            reset_products = page.get_all_product_det()            

            assert sorted(p["title"] for p in reset_products) == \
            sorted(p["title"] for p in default_products)
            assert len(reset_products) > 0

        except Exception as e:
            driver.save_screenshot("Screenshots/clear_filter_fail.png")
            pytest.fail(f"Clear filter test failed: {str(e)}")

 # Load More
    def test_load_more_prod(self,login_driver):
        try:
            driver = login_driver

            dashboard = MyProdPage(driver)
            dashboard.go_to_browse_product()

            page = BrowseProdPage(driver)         

            # initial state
            default_products = page.get_all_product_det()
            initial_count = len(default_products)
            
            page.click_load_more()

            # wait for UI update 
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(page.prod_cards))

            # after state
            new_products = page.get_all_product_det()
            new_count = len(new_products)

            assert new_count > initial_count, \
                f"Expected more products after Load More, but got {initial_count} -> {new_count}"
            
        except Exception as e:
            driver.save_screenshot("Screenshots/load_more.png")
            pytest.fail(f"Load more test failed: {str(e)}")
        
    # Open Product Detail Page
    def test_open_prod_detail_page(self, login_driver):        
        try:    
            driver = login_driver       
            dashboard = MyProdPage(driver)
            dashboard.go_to_browse_product() 

            browse_page=BrowseProdPage(driver)                          

            browse_page.click_first_product()

            prod_page = ProdDetailPage(driver)                        

            title_text=prod_page.is_loaded().text.lower()
            assert "detail" in title_text           
           
        except Exception as e:
            driver.save_screenshot(".\\Screenshots\\prod_det_page_failed.png")
            pytest.fail(f"Detail Product Page validation failed: {str(e)}")

    # View Count
    def test_view_count_increment(self, login_driver):        
        try: 
            driver = login_driver          
            dashboard = MyProdPage(driver)
            dashboard.go_to_browse_product() 

            browse_page=BrowseProdPage(driver)

            first_product = browse_page.get_all_product_det()[0]              
            title = first_product["title"].split("\n")[0]            
            initial_views = int(first_product["view_count"])

            browse_page.click_first_product()

            prod_page = ProdDetailPage(driver)                        

            assert prod_page.is_loaded()  

            detail_data = prod_page.get_product_det()

            assert detail_data["title"] == title
            detail_views = int(detail_data["views"])
            
            assert detail_views == initial_views + 1 

            driver.back()

            updated_product = browse_page.get_all_product_det()[0]
            updated_views = int(updated_product["view_count"])           

            assert updated_views == initial_views + 1        
           
        except Exception as e:
            driver.save_screenshot(".\\Screenshots\\prod_det_page_failed.png")
            pytest.fail(f"Detail Product Page validation failed: {str(e)}")
    
                

            


    
        

    
        