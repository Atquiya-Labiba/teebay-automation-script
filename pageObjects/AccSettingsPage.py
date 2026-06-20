from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AccSettingsPage:
    first_name = (By.NAME, "first_name")
    last_name = (By.NAME, "last_name")
    address = (By.NAME, "address")
    email = (By.NAME, "email")
    phone = (By.NAME, "phone_number") 
    toast_message = (By.CSS_SELECTOR, "[role='alert']")   

    update_btn = (By.XPATH, "//button[text()='Update']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def set_first_name(self, fname):
        f_name = self.wait.until(EC.visibility_of_element_located(self.first_name))
        f_name.clear()
        f_name.send_keys(fname)

    def set_last_name(self, lname):
        l_name = self.wait.until(EC.visibility_of_element_located(self.last_name))
        l_name.clear()
        l_name.send_keys(lname)

    def set_address(self, address):
        addr = self.wait.until(EC.visibility_of_element_located(self.address))
        addr.clear()
        addr.send_keys(address)

    def set_email(self, email):
        email_addr = self.wait.until(EC.visibility_of_element_located(self.email))
        email_addr.clear()
        email_addr.send_keys(email)

    def set_phone(self, phone):
        phn = self.wait.until(EC.visibility_of_element_located(self.phone))
        phn.clear()
        phn.send_keys(phone)

    def set_password(self, password):
        passw = self.wait.until(EC.visibility_of_element_located(self.password))
        passw.clear()
        passw.send_keys(password)  

    def get_toast_message(self):
        toast = self.wait.until(EC.visibility_of_element_located(self.toast_message))
        return toast.text.lower() 

    def click_update(self):
        self.wait.until(EC.element_to_be_clickable(self.update_btn)).click()
