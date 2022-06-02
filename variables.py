from configparser import DuplicateSectionError
# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.action_chains import ActionChains
import functions


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
action = ActionChains(driver)

wordsList = functions.getAll5LetterWords()

letterAndIndexForPresent = []
letterAndIndexForCorrect = []
absentLetters = []

