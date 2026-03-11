from game import Game
from mainMenu import MainMenu

if __name__ == "__main__":
    menu = MainMenu()
    menu.run()
    print(menu.info.online)
    print(menu.info.start_game)
    print(menu.info.number_of_players)
    print(menu.info.number_of_bots)
    # Game("127.0.0.1", 63659).run()