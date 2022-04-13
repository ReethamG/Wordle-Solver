from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import functions

driver = webdriver.Chrome()
action = ActionChains(driver)

wordsList = functions.getAll5LetterWords()

letterAndIndexForPresent = []
letterAndIndexForCorrect = []
absentLetters = []