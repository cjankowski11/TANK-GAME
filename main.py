from game import Game
from mainMenu import MainMenu

if __name__ == "__main__":
    menu = MainMenu()
    menu.run()
    print(menu.info.online)
    # Game("127.0.0.1", 63659).run()