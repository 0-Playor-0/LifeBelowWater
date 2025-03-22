import pygame
import random
import sys

class LevelBossFight:



    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 400))
        pygame.display.set_caption("Level Three")
        self.clock = pygame.time.Clock()

        # Game Control
        self.game_over = False
        self.sub_health = 100
        self.sub_max_health = 100
        self.sub_health_bar_rect = pygame.Rect(320, 125, 160, 15)

        self.score_font = pygame.font.Font('Pixeltype.ttf', 20)

        # Resources
        self.bg = pygame.transform.scale(pygame.image.load('bossbg.png').convert(), (800, 400))
        self.sub_image = pygame.transform.scale(pygame.image.load("sub.png").convert_alpha(), (200, 200))
        self.sub_rect = self.sub_image.get_rect(center=(400, 200))
        self.sub_hitbox = pygame.Rect(300, 150, 180, 100)


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.sub_image, self.sub_rect)  # Draw the submarine


            # Update score display
            score_surf = self.score_font.render(f'Score: {self.score}', True, 'White')
            self.screen.blit(score_surf, (10, 10))

            pygame.display.update()
            self.clock.tick(60)

def main():
    LevelBossFight().run()  # Start the boss fight level


if __name__ == "__main__":
    main()
