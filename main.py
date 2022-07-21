import variables
import functions


def run():
    variables.driver.get('https://www.nytimes.com/games/wordle/index.html')
    functions.wordleBot()


if __name__ == '__main__':
    run()
