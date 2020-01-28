from modules.environment import Environment
from modules.player import Player


env = Environment(
    p1=Player(name='Alice'),
    p2=Player(name='Bob')
)
env.launch_game(iterations=10)
