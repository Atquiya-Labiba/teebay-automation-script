from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BrowseProdPage:
    load_more_btn = (By.XPATH, "//button[text()='Load More']")
    #Product card details
    prod_title=(By.CSS_SELECTOR, "div.sc-hKwDye")
    category=(By.XPATH, ".//div[contains(text(),'Categories')]")
    price=(By.XPATH, ".//div[contains(text(),'Price')]")
    rent=(By.XPATH, ".//div[contains(text(),'Rent')]")
    description=(By.XPATH, ".//div[contains(text(),'Description')]")
    date_posted=(By.XPATH, ".//div[contains(text(),'Date posted')]")
    
    prod_cards = (By.CSS_SELECTOR, "div.sc-efQSVx.dwHBiw ")

    filter_title=(By.NAME,"title") 
    cat_filter_dropdown=(By.CSS_SELECTOR, "div[name='category']")
    cat_opt=(By.CSS_SELECTOR, "div[name='category'] div[role='option'] span")   

    #Buy filter
    buy_filter=(By.XPATH, "//label[text()='Buy Filters']")
    buy_min_price=(By.NAME,"min_buy_range")
    buy_max_price=(By.NAME,"max_buy_range")
    #Rent filter
    rent_filter=(By.XPATH, "//label[text()='Rent Filters']")
    rent_min_price=(By.NAME,"min_rent_range")
    rent_max_price=(By.NAME,"max_rent_range")
    rent_freq=(By.NAME,"rent_duration_type")
    freq_opt_loc=(By.CSS_SELECTOR, "div[name='rent_duration_type'] .menu div[role='option']")

    #Clear button
    clear_btn = (By.XPATH, "//button[text()='Clear']")
    #Filter button
    filter_btn = (By.XPATH, "//button[text()='Filter']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5) 

    def get_products(self):
        return self.driver.find_elements(*self.prod_cards)

    def is_products_visible(self):
        return len(self.get_products()) > 0
    
    def product_exists(self, title):
        return self.get_product_by_title(title) is not None               
    
    def get_all_product_det(self):        
        products = []
        for p in self.get_products():                       
            products.append({
            "title": p.find_element(*self.prod_title).text.strip(),
            "categories": p.find_element(*self.category).text,
            "price": p.find_element(*self.price).text,
            "rent": p.find_element(*self.rent).text,
            "description": p.find_element(*self.description).text,
            "date_posted": p.find_element(*self.date_posted).text,
                "view_count": int(p.text.split("\n")[-1].split()[0])
            })

        return products 

    def get_product_by_title(self, title):

        for p in self.get_products():

            prod_title = p.find_element(*self.prod_title).text            

            if prod_title.strip().lower() == title.strip().lower():
                return p

        return None    
    
    def open_product_by_title(self, title):
        product = self.get_product_by_title(title)

        if not product:
            raise Exception(f"Product not found: {title}")

        self.wait.until(EC.element_to_be_clickable(product))
        product.click() 

    def click_first_product(self):
        products = self.get_products()

        if len(products) == 0:
            raise Exception("No products found!")

        self.wait.until(EC.element_to_be_clickable(products[0]))
        products[0].click()

    def filter_by_title(self, title):
        title_val = self.driver.find_element(*self.filter_title)
        title_val.clear()
        title_val.send_keys(title)

    def filter_by_category(self, category):
        # open dropdown
        self.driver.find_element(*self.cat_filter_dropdown).click()

        options = self.driver.find_elements(*self.cat_opt)

        for opt in options:
            if opt.text.strip() == category:
                opt.click()
                break

    def set_buy_filter(self, enable=True, min_price=None, max_price=None):
        buy_checkbox = self.wait.until(EC.element_to_be_clickable(self.buy_filter))
        if enable:
            buy_checkbox.click()

        if min_price is not None:
            min_elem = self.wait.until(EC.visibility_of_element_located(self.buy_min_price))
            min_elem.clear()
            min_elem.send_keys(min_price)

        if max_price is not None:
            max_elem = self.wait.until(EC.visibility_of_element_located(self.buy_max_price))
            max_elem.clear()
            max_elem.send_keys(max_price)

    def set_rent_filter(self, enable=True, min_price=None, max_price=None, rent_freq=None):        
        rent_checkbox = self.wait.until(EC.element_to_be_clickable(self.rent_filter) )
        if enable:
            rent_checkbox.click()

        if min_price is not None:
            min_elem = self.wait.until(EC.visibility_of_element_located(self.rent_min_price))
            min_elem.clear()
            min_elem.send_keys(min_price)

        # max price
        if max_price is not None:
            max_elem = self.wait.until(EC.visibility_of_element_located(self.rent_max_price))
            max_elem.clear()
            max_elem.send_keys(max_price)

        # frequency dropdown
        if rent_freq:
            self.wait.until( EC.element_to_be_clickable(self.rent_freq)).click()

            # wait for options
            options = self.wait.until( EC.visibility_of_all_elements_located(self.freq_opt_loc ) )

            # select matching option
            for opt in options:
                if opt.text.strip() == rent_freq:
                    opt.click()
                    break

    def apply_filter(self):
        self.driver.find_element(*self.filter_btn).click()

    def clear_filter(self):
        self.driver.find_element(*self.clear_btn).click()       

    def click_load_more(self):
        self.driver.find_element(*self.load_more_btn).click()  

    
    
