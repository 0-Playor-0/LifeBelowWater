import pygame
import random 

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

class LevelOne:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((711, 400))
        pygame.display.set_caption("Level One")
        self.clock = pygame.time.Clock()
        
        # Score
        self.score = 0
        self.game_over = False
        self.game_paused = False
        self.score_font = pygame.font.Font('Pixeltype.ttf', 20)

        # Resources
        self.bg = pygame.transform.scale(pygame.image.load('graphics/bg.png').convert(), (711, 400))
        self.game_over_surf = pygame.transform.scale(pygame.image.load('graphics/over.png').convert(), (711, 400))
        self.level_over_surf = pygame.transform.scale(pygame.image.load('graphics/clear.png').convert(), (711, 400))

        self.bottles_rect = []
        self.numBottle = 3
        self.bottle_speed = 2
        self.fish = pygame.transform.scale(pygame.image.load('graphics/fish.png').convert_alpha(), (44, 26))
        self.fish_rect = self.fish.get_rect(bottomright=(200, 300))

        self.spawn_bottles()

    def spawn_bottles(self):
        for _ in range(self.numBottle):
            bottle = pygame.transform.scale(pygame.image.load('graphics/bottle.png').convert_alpha(), (25, 50))
            bottle_rect = bottle.get_rect(center=(random.randint(200, 700), 175))
            self.bottles_rect.append(bottle_rect)
    
    def draw_text(self,text, x, y, color="Black", size=30):
        font_custom = pygame.font.SysFont(None, size)
        rendered = font_custom.render(text, True, color)
        self.screen.blit(rendered, (x, y))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.screen.blit(self.bg, (0, 0))
            if not self.game_over and not self.game_paused:
                self.update_bottles()
                self.handle_input()
                for bottle_rect in self.bottles_rect:
                    self.screen.blit(pygame.transform.scale(pygame.image.load('graphics/bottle.png').convert_alpha(), (25, 50)), bottle_rect)
                self.screen.blit(self.fish, self.fish_rect)

                # Update score
                self.score += 0.01  # Increment score over time

                score_surf = self.score_font.render(f'Score : {int(self.score)}', False, 'Red')
                self.screen.blit(score_surf, (600, 50))

                # Collision detection
                for bottle_rect in self.bottles_rect:
                    if self.fish_rect.colliderect(bottle_rect):
                        self.game_over = True  # End game on collision
                        self.screen.blit(self.game_over_surf, (0, 0))  # Show game over screen
                        pygame.display.flip()  # Update the display
                        while self.game_over:  # Wait for user input to restart
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                    self.restart_game()  # Restart the game
                        break

                if self.score > 50:
                    self.screen.blit(self.level_over_surf, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(3000)  # Show cleared screen for 3 seconds
                    pygame.time.delay(5000)  # Wait for 5 seconds before transitioning
                    import Level3  # Import Level3 here
                    Level3.main()  # Start Level 3
                    draw_text(get_random_hint(), 355, 300, color=WHITE)  # Display hint

            pygame.display.update()
            self.clock.tick(60)

    def update_bottles(self):
        for bottle_rect in self.bottles_rect:
            bottle_rect.y += self.bottle_speed + random.randint(-1, 1)
            if bottle_rect.y > 350:
                bottle_rect.y = 175
                bottle_rect.x = random.randint(200, 700)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.fish_rect.y > 200:
            self.fish_rect.y -= 2.5
        if keys[pygame.K_DOWN] and self.fish_rect.y < 375:
            self.fish_rect.y += 2.5
        if keys[pygame.K_LEFT] and self.fish_rect.x > 0:
            self.fish_rect.x -= 2.5
        if keys[pygame.K_RIGHT] and self.fish_rect.x < 670:
            self.fish_rect.x += 2.5
        if keys[pygame.K_ESCAPE]:
            if keys[pygame.K_9]:  # Check for the '9' key press
                self.score = 100  # Set score to a high value to complete the level
                self.game_over = True  # Trigger game over state

        if keys[pygame.K_9]:  # Check for the '9' key press
            self.score = 100  # Set score to a high value to complete the level
            self.game_over = True  # Trigger game over state

            self.game_paused = not self.game_paused



    def restart_game(self):
        self.score = 0
        self.game_over = False
        self.bottles_rect.clear()  # Clear existing bottles
        self.spawn_bottles()  # Spawn new bottles

def main():
    LevelOne().run()

if __name__ == "__main__":
    main()
