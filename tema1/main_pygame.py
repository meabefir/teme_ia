import pygame
import copy

pygame.init()

from pygame_stuff.Game import Game

screen = pygame.display.set_mode([500, 500])

initialGame = Game(file="../input/input1.txt")
# initialGame = Game(rows=2, cols=2)
game = copy.deepcopy(initialGame)
clock = pygame.time.Clock()

running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        game.handleEvent(event)
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game = copy.deepcopy(initialGame)

    # Fill the background with white
    screen.fill((0, 0, 0))

    # # Draw a solid blue circle in the center
    # pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
    game.update()
    game.render(screen)

    # Flip the display
    pygame.display.flip()

    clock.tick(60)

# Done! Time to quit.
pygame.quit()