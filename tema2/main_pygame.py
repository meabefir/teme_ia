import pygame
import copy

from pygame_stuff.Game import Game

pygame.init()

screen = pygame.display.set_mode([750, 750])
pygame.display.set_caption("Twelve men's morris - Huja Petru")

game = Game(screen.get_size()[0])
clock = pygame.time.Clock()

running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        game.handle_event(event)
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game = Game(screen.get_size()[0])

    # Fill the background with white
    screen.fill((255, 255, 255))

    game.update()
    game.render(screen)

    # Flip the display
    pygame.display.flip()

    clock.tick(60)

# Done! Time to quit.
pygame.quit()