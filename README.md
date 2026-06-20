# Teebay Automation Framework

This is a **Automation Testing Framework** built using:
- Python
- Selenium WebDriver
- Pytest
- Page Object Model (POM)

It automates end-to-end test scenarios for the Teebay application including login, product CRUD, browsing,purchase and rent user flows.

## Test Case 
Test case file can be found from [View Test Cases](./TestCase_Report/)


## Installation & Setup
### Clone the repository
```bash
git clone https://github.com/Atquiya-Labiba/teebay-automation-script.git
cd teebay-automation-script
```

### Create virtual environment and activate it
python -m venv venv
venv\Scripts\activate

### Install dependencies
pip install -r requirements.txt

### Run all tests
pytest -v

### Run a specific test
pytest testCases/test_login.py -v


