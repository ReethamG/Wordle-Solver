import variables
import functions

def run():
    variables.driver.get('https://www.nytimes.com/games/wordle/index.html')

    functions.initalSteps()


    variables.action.perform()