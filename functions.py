import variables
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import functions
import time
import random

def initalSteps():  #Add a removed word list
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
    
def indexes(my_list, desired_element):
    return [index for index, element in enumerate(my_list) if element == desired_element]

def tileRowStates(word):
    i = 0
    tileRowStates = []

    for letter in word:

        if(word.count(letter) > 1):
            root1 = variables.driver.find_element(By.CSS_SELECTOR, 'game-app')
            shadow_root1 = root1.shadow_root
            root2 = shadow_root1.find_element(By.CSS_SELECTOR, f"game-row[letters={word}]")
            shadow_root2 = root2.shadow_root
            root3 = shadow_root2.find_element(By.CSS_SELECTOR, f" div:nth-child(2) > game-tile:nth-child({(indexes(word, letter)[i]) + 1})")
            shadow_root3 = root3.shadow_root
            tile = shadow_root3.find_element(By.CSS_SELECTOR, ".tile")
            tileRowStates.append(tile.get_attribute("data-state"))
            i = i + 1
        else:
            root1 = variables.driver.find_element(By.CSS_SELECTOR, 'game-app')
            shadow_root1 = root1.shadow_root
            root2 = shadow_root1.find_element(By.CSS_SELECTOR, f"game-row[letters={word}]")
            shadow_root2 = root2.shadow_root
            root3 = shadow_root2.find_element(By.CSS_SELECTOR, f"game-tile[letter={letter}]")
            shadow_root3 = root3.shadow_root
            tile = shadow_root3.find_element(By.CSS_SELECTOR, ".tile")
            tileRowStates.append(tile.get_attribute("data-state"))

    return tileRowStates

def tileRowStatesWithIndex(word):
    i = 0
    tileRowStatesWithIndex = []

    for letter in word:

        if(word.count(letter) > 1): 
            root1 = variables.driver.find_element(By.CSS_SELECTOR, 'game-app')
            shadow_root1 = root1.shadow_root
            root2 = shadow_root1.find_element(By.CSS_SELECTOR, f"game-row[letters={word}]")
            shadow_root2 = root2.shadow_root
            root3 = shadow_root2.find_element(By.CSS_SELECTOR, f" div:nth-child(2) > game-tile:nth-child({(indexes(word, letter)[i]) + 1})")
            shadow_root3 = root3.shadow_root
            tile = shadow_root3.find_element(By.CSS_SELECTOR, ".tile")
            tileRowStatesWithIndex.append([[letter, tile.get_attribute("data-state")], indexes(word, letter)[i]])
            i = i + 1

        else:
            root1 = variables.driver.find_element(By.CSS_SELECTOR, 'game-app')
            shadow_root1 = root1.shadow_root
            root2 = shadow_root1.find_element(By.CSS_SELECTOR, f"game-row[letters={word}]")
            shadow_root2 = root2.shadow_root
            root3 = shadow_root2.find_element(By.CSS_SELECTOR, f"game-tile[letter={letter}]")
            shadow_root3 = root3.shadow_root
            tile = shadow_root3.find_element(By.CSS_SELECTOR, ".tile")
            tileRowStatesWithIndex.append([[letter, tile.get_attribute("data-state")], word.find(letter)])

    return tileRowStatesWithIndex

def getAll5LetterWords(): 
    my_file = open("wordleWords.txt", "r")
    data = my_file.read()
    data_into_list = data.split(",")
    my_file.close()

    return data_into_list

def logic(rowStatesWithIndex):

    toCheckForDuplication = []
    duplicationInWord = False
    duplicatedLetter = ' '

    for element in rowStatesWithIndex:
        toCheckForDuplication.append(element[0][0])

    for letter in toCheckForDuplication:
        if(toCheckForDuplication.count(letter) > 1):
            duplicatedLetter = letter
            duplicationInWord = True
            break

    for tileStateWithLetter in rowStatesWithIndex:

        if(tileStateWithLetter[0][1] == "absent"):

            if(duplicationInWord == False):
                variables.absentLetters.append(tileStateWithLetter[0][0])
            else:
                variables.absentLetters.append(tileStateWithLetter[0][0])
                for element in list(variables.absentLetters):
                    if(element == duplicatedLetter):
                        variables.absentLetters.remove(element)
                 
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
                if(word not in variables.wordsList):
                    continue
                elif(word.find(element[0]) != element[1]):
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

    while(not(tileRowStates(nextWord) == ["correct", "correct", "correct", "correct", "correct"])):
        logic(tileRowStatesWithIndex(nextWord))
        nextWord = random.choice(variables.wordsList)
        typeInWord(nextWord)

    print("Done")