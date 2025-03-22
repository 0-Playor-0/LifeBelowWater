import pygame
import random 

pygame.init()
screen = pygame.display.set_mode((711,400))
pygame.display.set_caption("Level One")
clock = pygame.time.Clock()


#Score
global score
global game_over 
game_over = False
game_started = True
game_paused = False
score = 0
score_font = pygame.font.Font('Pixeltype.ttf',20)
score_surf = score_font.render(f'Score : {score}', False, 'Green')
game_over_surf = score_font.render(f'Game Over, Score : {score}', False, 'Red')
pause_surf = score_font.render(f'Game Paused, Score : {score}', False, 'Red')
game_cleared = False

#Resources
bg = pygame.image.load('bg.png').convert()
bg = pygame.transform.scale(bg, (711, 400))
game_over_surf = pygame.image.load('over.png').convert()
game_over_surf = pygame.transform.scale(game_over_surf, (711, 400))
level_over_surf = pygame.image.load('clear.png').convert()
level_over_surf = pygame.transform.scale(level_over_surf, (711, 400))


bottles = []
#Bottle
numBottle = 3
for x in range (numBottle):
    bottle = pygame.image.load('bottle.png').convert_alpha()
    bottle = pygame.transform.scale(bottle,(25, 50))
    bottles.append(bottle)

#Fish
fish = pygame.image.load('fish.png').convert_alpha()
fish = pygame.transform.scale(fish,(44, 26))
fish_rect = fish.get_rect(bottomright = (200,300))
fish_speed = 2.5
bottles_rect = []

#Bottle One
bottle_x_pos = random.randint(200,700)
bottle_y_pos = 175
bottle_rect = bottle.get_rect(center=(bottle_x_pos, bottle_y_pos))
bottles_rect.append(bottle_rect)

#Spawning bottles
bottle_speed = 2
for x in range(numBottle):
    if random.randint(0,1) == 0:
        bottle_x_pos = bottles_rect[0].x + x*random.randint(100, 200)
    else:
        bottle_x_pos = bottles_rect[0].x - x*random.randint(100, 200)

    bottle_y_pos = 175
    bottle_rect = bottle.get_rect(center=(bottle_x_pos, bottle_y_pos))
    bottles_rect.append(bottle_rect)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(bg,(0,0))
    if game_over is not True and game_paused is not True:
        #Bottle
        for a in range(numBottle):
            bottles_rect[a].y += bottle_speed+random.randint(-1,1)
            if bottles_rect[a].y > 350:
                bottles_rect[a].y = 175
                if random.randint(0,1) == 0:
                    bottles_rect[a].x = random.randint(200,700) + a*random.randint(100, 200)
                else:
                    bottles_rect[a].x = random.randint(200,700) - a*random.randint(100, 200)
        
        score += 0.01



        #Keyboard inputs
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and fish_rect.y>200:
            fish_rect.y -= fish_speed
        if keys[pygame.K_DOWN] and fish_rect.y < 375:
            fish_rect.y += fish_speed
        if keys[pygame.K_LEFT] and fish_rect.x>0:
            fish_rect.x -= fish_speed
        if keys[pygame.K_RIGHT] and fish_rect.x<670:
            fish_rect.x += fish_speed
        if keys[pygame.K_ESCAPE]:
            if game_paused == True:
                game_paused = False
            if game_paused == False:
                game_paused = True
        

        #The Fishes
        for x in range(numBottle):
            screen.blit(bottle,bottles_rect[x])
        screen.blit(fish,fish_rect)
    

        #Surfaces dynamically changing
        score_surf = score_font.render(f'Score : {int(score)}', False, 'Red')
        score_checked = [0]
        bottle_speed += 0.0001
        #Increasing Difficulty of game
        if score>50:
            if score not in score_checked:
                score_checked.append(score)
                if random.randint(0,1) == 0:
                    bottle_x_pos = bottles_rect[0].x + x*random.randint(100, 200)
                else:
                    bottle_x_pos = bottles_rect[0].x - x*random.randint(100, 200)

                bottle_y_pos = 175
                bottle_rect = bottle.get_rect(center=(bottle_x_pos, bottle_y_pos))
                bottles_rect.append(bottle_rect)
                numBottle+=1
        #Game Over logic
        for i in range(numBottle):
            if fish_rect.colliderect(bottles_rect[i]) == True:
                game_over = True
    
    
    keys = pygame.key.get_pressed()
    if game_paused == True:
        game_over_surf = score_font.render(f'Game Over, Score : {score}', False, 'Red')
        screen.blit(game_over_surf,(300,200))
        if keys[pygame.K_ESCAPE] and game_paused == True:
            game_paused = False
    if game_over == True and not game_cleared:
        screen.blit(game_over_surf,(0,0))
        #screen.blit(game_over_surf,(350, 150))
        if keys[pygame.K_SPACE] and game_over == True:
            game_over = False
            score = 0
            bottle_speed = 2
            print(game_over)
    if score>50:
        screen.blit(level_over_surf,(0,0))
        game_cleared = True

    
    screen.blit(score_surf,(600,50))
    pygame.display.update()
    clock.tick(60)
