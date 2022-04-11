import variables
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def initalSteps(): 
    variables.action.click()
    variables.action.send_keys('roate')
    variables.action.send_keys(Keys.RETURN) 
    variables.action.perform()

def tileState(word, letter):
    root1 = variables.driver.find_element(By.CSS_SELECTOR, 'game-app')
    shadow_root1 = root1.shadow_root
    root2 = shadow_root1.find_element(By.CSS_SELECTOR, f"game-row[letters={word}]")
    shadow_root2 = root2.shadow_root
    root3 = shadow_root2.find_element(By.CSS_SELECTOR, f"game-tile[letter={letter}]")
    shadow_root3 = root3.shadow_root
    tile = shadow_root3.find_element(By.CSS_SELECTOR, ".tile")

    return str(tile.get_attribute('data-state'))

def tileRowStates(word):
    return [tileState(word, word[0]), tileState(word, word[1]), tileState(word, word[2]), tileState(word, word[3]), tileState(word, word[4])]

def getAll5LetterWords(): 
    my_file = open("wordleWords.txt", "r")
    data = my_file.read()
    data_into_list = data.split(",")
    my_file.close()

    return data_into_list
    
