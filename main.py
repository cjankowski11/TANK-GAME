from mainMenu import MainMenu
from localGame import LocalGame
from onlineGame import OnlineGame
if __name__ == "__main__":
    while True:
        menu = MainMenu()
        game = None
        menu_info = menu.run()
        print(menu_info.online)
        if menu_info.online:
            game = OnlineGame(menu_info.number_of_bots, menu_info.number_of_rounds, menu_info.socket, )
            game.start_connection()
            pass
        elif menu_info.online is None:
            pass
        else:
            game = LocalGame(menu_info.number_of_players, menu_info.number_of_bots)
        if game is None:
            break
        else:
            for _ in range(1):
                game_running = game.run()
                if game_running is False:
                    break
    