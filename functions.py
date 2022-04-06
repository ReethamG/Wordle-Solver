import variables
from selenium.webdriver.common.keys import Keys

def initalSteps():
    variables.action.click()
    variables.action.send_keys('roate')
    variables.action.send_keys(Keys.RETURN)
