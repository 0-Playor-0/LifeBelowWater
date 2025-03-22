import pygame
import sys
import random

pygame.init()

# === CONFIGURATION ===
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
MAP_WIDTH, MAP_HEIGHT = 1600, 1200
TILE_SIZE = 40
FPS = 60
TOTAL_TIME = 30

# === COLORS ===
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
OIL_COLOR = (30, 30, 30)
BOOM_COLOR = (255, 100, 0)
PLAYER_COLOR = (0, 255, 0)
SKIMMER_COLOR = (0, 0, 0)
CLEANED_COLOR = (40, 60, 90)
BG_COLOR = (40, 60, 90)
RED = (255, 0, 0)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (90, 160, 210)
YELLOW = (255, 255, 0)

# === INIT ===
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Oil Spill Cleanup")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# === HINTS ===
hints = [
    "Protect marine life by reducing plastic use.",
    "Support sustainable fishing practices.",
    "Help keep oceans clean by participating in beach clean-ups.",
    "Learn about marine ecosystems and their importance.",
    "Advocate for policies that protect ocean habitats."
]

def get_random_hint():
    return random.choice(hints)

# === IMAGES ===
bg_image = pygame.image.load("graphics/oceanbg.png").convert()
bg_image = pygame.transform.scale(bg_image, (MAP_WIDTH, MAP_HEIGHT))
skimmer_img = pygame.image.load("graphics/skimmer.png").convert_alpha()
skimmer_img = pygame.transform.scale(skimmer_img, (50,50))
oil_spill_img = pygame.image.load("graphics/oil-removebg-preview.png").convert_alpha()
game_over_img = pygame.image.load("graphics/gameover.png").convert()
game_cleared_img = pygame.image.load("graphics/gamecleared.png").convert()
swimmer_img = pygame.image.load("graphics/swimmer.png").convert_alpha()
swimmer_img = pygame.transform.scale(swimmer_img, (80, 80))

# === TEXT FUNCTION ===
def draw_text(text, x, y, color=BLACK, size=30):
    font_custom = pygame.font.SysFont(None, size)
    rendered = font_custom.render(text, True, color)
    screen.blit(rendered, (x, y))

# === GAME STATE ===
def reset_game():
    global player_pos, boom_placed, has_skimmer, oil_patches, cleaned_patches
    global start_ticks, game_over, game_won, oil_spill_rect, boom_checkpoints
    global skimmer_rect

    player_pos = [100, 100]
    boom_placed = [False] * 4
    has_skimmer = False
    start_ticks = pygame.time.get_ticks()
    game_over = False
    game_won = False

    oil_spill_rect = pygame.Rect(MAP_WIDTH//2 - 150, MAP_HEIGHT//2 - 150, 300, 300)
    oil_spill_img_scaled = pygame.transform.scale(oil_spill_img, (oil_spill_rect.width, oil_spill_rect.height))

    boom_checkpoints = [
        pygame.Rect(oil_spill_rect.left - 30, oil_spill_rect.centery - 15, 30, 30),
        pygame.Rect(oil_spill_rect.right, oil_spill_rect.centery - 15, 30, 30),
        pygame.Rect(oil_spill_rect.centerx - 15, oil_spill_rect.top - 30, 30, 30),
        pygame.Rect(oil_spill_rect.centerx - 15, oil_spill_rect.bottom, 30, 30),
    ]

    oil_patches = []
    for _ in range(20):
        x = random.randint(oil_spill_rect.left + 10, oil_spill_rect.right - 10)
        y = random.randint(oil_spill_rect.top + 10, oil_spill_rect.bottom - 10)
        oil_patches.append(pygame.Rect(x, y, 10, 10))
    cleaned_patches = [False] * len(oil_patches)

    skimmer_rect = pygame.Rect(random.randint(100, MAP_WIDTH - 100), random.randint(100, MAP_HEIGHT - 100), 30, 30)

    return oil_spill_img_scaled

oil_spill_img = reset_game()

# === CAMERA & BUTTONS ===
camera_x, camera_y = 0, 0
retry_rect = pygame.Rect(SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 40, 120, 50)
pause_button_rect = pygame.Rect(SCREEN_WIDTH - 50, 10, 30, 30)
pause = False

# === MAIN LOOP ===
running = True
while running:
    dt = clock.tick(FPS) / 1000
    screen.blit(bg_image, (-camera_x, -camera_y))

    if not pause and not game_over:
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = max(0, TOTAL_TIME - seconds_passed)

    camera_x = max(0, min(player_pos[0] - SCREEN_WIDTH//2, MAP_WIDTH - SCREEN_WIDTH))
    camera_y = max(0, min(player_pos[1] - SCREEN_HEIGHT//2, MAP_HEIGHT - SCREEN_HEIGHT))
    player_rect = pygame.Rect(player_pos[0], player_pos[1], 80, 80)
    screen_player = player_rect.move(-camera_x, -camera_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over:
            if event.type == pygame.MOUSEBUTTONDOWN and retry_rect.collidepoint(event.pos):
                oil_spill_img = reset_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    oil_spill_img = reset_game()
                elif event.key == pygame.K_q:
                    running = False

        if event.type == pygame.MOUSEBUTTONDOWN and pause_button_rect.collidepoint(event.pos):
            pause = not pause

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and not pause:
            mx, my = event.pos
            world_mouse = (mx + camera_x, my + camera_y)
            for i, checkpoint in enumerate(boom_checkpoints):
                if not boom_placed[i] and checkpoint.collidepoint(world_mouse):
                    if player_rect.colliderect(checkpoint.inflate(40, 40)):
                        boom_placed[i] = True

    keys = pygame.key.get_pressed()
    if not game_over and not pause:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_pos[0] -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_pos[0] += 5
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_pos[1] -= 5
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_pos[1] += 5

    player_pos[0] = max(0, min(MAP_WIDTH - 30, player_pos[0]))
    player_pos[1] = max(0, min(MAP_HEIGHT - 30, player_pos[1]))

    screen.blit(oil_spill_img, oil_spill_rect.move(-camera_x, -camera_y))

    for i, checkpoint in enumerate(boom_checkpoints):
        screen_pos = checkpoint.move(-camera_x, -camera_y)
        color = BOOM_COLOR if boom_placed[i] else (255, 200, 100)
        pygame.draw.circle(screen, color, screen_pos.center, 15)

    if all(boom_placed):
        pygame.draw.rect(screen, YELLOW, oil_spill_rect.move(-camera_x - 10, -camera_y - 10).inflate(20, 20), 5, border_radius=20)
        if not has_skimmer:
            screen.blit(skimmer_img, skimmer_rect.move(-camera_x, -camera_y))
            if player_rect.colliderect(skimmer_rect):
                has_skimmer = True

    for i, patch in enumerate(oil_patches):
        world_patch = patch.move(-camera_x, -camera_y)
        if not cleaned_patches[i]:
            if has_skimmer:
                pygame.draw.circle(screen, BLACK, world_patch.center, 5)
            if has_skimmer and player_rect.colliderect(patch):
                cleaned_patches[i] = True

    screen.blit(swimmer_img, screen_player)

    if all(cleaned_patches):
        game_over = True
        game_won = True
    elif not pause and time_left <= 0:
        game_over = True

    draw_text(f"Time Left: {time_left}s", 10, 10)
    draw_text(f"Booms Placed: {sum(boom_placed)}/4", 10, 40)
    if all(boom_placed) and not has_skimmer:
        draw_text("Skimmer ready! Find it to clean!", 10, 70)
    if has_skimmer:
        draw_text("Cleaning oil...", 10, 70)

    hover_pause = pause_button_rect.collidepoint(pygame.mouse.get_pos())
    pygame.draw.rect(screen, BUTTON_HOVER if hover_pause else BUTTON_COLOR, pause_button_rect, border_radius=6)
    if pause:
        triangle = [(pause_button_rect.x + 10, pause_button_rect.y + 7),
                    (pause_button_rect.x + 10, pause_button_rect.y + 23),
                    (pause_button_rect.x + 22, pause_button_rect.y + 15)]
        pygame.draw.polygon(screen, BLACK, triangle)
        draw_text("Paused", SCREEN_WIDTH // 2 - 60, 100, BLACK, size=50)
    else:
        bar_width = 4
        gap = 6
        bar_height = 16
        bar_x = pause_button_rect.x + 8
        bar_y = pause_button_rect.y + 7
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, BLACK, (bar_x + bar_width + gap, bar_y, bar_width, bar_height))

    if game_over:
        if game_won:
            screen.blit(pygame.transform.scale(game_cleared_img, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
            draw_text(get_random_hint(), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, color=WHITE)  # Display hint
            pygame.display.flip()
            pygame.time.delay(3000)  # Show cleared screen for 3 seconds
            pygame.time.delay(5000)  # Wait for 5 seconds before transitioning
            import Level2  # Import Level2 here
            Level2.main()  # Start Level 2

        else:
            screen.blit(pygame.transform.scale(game_over_img, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        mx, my = pygame.mouse.get_pos()
        hover = retry_rect.collidepoint((mx, my))
        pygame.draw.rect(screen, BUTTON_HOVER if hover else BUTTON_COLOR, retry_rect, border_radius=8)
        draw_text("Retry", retry_rect.x + 35, retry_rect.y + 12)

    pygame.display.flip()

pygame.quit()
