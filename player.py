import random
import pygame
from dqn import DQN
import torch
# import stable_baselines3


class Player:
    def __init__(self, name="player", ready_status=None, lta=None):
        self.name = name
        self.points = 0
        self.ready = ready_status
        self.last_time_active = lta
        self.active_instructions = {
            "w": False, "a": False, "s": False,
            "d": False, "shoot": False}
        
    def update(self, w, a, s, d, shoot):
        self.active_instructions = {
            "w": w, "a": a, "s": s, "d": d, "shoot": shoot}
        
    def get_instructions(self):
        return self.active_instructions
    
    def is_bot(self):
        return False
    
    def add_point(self):
        self.points += 1

    def set_ready_status(self, ready_status):
        self.ready = ready_status

    def set_last_active_time(self, lta):
        self.last_time_active = lta

    def set_name(self, name):
        self.name = name


class BotPlayer(Player):
    def __init__(self, name="bot", neural_network=None):
        super().__init__(name)
        self.walls = []
        self.bullets = []
        self.players = {}
        self.nn = neural_network

    def get_action(self, state):
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        q_values = self.nn.forward(state)
        action = torch.argmax(q_values, dim=1).item()
        return action
    
    def is_bot(self):
        return True

