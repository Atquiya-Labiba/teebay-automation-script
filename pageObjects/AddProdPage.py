from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class AddProdPage:
    #Page Header
    page_header=(By.CSS_SELECTOR, "h1.ui.header")
    #Add Product button Locators
    add_product_btn = (By.XPATH, "//button[text()='Add Product']")

    #Form Locators
    prod_title=(By.NAME,"title")
    prod_categories=(By.NAME,"categories")
    prod_desc=(By.CSS_SELECTOR, "textarea[name='description']")
    prod_price=(By.NAME,"purchase_price")
    prod_rent_prc=(By.NAME,"rent_price")
    prod_rent_freq=(By.NAME,"rent_duration_type")

    ## Category dropdown locators
    cat_dropdown_loc=(By.CSS_SELECTOR, ".ui.multiple.selection.dropdown")
    cat_opt_loc = (By.CSS_SELECTOR,"[name='categories'] .menu div[role='option']")

    #Frequency dropdown Locators
    freq_opt_loc=(By.CSS_SELECTOR, "div[name='rent_duration_type'] .menu div[role='option']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def is_loaded(self):
        return self.wait.until(EC.visibility_of_element_located(self.page_header))

    def set_title(self, title):
        el = self.wait.until(EC.visibility_of_element_located(self.prod_title))        
        el.clear()
        time.sleep(2)
        el.send_keys(title)


    def set_description(self, desc):
        el = self.wait.until(EC.visibility_of_element_located(self.prod_desc))
        el.clear()
        el.send_keys(desc)


    def set_price(self, price):
        el = self.wait.until(EC.visibility_of_element_located(self.prod_price))        
        el.clear()
        el.send_keys(price)


    def set_rent_price(self, rent):
        el = self.wait.until(EC.visibility_of_element_located(self.prod_rent_prc))        
        el.clear()
        el.send_keys(rent)


    def select_frequency(self, freq):
        self.wait.until( EC.element_to_be_clickable(self.prod_rent_freq)).click()

        # wait for options
        options = self.wait.until( EC.visibility_of_all_elements_located(self.freq_opt_loc ) )

        # select matching option
        for opt in options:
            if opt.text.strip() == freq:
                opt.click()
                break


    def select_categories(self, values):
        self.wait.until( EC.element_to_be_clickable(self.cat_dropdown_loc) ).click()

        for value in values:

            options = self.wait.until(EC.presence_of_all_elements_located(self.cat_opt_loc))

            for opt in options:   

                if opt.text.strip() == value:                    
                    opt.click()
                    break
        self.driver.find_element(*self.prod_categories).send_keys(Keys.ESCAPE)
    

    def click_add_prod(self):        
            self.wait.until(EC.element_to_be_clickable(self.add_product_btn)).click()
        
    
