import menu
import game
import board
import pygame
import os
import sys
from minimax.minimax import minimax

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
    _event = None
    # Main loop
    while not done:
        clock.tick(FPS)
        # --- Main event loop
        if g1 is not None and ((
            g1.players == 1 and g1.state.curr_player == 2
        ) or g1.players == 0):
            _, best_moves = minimax(menu.difficulty_selected, True, alpha=float(
                '-inf'), beta=float('inf'), game=g1)
            g1.state.board.ai_tile_selection(g1, best_moves)
            menu.check_match_end(_event)
            g1.state.board.update_board(g1, _event)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                _event = event
                if menu.gamemode == 0:
                    g1 = menu.update_menu(event)
                if g1 is not None:
                    menu.check_match_end(event)
                    g1.state.board.update_board(g1, event)

    # Close the window and quit.
    pygame.quit()
