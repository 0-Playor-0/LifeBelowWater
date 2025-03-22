import pygame
import random
import time
import sys
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Level Boss Fight")
clock = pygame.time.Clock()


# Images
og_image = pygame.image.load("graphics/sub.png").convert_alpha()
sub_image = pygame.transform.scale(og_image, (200, 200))
sub_rect = sub_image.get_rect(center=(400, 200))
sub_hitbox = pygame.Rect(300, 150, 180, 100)

# Game Control
game_over = False
game_paused = False
game_cleared = False

swimmer = pygame.image.load("graphics/0.png").convert_alpha()
swimmer = pygame.transform.scale(swimmer, (100, 60))
swimmer_rect = swimmer.get_rect(center=(200, 200))
swimmer_hitbox = pygame.Rect(0, 0, 90, 50)
swimmer_hitbox.center = swimmer_rect.center
swimmer_speed = 5


# Health & UI
sub_health = 100
sub_max_health = 100
sub_health_bar_rect = pygame.Rect(320, 125, 160, 15)
swimmer_status = 'Idle'

# Missile variables
missiles = []
def spawn_missile(numMissile):
    spawn_loc = [50, 100, 150, 200, 250, 300, 350]
    sp_loc = random.sample(spawn_loc, numMissile)
    for i in range(numMissile):
        missile = pygame.image.load('graphics/missile.png').convert_alpha()
        missile = pygame.transform.scale(missile, (70, 50))
        missile = pygame.transform.flip(missile, True, False)
        missile_info = [missile]
        missile_rect = missile.get_rect(center=(700, sp_loc[i]))
        missile_info.append(missile_rect)
        missile_hitbox = pygame.Rect(0, 0, 50, 35)
        missile_hitbox.center = missile_rect.center
        missile_info.append(missile_hitbox)
        missiles.append(missile_info)

# Show health bar
def show_bar(screen, current, max_amount, bg_rect, color):
    pygame.draw.rect(screen, 'Gray', bg_rect)  
    ratio = current / max_amount
    current_width = bg_rect.width * ratio
    current_rect = bg_rect.copy()
    current_rect.width = current_width
    pygame.draw.rect(screen, color, current_rect)  
    pygame.draw.rect(screen, 'Black', bg_rect, 3) 

# Hearts
red = pygame.image.load('graphics/redheart.png').convert_alpha()
gray = pygame.image.load('graphics/blackheart.png').convert_alpha()
red = pygame.transform.scale(red, (25, 25))
gray = pygame.transform.scale(gray, (25, 25))
numHearts = 3
attacking = False
level_over_surf = pygame.image.load('graphics/clear.png').convert()
level_over_surf = pygame.transform.scale(level_over_surf, (711, 400))
# Background
bg = pygame.image.load('graphics/bossbg.png').convert()
bg = pygame.transform.scale(bg, (800, 400))

# Attack cooldown
last_attack_time = 0
attack_cooldown = 500
idle_frame = 0
frame = 0
do_attack = False

# Game loop
while True:
    if sub_health <= 0:
        game_cleared = True  # Player wins
        game_over = True  # End game
    if numHearts <= 0:
        game_over = True  # Player loses





    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.blit(bg, (0, 0))
    screen.blit(sub_image, sub_rect)

    # Hearts display
    heart_images = [red if i < numHearts else gray for i in range(3)]
    for i, img in enumerate(heart_images):
        screen.blit(img, (20 + i * 40, 20))
    
    if swimmer_status != 'swim' and not attacking and swimmer_status != 'hurt' and idle_frame < 4:
        swimmer = pygame.image.load(f"idle\{idle_frame}.png").convert_alpha()
        swimmer = pygame.transform.scale(swimmer, (100, 60))
        if random.randint(0, 3) == 1:
            idle_frame += 1
    else:
        idle_frame = 0

    current_time = pygame.time.get_ticks()
    # Swimmer movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and swimmer_hitbox.colliderect(sub_hitbox):
        if current_time - last_attack_time > attack_cooldown:
            attacking = True

    if attacking and frame < 6:
        swimmer = pygame.image.load(f"attack/{frame}.png").convert_alpha()
        swimmer = pygame.transform.scale(swimmer, (100, 60))
        if random.randint(0, 3) == 1:
            frame += 1
        if frame == 5:
            do_attack = True
    else:
        attacking = False
        frame = 0

    if do_attack and attacking:
        sub_health -= 1
        sub_health = max(0, sub_health)
        last_attack_time = current_time
        swimmer_rect.x -= 30
        swimmer_hitbox.x -= 30
        do_attack = False

    # Spawn missiles
    if len(missiles) != 3:
        spawn_missile(3)
        for missile in missiles:
            screen.blit(missile[0], missile[1])
    else:
        for missile in missiles:
            missile[1].x -= 7.5
            missile[2].x -= 7.5
            screen.blit(missile[0], missile[1])
        if missiles[1][1].x < 0:
            missiles = []

    if keys[pygame.K_UP] and swimmer_rect.y > 0 and not attacking:
        swimmer_rect.y -= swimmer_speed
        swimmer_hitbox.y -= swimmer_speed
    if keys[pygame.K_DOWN] and swimmer_rect.y < 325 and not attacking:
        swimmer_rect.y += swimmer_speed
        swimmer_hitbox.y += swimmer_speed
    if keys[pygame.K_LEFT] and swimmer_rect.x > 0 and not attacking:
        swimmer_rect.x -= swimmer_speed
        swimmer_hitbox.x -= swimmer_speed
    if keys[pygame.K_RIGHT] and swimmer_rect.x < 700 and not attacking:
        swimmer_rect.x += swimmer_speed
        swimmer_hitbox.x += swimmer_speed

    # Missile collision
    for missile in missiles:
        if swimmer_hitbox.colliderect(missile[2]):
            numHearts -= 1
            missile[1].y = 500
            missile[2].y = 500

    # Draw health bar and swimmer
    if game_cleared:
        screen.blit(pygame.transform.scale(level_over_surf, (800, 400)), (0, 0))
        pygame.display.flip()
        pygame.time.delay(3000)  # Show cleared screen for 3 seconds
       

    show_bar(screen, sub_health, sub_max_health, sub_health_bar_rect, 'Red')
    screen.blit(swimmer, swimmer_rect)

    pygame.display.update()
    clock.tick(60)
