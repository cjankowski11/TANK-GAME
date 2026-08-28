from experience_replay import ReplayBuffer
from dqn import DQN
from game_bot_wrapper import Wrapper
from player import BotPlayer
from gameEngine import GameEngine
FPS = 60
EPISODES = 1
quality_nn = DQN(52, 18)
target_nn = DQN(52, 18)
target_nn.load_state_dict(quality_nn.state_dict())
bot1 = BotPlayer("bot1", neural_network=quality_nn)
bot2 = BotPlayer("bot2", neural_network=quality_nn)
bot3 = BotPlayer("bot3", neural_network=quality_nn)
bot4 = BotPlayer("bot4", neural_network=quality_nn)
bots = [bot1, bot2, bot3, bot4]
memory = ReplayBuffer(10_000)

game = GameEngine(bots, FPS)
wrapped_game = Wrapper(game)

for ep in range(EPISODES):
    obs1 = wrapped_game.get_obs(bot1)
    obs2 = wrapped_game.get_obs(bot2)
    obs3 = wrapped_game.get_obs(bot3)
    obs4 = wrapped_game.get_obs(bot4)
    print(obs1)
    action1 = bot1.get_action(obs1)
    print(action1)





