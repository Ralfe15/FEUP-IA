import menu
import game
import board
import pygame
import os
import sys

if __name__ == '__main__':

    # Initialize Pygame
    pygame.init()

    # Set the width and height of the screen [width, height]
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    FPS = 60

    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)

    # Set the title of the window
    pygame.display.set_caption("LESS")

    menu = menu.Menu(screen)

    pygame.display.update()

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Loop until the user clicks the close button
    done = False
    g1 = None
    printed = False

    # Main loop
    while not done:
        clock.tick(FPS)

        if g1 is not None and g1.state.curr_player == 2 and not printed:
            print(g1.state.minimax(3, True, True))
            printed = True

        # --- Main event loop
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu.gamemode == 0:
                    g1 = menu.update_menu(event)

                if not g1 is None:
                    menu.check_match_end(event)
                    g1.state.board.update_board(g1, event)

    # Close the window and quit.
    pygame.quit()
