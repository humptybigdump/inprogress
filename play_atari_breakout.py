import gymnasium as gym
from pygame.locals import *
import ale_py
from gymnasium.utils.play import play

gym.register_envs(ale_py)
play(
    gym.make("ALE/Breakout-v5", render_mode="rgb_array"),
    keys_to_action={
        "a": 3,    # LEFT
        "d": 2,    # RIGHT
        " ": 1,    # FIRE
    },
    noop=0,
    fps=10 # FPS controls the speed of the game
)