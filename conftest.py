import pytest
from selenium import webdriver
from pageObjects.LoginPage import LoginPage
from utilities.readProperties import ReadConfig

@pytest.fixture()

def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)

    yield driver

    driver.quit()

#Login fixture
@pytest.fixture()
def login_driver(driver):

    driver.get(ReadConfig.getApplicationURL())

    LoginPage(driver).login(ReadConfig.getUseremail(),ReadConfig.getPassword())

    return driver