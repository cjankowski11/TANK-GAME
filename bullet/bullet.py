import time
import pygame

class Bullet:
    def __init__(self, position):
        self.position = position

    def get_position(self):
        return self.position