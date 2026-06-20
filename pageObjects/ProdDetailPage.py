from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageObjects.MyProdPage import MyProdPage
from pageObjects.BrowseProdPage import BrowseProdPage


class ProdDetailPage:
    #Page Header
    page_header=(By.CSS_SELECTOR, "h1.ui.header")  

    product_title = (By.CSS_SELECTOR, "div.sc-bBHHxi.haGHWM")
    views = (By.XPATH, "//div[contains(text(),'Views')]")
    categories = (By.XPATH, "//div[contains(text(),'Categories')]")
    status = (By.CSS_SELECTOR, "div.sc-khQegj.eeziuM div.ui.label")
    price = (By.XPATH, "//div[contains(text(),'Purchase Price')]")    
    rent_history = (By.XPATH, "//div[contains(text(),'Rent history')]")
    description = (By.CSS_SELECTOR, "div.sc-eJwWfJ") 

    #Buttons
    buy_btn=(By.XPATH, "//button[text()='Buy']")
    rent_btn=(By.XPATH, "//button[text()='Rent']")

    #Popup elements
    yes_btn = (By.XPATH, "//button[text()='Yes!']")
    cancel_button = (By.XPATH, "//button[text()='Cancel']")
    modal = (By.CSS_SELECTOR, "div.ui.modal") 

    start_date_input = (By.NAME, "start_date")
    end_date_input = (By.NAME, "end_date")

    book_rent_btn = (By.XPATH, "//button[text()='Book rent']")  

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def is_loaded(self):
        return self.wait.until(EC.visibility_of_element_located(self.page_header))   
            
    
    def get_product_det(self):
        price_text = self.driver.find_element(*self.price).text

        purchase = price_text.split("|")[0].strip()
        rent = price_text.split("|")[1].strip()

        purchase_amount = int(purchase.split("$")[1].split()[0])

        rent_amount = int(rent.split("$")[1].split()[0])
        rent_freq = rent.split()[-1].lower()

        views_text=self.driver.find_element(*self.views).text.strip()
        view_count=int(views_text.split(":")[1].strip())

        return {
            "title": self.driver.find_element(*self.product_title).text.strip(),
            "views": view_count,
            "categories": self.driver.find_element(*self.categories).text.strip(),
            "status": self.status,
            "purchase_amount": purchase_amount,
            "rent_amount": rent_amount,
            "rent_freq": rent_freq,
            "rent_history": self.driver.find_element(*self.rent_history).text.strip(),
            "description": self.driver.find_element(*self.description).text.strip(),
    }

    def get_status(self):
        return self.driver.find_element(*self.status).text.strip().lower()

    def wait_for_modal(self):
        return self.wait.until(EC.visibility_of_element_located(self.modal))
    
    def is_buy_visible(self):
        elems = self.driver.find_elements(*self.buy_btn)
        return len(elems) > 0 and elems[0].is_displayed()

    def is_rent_visible(self):
        elems = self.driver.find_elements(*self.rent_btn)
        return len(elems) > 0 and elems[0].is_displayed()

    def click_buy(self):
        self.wait.until(EC.element_to_be_clickable(self.buy_btn)).click()
        self.wait_for_modal()

    def confirm_buy(self):
        self.wait_for_modal()
        self.wait.until(EC.element_to_be_clickable(self.yes_btn)).click()

    def cancel_buy(self):
        self.wait_for_modal()
        self.wait.until(EC.element_to_be_clickable(self.cancel_button)).click()

    def open_rent(self):
        self.wait.until(EC.element_to_be_clickable(self.rent_btn)).click()
        self.wait_for_modal()

    def set_rent_dates(self, start_date, end_date):
        start = self.wait.until(EC.visibility_of_element_located(self.start_date_input))
        start.clear()
        start.send_keys(start_date)

        end = self.driver.find_element(*self.end_date_input)
        end.clear()
        end.send_keys(end_date)

    def confirm_rent(self):
        self.wait.until(EC.element_to_be_clickable(self.book_rent_btn)).click()

    def get_rent_history(self):
        return self.driver.find_element(*self.rent_history).text.strip()
   
    

   
    
