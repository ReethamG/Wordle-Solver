import variables
import functions
import time

def run(): #All the functions together in a function
    variables.driver.get('https://www.nytimes.com/games/wordle/index.html')
    functions.initalSteps()
    time.sleep(4)