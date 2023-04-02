import pygame
import game
import os
import menu
import sys

# Define colors
WHITE = (255, 255, 255)
BLACK = (80, 80, 80)
BLUE = (111,205,244)
RED = (242, 107, 102)
BASE_X = 175
BASE_Y = 45

# difference between the size of the piece and the selected piece
HALF_SIZE_DIFF = 5.2

PLAYER1 = pygame.image.load(os.path.join('assets', 'player1.png'))
PLAYER1_SELECTED = pygame.image.load(os.path.join('assets', 'player1_selected.png'))
PLAYER1_POSSIBLE_MOVE = pygame.image.load(os.path.join('assets', 'p1_possible_move.png'))
PLAYER1_USER_UNSELECTED = pygame.image.load(os.path.join('assets', 'p1_unselected.png'))
PLAYER1_USER_SELECTED = pygame.image.load(os.path.join('assets', 'p1_selected.png'))

PLAYER2 = pygame.image.load(os.path.join('assets', 'player2.png'))
PLAYER2_SELECTED = pygame.image.load(os.path.join('assets', 'player2_selected.png'))
PLAYER2_POSSIBLE_MOVE = pygame.image.load(os.path.join('assets', 'p2_possible_move.png'))
PLAYER2_USER_UNSELECTED = pygame.image.load(os.path.join('assets', 'p2_unselected.png'))
PLAYER2_USER_SELECTED = pygame.image.load(os.path.join('assets', 'p2_selected.png'))

BACK_ARROW = pygame.image.load(os.path.join('assets', 'back_arrow.png'))

BLANK_TILE = pygame.image.load(os.path.join('assets', 'blank_tile.png'))

RIGHT_WALL = pygame.image.load(os.path.join('assets', 'wall.png'))
DOWN_WALL = pygame.transform.rotate(RIGHT_WALL, 270)
LEFT_WALL = pygame.transform.rotate(RIGHT_WALL, 180)
UP_WALL = pygame.transform.rotate(RIGHT_WALL, 90)


class Board:
    def __init__(self, screen, board_size=6):
        self.screen = screen
        self.menu = menu
        self.p1_pieces = []
        self.p2_pieces = []

        self.FONT = pygame.font.SysFont('arialBlack', 30)

        self.BOARD_SIZE = board_size

        self.board = [[0 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]

        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):

                x = i * 115 + BASE_X
                y = j * 115 + BASE_Y
                WIDTH = 109
                HEIGHT = 109

                if (i == 0 and j == 0) or (i == 0 and j == 1) or (i == 1 and j == 0) or (i == 1 and j == 1):
                    tile = game.Tile(1, (i, j), pygame.Rect(x, y, WIDTH, HEIGHT))
                    self.board[i][j] = tile
                    self.p1_pieces.append(tile)
                elif (i == self.BOARD_SIZE - 2 and j == self.BOARD_SIZE - 2) or (
                        i == self.BOARD_SIZE - 2 and j == self.BOARD_SIZE - 1) or (
                        i == self.BOARD_SIZE - 1 and j == self.BOARD_SIZE - 2) or (
                        i == self.BOARD_SIZE - 1 and j == self.BOARD_SIZE - 1):
                    tile = game.Tile(2, (i, j), pygame.Rect(x, y, WIDTH, HEIGHT))
                    self.board[i][j] = tile
                    self.p2_pieces.append(tile)
                else:
                    self.board[i][j] = game.Tile(0, (i, j), pygame.Rect(x, y, WIDTH, HEIGHT))

    def draw_window(self, game=None, selected_tile=False):

        possible_moves = []

        if selected_tile:
            possible_moves = game.state.get_moves_for_tile(selected_tile)
            possible_moves = [i[0] for i in possible_moves]

        self.screen.fill(WHITE)

        #Draw back arrow
        back_arrow_rect = BACK_ARROW.get_rect()
        back_arrow_rect.center = (30, 40)
        self.screen.blit(BACK_ARROW, back_arrow_rect)

        #Draw player icons
        if game.state.curr_player == 1:
            self.screen.blit(PLAYER1_USER_SELECTED, (40, 90))
            self.screen.blit(PLAYER2_USER_UNSELECTED, (890, 550))
            credits = self.FONT.render(f"{game.state.move_credits} / 3", True, RED)
            self.screen.blit(credits, (50, 200))
        else:
            self.screen.blit(PLAYER1_USER_UNSELECTED, (40, 90))
            self.screen.blit(PLAYER2_USER_SELECTED, (890, 550))
            credits = self.FONT.render(f"{game.state.move_credits} / 3", True, BLUE)
            self.screen.blit(credits, (900, 660))

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                x = i * 115 + BASE_X
                y = j * 115 + BASE_Y

                self.screen.blit(BLANK_TILE, (x, y))

                if self.board[i][j].walls[0] == 1:
                    self.screen.blit(UP_WALL, (x, y))

                if self.board[i][j].walls[1] == 1:
                    self.screen.blit(RIGHT_WALL, (x, y))

                if self.board[i][j].walls[2] == 1:
                    self.screen.blit(DOWN_WALL, (x, y))

                if self.board[i][j].walls[3] == 1:
                    self.screen.blit(LEFT_WALL, (x, y))

                if self.board[i][j].value == 1:
                    if self.board[i][j].selected:
                        self.screen.blit(PLAYER1_SELECTED, (x + 27 - HALF_SIZE_DIFF, y + 27 - HALF_SIZE_DIFF))
                    else:
                        self.screen.blit(PLAYER1, (x + 27, y + 27))

                if self.board[i][j].value == 2:
                    if self.board[i][j].selected:
                        self.screen.blit(PLAYER2_SELECTED, (x + 27 - HALF_SIZE_DIFF, y + 27 - HALF_SIZE_DIFF))
                    else:
                        self.screen.blit(PLAYER2, (x + 27, y + 27))

                if self.board[i][j] in possible_moves:
                    if selected_tile.value == 1:
                        self.screen.blit(PLAYER1_POSSIBLE_MOVE, (x + 27, y + 27))
                    else:
                        self.screen.blit(PLAYER2_POSSIBLE_MOVE, (x + 27, y + 27))

        pygame.display.update()

    def tile_clicked(self, event):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j].rect.collidepoint(event.pos):
                    return self.board[i][j]

        return None

    def get_selected_tile(self):
        for i in range(len(self.p1_pieces)):

            if self.p1_pieces[i].selected:
                return self.p1_pieces[i]

            elif self.p2_pieces[i].selected:
                return self.p2_pieces[i]

        return False

    def update_board(self, game, event):

        tile = self.tile_clicked(event)
        if not tile: return

        if game.state.game_over != 0: return

        if game.state.curr_player == 1:
            if tile in self.p1_pieces:
                for i in self.p1_pieces:
                    if i != tile:
                        i.selected = False
                    else:
                        i.selected = not i.selected

        if game.state.curr_player == 2:
            if tile in self.p2_pieces:
                for i in self.p2_pieces:
                    if i != tile:
                        i.selected = False
                    else:
                        i.selected = not i.selected

        selected_tile = self.get_selected_tile()

        if selected_tile:
            possible_moves = game.state.get_moves_for_tile(selected_tile)
            possible_tiles = [i[0] for i in possible_moves]

            if tile in possible_tiles:
                for k in possible_moves:
                    if k[0] == tile:
                        cost = k[1]
                game.state.move_piece(selected_tile.index[0], selected_tile.index[1], tile.index[0], tile.index[1],
                                      cost)
                game.state.is_game_over()
                selected_tile.selected = False

        self.draw_window(game, selected_tile)
