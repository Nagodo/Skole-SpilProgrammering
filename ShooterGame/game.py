import pygame
from player import Player
from bullet import Bullet, bullets
from enemy import Enemy, enemies


pygame.init()

screen = pygame.display.set_mode((1420, 880))
#FUllscreen

pygame.display.set_caption("Shooter Game")
clock = pygame.time.Clock()

gamerunning = True

class Game():
    def __init__(self):
        self.player = Player()
        self.SpawnEnemy()
        self.score = 0

    def draw_background(self):
        screen.fill((0,0,0))

    def draw_game(self):
        #Draw player sprite
        screen.blit(self.player.images[self.player.animation_state], (self.player.position[0], self.player.position[1]))
        for i in range(len(bullets)):
            screen.blit(bullets[i].image, (bullets[i].position[0], bullets[i].position[1]))

        for i in range(len(enemies)):
            screen.blit(enemies[i].image, (enemies[i].position[0], enemies[i].position[1]))
        
        #Draw score
        font = pygame.font.Font(None, 36)
        text = font.render("Score: " + str(self.score), 1, (255, 255, 255))
        screen.blit(text, (10, 10))

        #Draw line from player to mouse
        pygame.draw.line(screen, (255, 255, 255), (self.player.position[0] + 80, self.player.position[1] + 100), pygame.mouse.get_pos(), 5)

    def SpawnEnemy(self):
        enemies.append(Enemy())

def GetDirectionToMouse():
    mouse = pygame.mouse.get_pos()
    player = game.player.position
    x = mouse[0] - player[0]
    y = mouse[1] - player[1]
    return [x, y]

game = Game()

elapsed = 0
while gamerunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamerunning = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.score -= 1
            bullet = Bullet(GetDirectionToMouse(), [game.player.position[0], game.player.position[1]])
            
    #Movement
    keys = pygame.key.get_pressed()  #checking pressed keys
    
    move = [0, 0]
    if keys[pygame.K_w]:
        move[1] -= 1
    if keys[pygame.K_s]:
        move[1] += 1
    if keys[pygame.K_a]:
        move[0] -= 1
    if keys[pygame.K_d]:
        move[0] += 1
           
    if move[0] != 0 or move[1] != 0:
        
        game.player.position[0] += move[0]
        game.player.position[1] += move[1]
        if elapsed > 5:
            elapsed = 0
            game.player.animation_state = (game.player.animation_state + 1) % 3
            

    else:
        game.player.animation_state = 0

    if len(bullets) > 0:
        for bullet in bullets:
            bullet.position[0] += bullet.direction[0] * bullet.speed
            bullet.position[1] += bullet.direction[1] * bullet.speed

            if len(enemies) > 0:
                for e in enemies:
                    if bullet.position[0] > e.position[0] and bullet.position[0] < e.position[0] + 200:
                        if bullet.position[1] > e.position[1] and bullet.position[1] < e.position[1] + 200:
                            enemies.remove(e)
                            bullets.remove(bullet)
                            game.SpawnEnemy()
                            game.score += 2
                            break

            
            
    
    game.draw_background()
    game.draw_game()

    pygame.display.flip()
    clock.tick(60)

    elapsed += 1

