from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MyProdPage:    
    prod_cards = (By.CSS_SELECTOR, "div.sc-dkPtRN.jHqjxp ") 
    prod_title=(By.CSS_SELECTOR, "div.sc-hKwDye.izvDwJe")
    category=(By.XPATH, ".//div[contains(text(),'Categories')]")
    price=(By.XPATH, ".//div[contains(text(),'Price')]")
    rent=(By.XPATH, ".//div[contains(text(),'Rent')]")
    description=(By.XPATH, ".//div[contains(text(),'Description')]")
    date_posted=(By.XPATH, ".//div[contains(text(),'Date posted')]")   
    
    add_product_btn = (By.XPATH, "//button[text()='Add Product']")

    #Delete Elements
    del_icon = (By.CSS_SELECTOR, ".trash.icon")
    popup = (By.CSS_SELECTOR, ".ui.modal")
    cancel_btn = (By.XPATH, "//button[text()='Cancel']")
    yes_btn = (By.XPATH, "//button[text()='Yes, delete']")

    #Navbar elements link    
    browse_prod_link = (By.LINK_TEXT, "Browse Products")
    purchased_rent_link = (By.LINK_TEXT, "Bought/Sold/Borrowed/Lent List")
    account_settings_link = (By.LINK_TEXT, "Account Settings")

    #Logout Popup elements
    logout_link = (By.LINK_TEXT, "Logout")
    logout_popup_msg = (By.CSS_SELECTOR, ".ui.modal .description")    
    logout_cancel_btn = (By.XPATH, "//button[contains(text(),'Cancel')]")
    logout_confirm_btn = (By.XPATH, "//button[contains(text(),'Yes I am sure!')]")
    logout_modal = (By.CSS_SELECTOR, ".ui.modal")

    #Toast for create product
    toast = (By.CSS_SELECTOR, "[role='alert']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def is_loaded(self):
        return self.driver.find_element(*self.add_product_btn).is_displayed()
    
    def get_products(self):
        return self.wait.until(EC.presence_of_all_elements_located(self.prod_cards))
    
    def get_product_by_title(self, title):
        for p in self.get_products():
            prod_title = p.find_element(*self.prod_title).text
            if prod_title == title:
                return p
        return None

    def is_products_visible(self):
        return len(self.get_products()) > 0
      

    def click_first_product(self):
        products = self.get_products()

        if len(products) == 0:
            raise Exception("No products found!")

        self.wait.until(EC.element_to_be_clickable(products[0])).click()

    #Toast
    def get_toast_message(self):
        toast = self.wait.until(EC.visibility_of_element_located(self.toast))
        return toast.text.lower()

    #Add button click
    def click_add(self):
        self.wait.until(EC.element_to_be_clickable(self.add_product_btn)).click()

    #Delete product
    def delete_first(self):
        products = self.get_products()

        if not products:
            raise Exception("No products found")

        products[0].find_element(*self.del_icon).click()

        self.wait.until(EC.visibility_of_element_located(self.popup))

        self.wait.until(EC.element_to_be_clickable(self.yes_btn)).click()


    # LOGOUT Handling
    def click_logout(self):
        logout_btn = self.wait.until(EC.element_to_be_clickable(self.logout_link))
        logout_btn.click()   
    
    def get_popup_message(self):
        modal = self.wait.until(EC.visibility_of_element_located(self.logout_modal))
        return modal.find_element(*self.logout_popup_msg).text

    def confirm_logout(self):
        self.wait.until(EC.element_to_be_clickable(self.logout_confirm_btn)).click()

    def cancel_logout(self):
        self.wait.until(EC.element_to_be_clickable(self.logout_cancel_btn)).click()

    #Go to other pages links function:
    def go_to_account_settings(self):
        self.driver.find_element(*self.account_settings_link).click()
    def go_to_browse_product(self):
        self.driver.find_element(*self.browse_prod_link).click()
    def go_to_bought_rent_link(self):
        self.driver.find_element(*self.purchased_rent_link).click()
    
