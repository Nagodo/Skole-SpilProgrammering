import pygame
import random

game_state = 0

offset = [5, 5]
max_width = 750
tile_size = 20
tile_border_w = (20 * 0.1)
tile_border_offset = tile_border_w / 2
difficulty = 1
textdata = [(32, (-8, -18)),(18, (-5, -10)),(10, (-3, -6)),(8, (-2, -4)),(8, (-2, -4))]

tile_colors = [(0, 0, 0),  (0, 0, 255), (255, 0, 0), (0, 255, 0),(255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 255, 255)]

class Game():
    def draw(self):
        if game_state == 0:
            screen.fill((0, 0, 0))
            #Draw title
            font = pygame.font.SysFont('Arial', 50)
            text = font.render('Minesweeper', True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (max_width / 2, 100)
            screen.blit(text, textRect)

            #Draw start game text
            font = pygame.font.SysFont('Arial', 30)
            text = font.render('Tryk ENTER for at starte', True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (max_width / 2, 200)
            screen.blit(text, textRect)

            #Draw difficulty text
            font = pygame.font.SysFont('Arial', 30)
            text = font.render('Sværhedsgrad: ' + str(difficulty), True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (max_width / 2, 300)
            screen.blit(text, textRect)
        
        if game_state == 1:
            for x in range(len(self.grid.grid)):
                for y in range(len(self.grid.grid[x])):
                    if self.grid.grid[x][y].updated:
                        self.grid.grid[x][y].updated = False
                        pygame.draw.rect(screen, (240,240,240,255), pygame.Rect(x * tile_size + offset[0], y * tile_size + offset[1], tile_size, tile_size))
                    
                        if self.grid.grid[x][y].hover:
                            pygame.draw.rect(screen, (159,159,159,255), pygame.Rect(x * tile_size + offset[0] + tile_border_offset, y * tile_size + offset[1] + tile_border_offset, tile_size - tile_border_w, tile_size - tile_border_w))
                        else:
                            pygame.draw.rect(screen, (189,189,189,255), pygame.Rect(x * tile_size + offset[0] + tile_border_offset, y * tile_size + offset[1] + tile_border_offset, tile_size - tile_border_w, tile_size - tile_border_w))

                        if self.grid.grid[x][y].isflagged:
                            pygame.draw.rect(screen, (255,0,0,255), pygame.Rect(x * tile_size + offset[0] + tile_border_offset, y * tile_size + offset[1] + tile_border_offset, tile_size - tile_border_w, tile_size - tile_border_w))

                        if self.grid.grid[x][y].isRevealed:
                            pygame.draw.rect(screen, (219,219,219,255), pygame.Rect(x * tile_size + offset[0] + tile_border_offset, y * tile_size + offset[1] + tile_border_offset, tile_size - tile_border_w, tile_size - tile_border_w))
                            if self.grid.grid[x][y].bombsNear:
                                font = pygame.font.SysFont('Arial', textdata[difficulty-1][0], True)
                                color = tile_colors[self.grid.grid[x][y].bombsNear]
                                text = font.render(str(self.grid.grid[x][y].bombsNear), True, color)
                                screen.blit(text, (x * tile_size + offset[0] + textdata[difficulty-1][1][0] + tile_size / 2, y * tile_size + offset[1] + textdata[difficulty-1][1][1] + tile_size / 2))
                            if self.grid.grid[x][y].isBomb:
                                pygame.draw.circle(screen, (0,0,0,255), (int(x * tile_size + offset[0] + tile_size / 2), int(y * tile_size + offset[1] + tile_size / 2)), int(tile_size / 3))
                       

    def StartGame(self):
        global tile_size
        global game_state
        grid_amount = 15 * difficulty
        SetMaxWidth(difficulty)
        tile_size = (max_width / grid_amount)
        self.grid = Grid(grid_amount)
        screen.fill((0, 0, 0))
        game_state = 1
    
    def GameOver(self):
        for x in range(len(self.grid.grid)):
            for y in range(len(self.grid.grid[x])):
                self.grid.grid[x][y].isRevealed = True
                self.grid.grid[x][y].updated = True
                    

class Grid():
    def __init__(self, amount):
        self.grid = [[Tile(j, i) for i in range(amount)] for j in range(amount)]
        self.firstpress = False
        self.firstpresspos = (0, 0)
        #Set bombs

    def GenerateBombs(self, amount, difficulty):
        a = (amount * (difficulty + (difficulty * 2)))
        i = 0
        while i < a:
            i += 1
            x = random.randint(0, amount - 1)
            y = random.randint(0, amount - 1)
            if x == self.firstpresspos[0] or y == self.firstpresspos[1]:
                i -= 1
            else:
                self.grid[x][y].isBomb = True

        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                if self.grid[x][y].isBomb:
                    
                    if x-1 >= 0:
                        if not self.grid[x-1][y].isBomb:
                            self.grid[x-1][y].bombsNear += 1
                        
                        if y-1 >= 0:
                            if not self.grid[x-1][y-1].isBomb:
                                self.grid[x-1][y-1].bombsNear += 1

                        if y+1 < len(self.grid[x-1]):
                            if not self.grid[x-1][y+1].isBomb:
                                self.grid[x-1][y+1].bombsNear += 1
                    
                    if y-1 >= 0:
                        if not self.grid[x][y-1].isBomb:
                            self.grid[x][y-1].bombsNear += 1
                    
                    if y+1 < len(self.grid[x]):
                        if not self.grid[x][y+1].isBomb:
                            self.grid[x][y+1].bombsNear += 1

                    if x+1 < len(self.grid):
                        if not self.grid[x+1][y].isBomb:
                            self.grid[x+1][y].bombsNear += 1
                        
                        if y-1 >= 0:
                            if not self.grid[x+1][y-1].isBomb:
                                self.grid[x+1][y-1].bombsNear += 1

                        if y+1 < len(self.grid[x+1]):
                            if not self.grid[x+1][y+1].isBomb:
                                self.grid[x+1][y+1].bombsNear += 1
    
    

class Tile():
    def __init__(self, i, j):
        self.hover = False
        self.isRevealed = False
        self.isBomb = False
        self.bombsNear = 0
        self.updated = True
        self.isflagged = False
        self.x = i
        self.y = j
    
    def OnClick(self):
        if not game.grid.firstpress:
            game.grid.firstpress = True
            game.grid.firstpresspos = (self.x, self.y)
            game.grid.GenerateBombs(len(game.grid.grid), difficulty)

        if self.isBomb:
            game.GameOver()
            return
        
        if self.isflagged:
            return

        self.RevealThis()

    def RevealThis(self):
        self.isRevealed = True
        self.updated = True

        
        if self.x + 1 < len(game.grid.grid):
            if not game.grid.grid[self.x+1][self.y].isRevealed and not game.grid.grid[self.x+1][self.y].isflagged and not game.grid.grid[self.x+1][self.y].isBomb and not (game.grid.grid[self.x+1][self.y].bombsNear > 0 and game.grid.grid[self.x][self.y].bombsNear > 0):
                game.grid.grid[self.x+1][self.y].RevealThis()
            
            if self.y + 1 < len(game.grid.grid[self.x+1]):
                if not game.grid.grid[self.x+1][self.y+1].isRevealed and not game.grid.grid[self.x+1][self.y+1].isflagged and not game.grid.grid[self.x+1][self.y+1].isBomb and not (game.grid.grid[self.x+1][self.y+1].bombsNear > 0 and game.grid.grid[self.x][self.y].bombsNear > 0):
                    game.grid.grid[self.x+1][self.y+1].RevealThis()
            
            if self.y - 1 >= 0:
                if not game.grid.grid[self.x+1][self.y-1].isRevealed and not game.grid.grid[self.x+1][self.y-1].isflagged and not game.grid.grid[self.x+1][self.y-1].isBomb and not (game.grid.grid[self.x+1][self.y-1].bombsNear > 0 and game.grid.grid[self.x][self.y].bombsNear > 0):
                    game.grid.grid[self.x+1][self.y-1].RevealThis()
        
        if self.x - 1 >= 0:
            if not game.grid.grid[self.x-1][self.y].isRevealed and not game.grid.grid[self.x-1][self.y].isflagged and not game.grid.grid[self.x-1][self.y].isBomb and not (game.grid.grid[self.x-1][self.y].bombsNear > 0 and game.grid.grid[self.x][self.y].bombsNear > 0):
                game.grid.grid[self.x-1][self.y].RevealThis()
            
            if self.y + 1 < len(game.grid.grid[self.x-1]):
                if not game.grid.grid[self.x-1][self.y+1].isRevealed and not game.grid.grid[self.x-1][self.y+1].isflagged and not game.grid.grid[self.x-1][self.y+1].isBomb and not (game.grid.grid[self.x-1][self.y+1].bombsNear > 0 and game.grid.grid[self.x][self.y].bombsNear > 0):
                    game.grid.grid[self.x-1][self.y+1].RevealThis()

            if self.y - 1 >= 0:
                if not game.grid.grid[self.x-1][self.y-1].isRevealed and not game.grid.grid[self.x-1][self.y-1].isflagged and not game.grid.grid[self.x-1][self.y-1].isBomb and not (game.grid.grid[self.x-1][self.y-1].bombsNear > 0 and game.grid.grid[self.x][self.y].bombsNear > 0):
                    game.grid.grid[self.x-1][self.y-1].RevealThis()

        if self.y + 1 < len(game.grid.grid):
            if not game.grid.grid[self.x][self.y+1].isRevealed and not game.grid.grid[self.x][self.y+1].isflagged and not game.grid.grid[self.x][self.y+1].isBomb and not (game.grid.grid[self.x][self.y+1].bombsNear > 0 and game.grid.grid[self.x][self.y].bombsNear > 0):
                game.grid.grid[self.x][self.y+1].RevealThis()
        
        if self.y - 1 >= 0:
            if not game.grid.grid[self.x][self.y-1].isRevealed and not game.grid.grid[self.x][self.y-1].isflagged and not game.grid.grid[self.x][self.y-1].isBomb and not (game.grid.grid[self.x][self.y-1].bombsNear > 0 and game.grid.grid[self.x][self.y].bombsNear > 0):
                game.grid.grid[self.x][self.y-1].RevealThis()
        
                  

    
    def OnRightClick(self):
        if self.isflagged:
            self.isflagged = False
            self.updated = True
            return
        self.isflagged = True
        self.updated = True

def SetMaxWidth(difficulty):
    global max_width
    if difficulty == 3:
        max_width = 720
    if difficulty == 4:
        max_width = 840
    if difficulty == 5:
        max_width = 900
    



#Init
pygame.init()
screen = pygame.display.set_mode((1000, 920))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

game = Game()





#Game Loop
running = True
while running:
    #Events
    for event in pygame.event.get():
        #Mouse down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and game_state == 0:
                game.StartGame()

            if event.key == pygame.K_r and game_state == 1:
                game_state = 0

            if event.key == pygame.K_1 and game_state == 0:
                difficulty = 1
            if event.key == pygame.K_2 and game_state == 0:
                difficulty = 2
            if event.key == pygame.K_3 and game_state == 0:
                difficulty = 3
            if event.key == pygame.K_4 and game_state == 0:
                difficulty = 4
            if event.key == pygame.K_5 and game_state == 0:
                difficulty = 5
       
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == 1:
                for x in range(len(game.grid.grid)):
                    for y in range(len(game.grid.grid[x])):
                        if mouse_x > x * tile_size and mouse_x < x * tile_size + tile_size and mouse_y > y * tile_size and mouse_y < y * tile_size + tile_size:
                            if event.button == 1:
                                game.grid.grid[x][y].OnClick()
                            elif event.button == 3:
                                game.grid.grid[x][y].OnRightClick()
         
                

        if event.type == pygame.QUIT:
            running = False


    #Update
    mouse_pos = pygame.mouse.get_pos()
    
    mouse_x = mouse_pos[0] - offset[0]
    mouse_y = mouse_pos[1] - offset[1]
    if game_state == 1:
        for x in range(len(game.grid.grid)):
            for y in range(len(game.grid.grid[x])):
                if mouse_x > x * tile_size and mouse_x < x * tile_size + tile_size and mouse_y > y * tile_size and mouse_y < y * tile_size + tile_size:
                    game.grid.grid[x][y].hover = True
                    game.grid.grid[x][y].updated = True
                else:
                    if game.grid.grid[x][y].hover:
                        game.grid.grid[x][y].hover = False
                        game.grid.grid[x][y].updated = True
                
            

    game.draw()
    
    pygame.display.flip()
    clock.tick(60)

