# Game data structure representing a certain state of a LESS match
import random

BOARD_SIZE = 6
DEBUG = True
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
MOVE_CREDITS = 3


# def generate_initial_state():
#     # Returns a game in initial state: a 6x6 board with 4 players in top left and bottom right corners
#     board = [[Tile() for _ in range(6)] for _ in range(6)]
#     for i in range(2):
#         for j in range(2):
#             board[i][j] = Tile(1)
#             board[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - j] = Tile(2)
#     return board

class Game:
    def __init__(self, players, board):
        self.players = players
        # Generate new game state, fresh board and random starting player
        # TODO: REPLACE W random.randint(1, 2)
        self.state = GameState(board, 1)


class Tile:
    def __init__(self, value=0, index=(0, 0), rect=None):
        self.value = value
        self.walls = [1 if random.randint(
            0, 9) <= 2 else 0 for _ in range(4)]
        self.selected = False
        self.index = index
        self.rect = rect

    def __str__(self):
        return f"{self.value}"

    def has_wall_up(self):
        return self.walls[0]

    def has_wall_right(self):
        return self.walls[1]

    def has_wall_down(self):
        return self.walls[2]

    def has_wall_left(self):
        return self.walls[3]


class GameState:
    def __init__(self, board, curr_player, move_credits=3):
        self.board = board
        self.curr_player = curr_player
        self.move_credits = move_credits
        self.game_over = 0  # 0 = game not over, 1 = player 1 wins, 2 = player 2 wins
    """
    Get available moves for piece at coords (x, y)
    Returns list of available moves [[(x, y), cost]]
    Legal moves are: moving to an empty space left/right/up/down, leaping one piece to an empty space
    """

    def get_moves_by_cost(self, x, y, cost):
        moves = []

        if x not in range(BOARD_SIZE) or y not in range(BOARD_SIZE) or self.board.board[x][y].value == 0:
            return []

        self.get_valid_adjacent_moves_with_walls(y, x, moves)
        return self.get_valid_leap_moves_with_cost(y, x, moves, cost)

    def is_valid_position(self, x, y):
        """
        Given a position (x,y), returns True if it's within the board, False otherwise.
        """
        return x in range(BOARD_SIZE) and y in range(BOARD_SIZE)

    def is_valid_starting_point(self, x, y):
        """
        Given a position (x,y), returns True if it's a valid starting point for a move (value != 0), False otherwise.
        """
        return self.board.board[x][y].value != 0

    def get_valid_simple_moves(self, x, y, cost):
        """
        Given a position (x,y) and a cost, returns all possible valid simple moves from that position with that specific cost.
        """
        moves = []

        self.get_valid_adjacent_moves_with_walls(y, x, moves)
        # Return only the moves with the desired cost
        return [move for move in moves if move[1] == cost]

    def get_valid_adjacent_moves_with_walls(self, y, x, moves):
        if y - 1 in range(BOARD_SIZE) and self.board.board[x][y - 1].value == 0:
            moves.append([(x, y - 1), self.check_walls_simple_move(x, y, UP)])
        if y + 1 in range(BOARD_SIZE) and self.board.board[x][y + 1].value == 0:
            moves.append(
                [(x, y + 1), self.check_walls_simple_move(x, y, DOWN)])
        if x + 1 in range(BOARD_SIZE) and self.board.board[x + 1][y].value == 0:
            moves.append(
                [(x + 1, y), self.check_walls_simple_move(x, y, RIGHT)])
        if x - 1 in range(BOARD_SIZE) and self.board.board[x - 1][y].value == 0:
            moves.append(
                [(x - 1, y), self.check_walls_simple_move(x, y, LEFT)])

    def get_valid_leap_moves(self, x, y, cost):
        """
        Given a position (x,y) and a cost, returns all possible valid leap moves from that position with that specific cost.
        """
        moves = []

        return self.get_valid_leap_moves_with_cost(y, x, moves, cost)

    def get_valid_leap_moves_with_cost(self, y, x, moves, cost):
        """
        This function is used to identify valid leap moves on a board for a given position and cost. 
        A leap move is a move where a piece jumps over another piece to an empty square on the board.
        The function checks for leap moves in all four directions (up, down, left, right) 
        and returns a list of all valid leap moves with the given cost. 
        The function uses the check_can_leap method to determine if a piece can leap over another piece,
        and only considers moves where the destination square is empty.
        """
        if (
            y - 2 in range(BOARD_SIZE)
            and self.board.board[x][y - 1].value != 0
            and self.board.board[x][y - 2].value == 0
            and self.check_can_leap(x, y, UP)
        ):
            moves.append([(x, y - 2), 1])
        if (
            y + 2 in range(BOARD_SIZE)
            and self.board.board[x][y + 1].value != 0
            and self.board.board[x][y + 2].value == 0
            and self.check_can_leap(x, y, DOWN)
        ):
            moves.append([(x, y + 2), 1])
        if (
            x + 2 in range(BOARD_SIZE)
            and self.board.board[x + 1][y].value != 0
            and self.board.board[x + 2][y].value == 0
            and self.check_can_leap(x, y, RIGHT)
        ):
            moves.append([(x + 2, y), 1])
        if (
            x - 2 in range(BOARD_SIZE)
            and self.board.board[x - 1][y].value != 0
            and self.board.board[x - 2][y].value == 0
            and self.check_can_leap(x, y, LEFT)
        ):
            moves.append([(x - 2, y), 1])
        return [move for move in moves if move[1] == cost]


    def get_moves_for_tile(self, tile):
        all_moves = [self.get_moves_by_cost(tile.index[0], tile.index[1], 1)]
        if self.move_credits >= 2:
            all_moves.append(self.get_moves_by_cost(
                tile.index[0], tile.index[1], 2))
        if self.move_credits == 3:
            all_moves.append(self.get_moves_by_cost(
                tile.index[0], tile.index[1], 3))
        possible_moves = []

        for i in all_moves:
            if len(i) >= 1:
                for j in i:
                    tile = self.board.board[j[0][0]][j[0][1]]
                    possible_moves.append((tile, j[1]))

        return possible_moves

    def move_piece(self, xi, yi, xf, yf, cost=0,player =None):
        self.move_credits -= cost
        self.board.board[xf][yf].value = self.board.board[xi][yi].value
        self.board.board[xi][yi].value = 0

        if self.curr_player == 1 or player == 1:
            self.board.p1_pieces.remove(self.board.board[xi][yi])
            self.board.p1_pieces.append(self.board.board[xf][yf])
        else:
            self.board.p2_pieces.remove(self.board.board[xi][yi])
            self.board.p2_pieces.append(self.board.board[xf][yf])

        if self.move_credits == 0:
            if player is None:
                self.curr_player = 1 if self.curr_player == 2 else 2
            self.move_credits = MOVE_CREDITS
        self.is_game_over()
        # new_board = copy.deepcopy(self.board)
        # new_board.board[yf][xf],new_board.board[yi][xi] = self.board.board[yi][xi], self.board.board[yf][xf]
        # return GameState(new_board, self.curr_player)

    def is_game_over(self):
        p1_corner = [(0, 0), (0, 1), (1, 0), (1, 1)]
        p2_corner = [(BOARD_SIZE - 1, BOARD_SIZE - 1), (BOARD_SIZE - 1, BOARD_SIZE - 2),
                     (BOARD_SIZE - 2, BOARD_SIZE - 1), (BOARD_SIZE - 2, BOARD_SIZE - 2)]

        if all(coord.index in p2_corner for coord in self.board.p1_pieces):
            self.game_over = 1
        elif all(coord.index in p1_corner for coord in self.board.p2_pieces):
            self.game_over = 2

    def check_walls_simple_move(self, source_x, source_y, direction):
        cost = 1
        if direction == UP:
            if self.board.board[source_x][source_y].has_wall_up():
                cost += 1
            if self.board.board[source_x][source_y - 1].has_wall_down():
                cost += 1
        if direction == DOWN:
            if self.board.board[source_x][source_y].has_wall_down():
                cost += 1
            if self.board.board[source_x][source_y + 1].has_wall_up():
                cost += 1
        if direction == LEFT:
            if self.board.board[source_x][source_y].has_wall_left():
                cost += 1
            if self.board.board[source_x - 1][source_y].has_wall_right():
                cost += 1
        if direction == RIGHT:
            if self.board.board[source_x][source_y].has_wall_right():
                cost += 1
            if self.board.board[source_x + 1][source_y].has_wall_left():
                cost += 1
        return cost

    def check_can_leap(self, source_x, source_y, direction):
        if direction == UP:
            return not (self.board.board[source_x][source_y].has_wall_up() or  # Current tile has wall up
                        # Middle tile has wall down
                        self.board.board[source_x][source_y - 1].has_wall_down() or
                        # Middle tile has wall up
                        self.board.board[source_x][source_y - 1].has_wall_up() or
                        # Destination tile has wall down
                        self.board.board[source_x][source_y - \
                                                   2].has_wall_down()
                        )
        if direction == DOWN:
            return not (self.board.board[source_x][source_y].has_wall_down() or
                        self.board.board[source_x][source_y + 1].has_wall_down() or
                        self.board.board[source_x][source_y + 1].has_wall_up() or
                        self.board.board[source_x][source_y + 2].has_wall_up()
                        )
        if direction == LEFT:
            return not (self.board.board[source_x][source_y].has_wall_left() or
                        self.board.board[source_x - 1][source_y].has_wall_left() or
                        self.board.board[source_x - 1][source_y].has_wall_right() or
                        self.board.board[source_x -
                                         2][source_y].has_wall_right()
                        )
        if direction == RIGHT:
            return not (self.board.board[source_x][source_y].has_wall_right() or
                        self.board.board[source_x + 1][source_y].has_wall_right() or
                        self.board.board[source_x + 1][source_y].has_wall_left() or
                        self.board.board[source_x +
                                         2][source_y].has_wall_left()
                        )

    def print_board(self):
        # print("   0  1  2  3  4  5 --> X")z
        for i in range(len(self.board.board)):
            # print(i, end=" ")
            for j in self.board.board[i]:
                print(j.value, end=" ")
            print("")
