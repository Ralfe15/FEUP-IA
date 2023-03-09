# Game data structure representing a certain state of a LESS match
import random

BOARD_SIZE = 6
DEBUG = False


def generate_initial_state():
    # Returns a game in initial state: a 6x6 board with 4 players in top left and bottom right corners
    board = [[Tile() for _ in range(6)] for _ in range(6)]
    board[0][0] = board[0][1] = board[1][0] = board[1][1] = Tile(1)
    board[BOARD_SIZE - 1][BOARD_SIZE - 1] = board[BOARD_SIZE - 1][BOARD_SIZE - 2] = board[BOARD_SIZE - 2][
        BOARD_SIZE - 1] \
        = board[BOARD_SIZE - 2][BOARD_SIZE - 2] = Tile(2)
    return board


class Game:
    def __init__(self, players):
        self.players = players
        # Generate new game state, fresh board and random starting player
        self.state = GameState(generate_initial_state(), random.randint(1, 2))


class Tile:
    def __init__(self, value=0):
        self.value = value
        self.walls = [1 if random.randint(0,1) <= 0.3 else 0 for _ in range(4)]

    def __str__(self):
        
        return "{}".format(self.value)

    def has_wall_up(self):
        return self.walls[0]

    def has_wall_right(self):
        return self.walls[1]

    def has_wall_down(self):
        return self.walls[2]

    def has_wall_left(self):
        return self.walls[3]

    #  || _ ¯¯¯¯¯¯
    #  ¯

    

class GameState:
    # To access a (x, y) coord on the board: self.board[y][x] starting at (0,0)
    def __init__(self, board, curr_player):
        self.board = board
        self.curr_player = curr_player
        self.p1_pieces = []
        self.p2_pieces = []
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 1:
                    self.p1_pieces.append([i, j])
                elif self.board[i][j] == 2:
                    self.p2_pieces.append([i, j])

    # Get available moves for piece at coords (x, y)
    # Returns list of available moves [[(x, y), cost]]
    # Legal moves are: moving to an empty space left/right/up/down, leaping one piece to an empty space
    def get_moves(self, x, y):
        moves = []
        if x not in range(BOARD_SIZE) or y not in range(BOARD_SIZE) or self.board[x][y].value == 0:
            return []

        # Check up
        if y - 1 in range(BOARD_SIZE) and self.board[y - 1][x].value == 0:
            if DEBUG: print("move up")
            moves.append([(x, y - 1), 1])
        # Check down
        if y + 1 in range(BOARD_SIZE) and self.board[y + 1][x].value == 0:
            if DEBUG: print("move down")
            moves.append([(x, y + 1), 1])
        # Check right
        if x + 1 in range(BOARD_SIZE) and self.board[y][x + 1].value == 0:
            if DEBUG: print("move right")
            moves.append([(x + 1, y), 1])
        # Check left
        if x - 1 in range(BOARD_SIZE) and self.board[y][x - 1].value == 0:
            if DEBUG: print("move left")
            moves.append([(x - 1, y), 1])

        # Check leap up
        if y - 2 in range(BOARD_SIZE) and self.board[y - 1][x].value != 0 and self.board[y - 2][x].value == 0:
            if DEBUG: print("leap up")
            moves.append([(x, y - 2), 1])
        # Check leap down
        if y + 2 in range(BOARD_SIZE) and self.board[y + 1][x].value != 0 and self.board[y + 2][x].value == 0:
            if DEBUG: print("leap down")
            moves.append([(x, y + 2), 1])
        # Check leap right
        if x + 2 in range(BOARD_SIZE) and self.board[y][x + 1].value != 0 and self.board[y][x + 2].value == 0:
            if DEBUG: print("leap right")
            moves.append([(x + 2, y), 1])
        # Check leap left
        if x - 2 in range(BOARD_SIZE) and self.board[y][x - 1].value != 0 and self.board[y][x - 2].value == 0:
            if DEBUG: print("leap left")
            moves.append([(x - 2, y), 1])

        return moves

    def move_piece(self, xi, yi, xf, yf):
        if (xf, yf) in [move[0] for move in self.get_moves(xi, yi)]:
            self.board[yf][xf], self.board[yi][xi] = self.board[yi][xi], self.board[yf][xf]
        else:
            if DEBUG: print("INVALID MOVE")



    def print_board(self):
        # print("   0  1  2  3  4  5 --> X")z
        for i in range(len(self.board)):
            # print(i, end=" ")
            for j in self.board[i]:
                print(j, end=" ")
            print("")

