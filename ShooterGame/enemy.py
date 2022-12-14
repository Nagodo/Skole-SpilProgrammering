import pygame
import random
enemies = []

class Enemy():
    def __init__(self):
        self.position = self.RandPos()
        self.image = pygame.image.load("images/enemy.png")
        self.speed = 5
        self.health = 100

    def RandPos(self):
        self.position = [random.randint(0, 1200), random.randint(0, 600)]
        return self.position
