import variables
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import functions
import time
import random


def initalSteps():  # Add a removed word list
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


def tileRowStates(word, row):
    i = 0
    tileRowStates = []

    for letter in word:

        if(word.count(letter) > 1):
            tile = variables.driver.find_element_by_xpath(
                f'//*[@id="wordle-app-game"]/div[1]/div/div[{row}]/div[{(indexes(word, letter)[i])+1}]/div')
            tileRowStates.append(tile.get_attribute("data-state"))
            i = i + 1
        else:
            tile = variables.driver.find_element_by_xpath(
                f'//*[@id="wordle-app-game"]/div[1]/div/div[{row}]/div[{(indexes(word, letter)[0])+1}]/div')
            tileRowStates.append(tile.get_attribute("data-state"))

    return tileRowStates


def tileRowStatesWithIndex(word, row):
    i = 0
    tileRowStatesWithIndex = []

    for letter in word:

        if(word.count(letter) > 1):
            tile = variables.driver.find_element_by_xpath(
                f'//*[@id="wordle-app-game"]/div[1]/div/div[{row}]/div[{(indexes(word, letter)[i])+1}]/div')
            tileRowStatesWithIndex.append(
                [[letter, tile.get_attribute("data-state")], indexes(word, letter)[i]])
            i = i + 1

        else:
            tile = variables.driver.find_element_by_xpath(
                f'//*[@id="wordle-app-game"]/div[1]/div/div[{row}]/div[{(indexes(word, letter)[0])+1}]/div')
            tileRowStatesWithIndex.append(
                [[letter, tile.get_attribute("data-state")], word.find(letter)])

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
            variables.letterAndIndexForPresent.append(
                [tileStateWithLetter[0][0], tileStateWithLetter[1]])

        else:
            variables.letterAndIndexForCorrect.append(
                [tileStateWithLetter[0][0], tileStateWithLetter[1]])

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
    row = 1
    functions.initalSteps()
    logic(tileRowStatesWithIndex("roate", row))
    nextWord = random.choice(variables.wordsList)
    typeInWord(nextWord)
    row = row + 1

    while(not(tileRowStates(nextWord, row) == ["correct", "correct", "correct", "correct", "correct"])):
        logic(tileRowStatesWithIndex(nextWord, row))
        nextWord = random.choice(variables.wordsList)
        typeInWord(nextWord)
        row = row + 1

    print("Done")
