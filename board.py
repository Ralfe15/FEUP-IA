import time
import pygame
import game
import os
import menu

# Define colors
WHITE = (255, 255, 255)
BLACK = (80, 80, 80)
BLUE = (111, 205, 244)
RED = (242, 107, 102)
BASE_X = 175
BASE_Y = 45

# difference between the size of the piece and the selected piece
HALF_SIZE_DIFF = 5.2

PLAYER1 = pygame.image.load(os.path.join('assets', 'player1.png'))
PLAYER1_SELECTED = pygame.image.load(
    os.path.join('assets', 'player1_selected.png'))
PLAYER1_POSSIBLE_MOVE = pygame.image.load(
    os.path.join('assets', 'p1_possible_move.png'))
PLAYER1_USER_UNSELECTED = pygame.image.load(
    os.path.join('assets', 'p1_unselected.png'))
PLAYER1_USER_SELECTED = pygame.image.load(
    os.path.join('assets', 'p1_selected.png'))

PLAYER2 = pygame.image.load(os.path.join('assets', 'player2.png'))
PLAYER2_SELECTED = pygame.image.load(
    os.path.join('assets', 'player2_selected.png'))
PLAYER2_POSSIBLE_MOVE = pygame.image.load(
    os.path.join('assets', 'p2_possible_move.png'))
PLAYER2_USER_UNSELECTED = pygame.image.load(
    os.path.join('assets', 'p2_unselected.png'))
PLAYER2_USER_SELECTED = pygame.image.load(
    os.path.join('assets', 'p2_selected.png'))

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

        self.board = [[0 for _ in range(self.BOARD_SIZE)]
                      for _ in range(self.BOARD_SIZE)]

        WIDTH = 109
        HEIGHT = 109

        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):

                x = i * 115 + BASE_X
                y = j * 115 + BASE_Y
                if (i == 0 and j == 0) or (i == 0 and j == 1) or (i == 1 and j == 0) or (i == 1 and j == 1):
                    tile = game.Tile(
                        1, (i, j), pygame.Rect(x, y, WIDTH, HEIGHT))
                    self.board[i][j] = tile
                    self.p1_pieces.append(tile)
                elif (i == self.BOARD_SIZE - 2 and j == self.BOARD_SIZE - 2) or (
                        i == self.BOARD_SIZE - 2 and j == self.BOARD_SIZE - 1) or (
                        i == self.BOARD_SIZE - 1 and j == self.BOARD_SIZE - 2) or (
                        i == self.BOARD_SIZE - 1 and j == self.BOARD_SIZE - 1):
                    tile = game.Tile(
                        2, (i, j), pygame.Rect(x, y, WIDTH, HEIGHT))
                    self.board[i][j] = tile
                    self.p2_pieces.append(tile)
                else:
                    self.board[i][j] = game.Tile(
                        0, (i, j), pygame.Rect(x, y, WIDTH, HEIGHT))

    def draw_window(self, game=None, selected_tile=False):

        possible_moves = []

        if selected_tile:
            possible_moves = game.state.get_moves_for_tile(selected_tile)
            possible_moves = [i[0] for i in possible_moves]

        self.screen.fill(WHITE)

        # Draw back arrow
        back_arrow_rect = BACK_ARROW.get_rect()
        back_arrow_rect.center = (30, 40)
        self.screen.blit(BACK_ARROW, back_arrow_rect)

        # Draw player icons
        if game.state.curr_player == 1:
            self.screen.blit(PLAYER1_USER_SELECTED, (40, 90))
            self.screen.blit(PLAYER2_USER_UNSELECTED, (890, 550))
            credits = self.FONT.render(
                f"{game.state.move_credits} / 3", True, RED)
            self.screen.blit(credits, (50, 200))
        else:
            self.screen.blit(PLAYER1_USER_UNSELECTED, (40, 90))
            self.screen.blit(PLAYER2_USER_SELECTED, (890, 550))
            credits = self.FONT.render(
                f"{game.state.move_credits} / 3", True, BLUE)
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
                        self.screen.blit(
                            PLAYER1_SELECTED, (x + 27 - HALF_SIZE_DIFF, y + 27 - HALF_SIZE_DIFF))
                    else:
                        self.screen.blit(PLAYER1, (x + 27, y + 27))

                if self.board[i][j].value == 2:
                    if self.board[i][j].selected:
                        self.screen.blit(
                            PLAYER2_SELECTED, (x + 27 - HALF_SIZE_DIFF, y + 27 - HALF_SIZE_DIFF))
                    else:
                        self.screen.blit(PLAYER2, (x + 27, y + 27))

                if self.board[i][j] in possible_moves:
                    if selected_tile.value == 1:
                        self.screen.blit(
                            PLAYER1_POSSIBLE_MOVE, (x + 27, y + 27))
                    else:
                        self.screen.blit(
                            PLAYER2_POSSIBLE_MOVE, (x + 27, y + 27))

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
        """
        Updates the game board based on user's input or ai's selection.
        """
        if game.state.game_over != 0:
            return
        if tile := self.tile_clicked(event):
            self.select_or_deselect_tiles(game, tile)
            selected_tile = False
            self.make_move(game, tile, selected_tile)

    def update_board_ai(self, game, tile):
            """
            Updates the game board based on user's input or ai's selection.
            """
            if game.state.game_over != 0:
                return
            else:
                selected_tile = False;            #selected_tile = self.get_selected_tile()
            if tile:
                self.select_or_deselect_tiles(game, tile)
                self.make_move(game, tile, selected_tile)
    def ai_tile_selection(self, game,best_moves,menu):
        """
        Selects a ai tile and moves to one of its possible positions.
        """
        pieces = self.p1_pieces if game.state.curr_player == 1 else self.p2_pieces
        #while there is some movement
        while best_moves:
            #for every piece
            for piece in pieces:
                #if present pos is equal to some piece go on
                if best_moves[0][0] == piece.index :
                    #now check if this position
                    for possible_move in game.state.get_moves_for_tile(piece):
                        if (isinstance(possible_move, int)):
                            continue
                        if  best_moves[0][1] == possible_move[0].index:
                                time.sleep(0.5)
                                self.select_or_deselect_tiles(game, possible_move[0])
                                self.make_move(game, possible_move[0], piece)
                                #self.select_or_deselect_tiles(game, best_moves[0][0])
                                menu.check_match_ended()
                                self.update_board_ai(game,possible_move[0])
                                best_moves.pop(0)
                                if len(best_moves) == 0:return
                                break
            
    def select_or_deselect_tiles(self, game, tile):
        """
        Selects/Deselects tiles for movement.
        """
        if game.state.curr_player == 1 and tile in self.p1_pieces:
            for i in self.p1_pieces:
                i.selected = False if i != tile else not i.selected
        elif game.state.curr_player == 2 and tile in self.p2_pieces:
            for i in self.p2_pieces:
                i.selected = False if i != tile else not i.selected
  
    def make_move(self, game, tile, selected_tile = False):
        """
        Moves the piece from selected tile to a valid tile.
        """
        
        if (
            game.players != 1 or game.state.curr_player != 2
        ) and game.players != 0:
            selected_tile = self.get_selected_tile()


        if selected_tile:
            possible_moves = game.state.get_moves_for_tile(selected_tile)
            possible_tiles = [i[0] for i in possible_moves]

            if tile in possible_tiles:
                for move in possible_moves:
                    if move[0] == tile:
                        cost = move[1]
                game.state.move_piece(selected_tile.index[0], selected_tile.index[1],
                                      tile.index[0], tile.index[1], cost)
                game.state.is_game_over()
                selected_tile.selected = False

        self.draw_window(game, selected_tile)
