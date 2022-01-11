from Game import *
import pygame
pygame.init()

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()

"""

screen = pygame.display.set_mode((800, 800))
running = True

image = pygame.image.load("ball.png").convert()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(image, (0, 0))

    pygame.display.flip()

pygame.quit()

"""