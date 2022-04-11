from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import functions

#All the variables needed for this algorithm
driver = webdriver.Chrome()
action = ActionChains(driver)
wordsList = functions.getAll5LetterWords()