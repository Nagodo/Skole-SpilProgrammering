import pygame
bullets = []

clock = pygame.time.Clock()

class Bullet():
    def __init__(self, direction, position):

        position[0] += 80
        position[1] += 100

        self.position = position
        self.image = pygame.image.load("images/bullet.png")
        self.speed = 20

        #Convert direction to unit vector
        magnitude = (direction[0]**2 + direction[1]**2)**0.5
        self.direction = [direction[0]/magnitude, direction[1]/magnitude]


        bullets.append(self)

