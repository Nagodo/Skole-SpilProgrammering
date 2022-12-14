import pygame

class Player():
    def __init__(self):
        self.position = [0,0]

        self.images = [pygame.image.load("images/player1.png"),pygame.image.load("images/player2.png"),pygame.image.load("images/player3.png")]

        self.animation_state = 0