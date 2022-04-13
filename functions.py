import variables
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import functions
import time
import random

def initalSteps(): 
    variables.action.click()
    variables.action.send_keys('roate')
    variables.action.send_keys(Keys.RETURN) 
    variables.action.perform()
    time.sleep(5)

def typeInWord(word):
    variables.action.send_keys(f'{word}')
    variables.action.send_keys(Keys.RETURN)
    variables.action.perform()
    time.sleep(5)

def tileStateWithLetter(word, letter):
    root1 = variables.driver.find_element(By.CSS_SELECTOR, 'game-app')
    shadow_root1 = root1.shadow_root
    root2 = shadow_root1.find_element(By.CSS_SELECTOR, f"game-row[letters={word}]")
    shadow_root2 = root2.shadow_root
    root3 = shadow_root2.find_element(By.CSS_SELECTOR, f"game-tile[letter={letter}]")
    shadow_root3 = root3.shadow_root
    tile = shadow_root3.find_element(By.CSS_SELECTOR, ".tile")

    return [letter, tile.get_attribute("data-state")]

def tileState(word, letter):
    root1 = variables.driver.find_element(By.CSS_SELECTOR, 'game-app')
    shadow_root1 = root1.shadow_root
    root2 = shadow_root1.find_element(By.CSS_SELECTOR, f"game-row[letters={word}]")
    shadow_root2 = root2.shadow_root
    root3 = shadow_root2.find_element(By.CSS_SELECTOR, f"game-tile[letter={letter}]")
    shadow_root3 = root3.shadow_root
    tile = shadow_root3.find_element(By.CSS_SELECTOR, ".tile")

    return tile.get_attribute("data-state")

def tileRowStatesWithIndex(word):
    return [
        [tileStateWithLetter(word, word[0]), 0], 
        [tileStateWithLetter(word, word[1]), 1], 
        [tileStateWithLetter(word, word[2]), 2], 
        [tileStateWithLetter(word, word[3]), 3], 
        [tileStateWithLetter(word, word[4]), 4]
        ]

def tileRowStates(word):
    return [
        tileState(word, word[0]),
        tileState(word, word[1]),
        tileState(word, word[2]),
        tileState(word, word[3]),
        tileState(word, word[4])
        ]

def getAll5LetterWords(): 
    my_file = open("wordleWords.txt", "r")
    data = my_file.read()
    data_into_list = data.split(",")
    my_file.close()

    return data_into_list

def logic(rowStatesWithIndex):
    for tileStateWithLetter in rowStatesWithIndex:

        if(tileStateWithLetter[0][1] == "absent"):
            variables.absentLetters.append(tileStateWithLetter[0][0])
        
        elif(tileStateWithLetter[0][1] == "present"):
            variables.letterAndIndexForPresent.append([tileStateWithLetter[0][0], tileStateWithLetter[1]])
            
        else:
            variables.letterAndIndexForCorrect.append([tileStateWithLetter[0][0], tileStateWithLetter[1]]) 
    
    for word in list(variables.wordsList):

        for letter in variables.absentLetters:
            if(letter in word):
                if(word not in variables.wordsList):
                    continue
                else:
                    if(word not in variables.wordsList):
                        continue
                    else:
                        variables.wordsList.remove(word)

        for element in variables.letterAndIndexForPresent:
            if(element[0] in word):
                if(word not in variables.wordsList):
                    continue
                else:
                    if(word.find(element[0]) == element[1]): 
                        variables.wordsList.remove(word)
            else:
                if(word not in variables.wordsList):
                    continue
                else:
                    variables.wordsList.remove(word)
        
        for element in variables.letterAndIndexForCorrect:
            if(element[0] in word):
                if word not in variables.wordsList:
                    continue
                else:
                    if(word.find(element[0]) != element[1]): 
                        variables.wordsList.remove(word)
            else:
                if(word not in variables.wordsList):
                    continue
                else:
                    variables.wordsList.remove(word)
            
def wordleBot():
    functions.initalSteps() 

    logic(tileRowStatesWithIndex("roate"))
    nextWord = random.choice(variables.wordsList)
    typeInWord(nextWord)

    while(not(tileRowStates(nextWord)== ["correct", "correct", "correct", "correct", "correct"])):

        logic(tileRowStatesWithIndex(nextWord))
        nextWord = random.choice(variables.wordsList) 
        typeInWord(nextWord)

    print("Done")