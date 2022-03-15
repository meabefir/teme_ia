import pygame

pygame.init()

from pygame_stuff.Game import Game

screen = pygame.display.set_mode([500, 500])

game = Game()
clock = pygame.time.Clock()

running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        game.handleEvent(event)

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