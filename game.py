# Game data structure representing a certain state of a LESS match
import copy
import random
import board

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

def manhattan_distance(coords_piece, player):
    if player == 2:
        return coords_piece[0] + coords_piece[1]
    elif player == 1:
        return (BOARD_SIZE - 1 - coords_piece[0]) + (BOARD_SIZE - 1 - coords_piece[1])


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
        """
        Given a position (x,y) and a cost, returns all possible valid moves from that position with that specific cost.
        """
        moves = []

        # Return empty list if position is invalid or if it's not a valid starting point (value == 0)
        if not self.is_valid_position(x, y) or not self.is_valid_starting_point(x, y):
            return []

        # Add valid moves with cost to the moves list
        moves += self.get_valid_simple_moves(x, y, cost)
        moves += self.get_valid_leap_moves(x, y, cost)

        return moves

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

        # Check up
        if y - 1 in range(BOARD_SIZE) and self.board.board[x][y - 1].value == 0:
            moves.append([(x, y - 1), self.check_walls_simple_move(x, y, UP)])

        # Check down
        if y + 1 in range(BOARD_SIZE) and self.board.board[x][y + 1].value == 0:
            moves.append(
                [(x, y + 1), self.check_walls_simple_move(x, y, DOWN)])

        # Check right
        if x + 1 in range(BOARD_SIZE) and self.board.board[x + 1][y].value == 0:
            moves.append(
                [(x + 1, y), self.check_walls_simple_move(x, y, RIGHT)])

        # Check left
        if x - 1 in range(BOARD_SIZE) and self.board.board[x - 1][y].value == 0:
            moves.append(
                [(x - 1, y), self.check_walls_simple_move(x, y, LEFT)])

        # Return only the moves with the desired cost
        return [move for move in moves if move[1] == cost]

    def get_valid_leap_moves(self, x, y, cost):
        """
        Given a position (x,y) and a cost, returns all possible valid leap moves from that position with that specific cost.
        """
        moves = []

        # Check leap up
        if y - 2 in range(BOARD_SIZE) and self.board.board[x][y - 1].value != 0 and self.board.board[x][y - 2].value == 0 and self.check_can_leap(x, y, UP):
            moves.append([(x, y - 2), 1])

        # Check leap down
        if y + 2 in range(BOARD_SIZE) and self.board.board[x][y + 1].value != 0 and self.board.board[x][y + 2].value == 0 and self.check_can_leap(x, y, DOWN):
            moves.append([(x, y + 2), 1])

        # Check leap right
        if x + 2 in range(BOARD_SIZE) and self.board.board[x + 1][y].value != 0 and self.board.board[x + 2][y].value == 0 and self.check_can_leap(x, y, RIGHT):
            moves.append([(x + 2, y), 1])

        # Check leap left
        if x - 2 in range(BOARD_SIZE) and self.board.board[x - 1][y].value != 0 and self.board.board[x - 2][y].value == 0 and self.check_can_leap(x, y, LEFT):
            moves.append([(x - 2, y), 1])

        # Return only the moves with the desired cost
        return [move for move in moves if move[1] == cost]

    def minimax(self, depth, max_player):
        if depth == 0 or self.state.game_over != 0:
            return self.evaluate(self.curr_player)

        best_move = None
        if max_player:
            maxEval = float('-inf')
            for move in self.get_terminal_states(1):
                evaluation = self.minimax(depth-1, False)[0]
                maxEval = max(maxEval, evaluation)
                if maxEval < evaluation:
                    maxEval = evaluation
                    best_move = move
            return maxEval, best_move
        else:
            minEval = float('inf')
            for move in self.get_terminal_states(2):
                evaluation = self.minimax(move, depth-1, True)[0]
                minEval = min(minEval, evaluation)
                if minEval > evaluation:
                    minEval = evaluation
                    best_move = move
            return minEval, best_move


    def get_all_moves(self, player):
        all_moves = {}
        if player == 1:
            for tile in self.board.p1_pieces:
                self.get_all_moves_for_tile(tile, all_moves)
        elif player == 2:
            for tile in self.board.p2_pieces:
                self.get_all_moves_for_tile(tile, all_moves)
        return all_moves

    def get_all_moves_for_tile(self, tile, all_moves):
        # All possible moves with associated cost for player 1
        all_moves[tile.index] = self.get_moves_by_cost(
            tile.index[0], tile.index[1], 1)
        if self.move_credits >= 2:
            all_moves[tile.index] += self.get_moves_by_cost(
                tile.index[0], tile.index[1], 2)
        if self.move_credits == 3:
            all_moves[tile.index] += self.get_moves_by_cost(
                tile.index[0], tile.index[1], 3)

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

    def get_terminal_states(self, player):
        """
        Returns a list of move sequences that use all 3 "move credits" for the given player.
        """
        move_sequences = []
        moves = self.get_all_moves(player)

        for piece_coordinate, piece_moves in moves.items():
            for move in piece_moves:
                if move[1] == 3:
                    # If move is a 3 cost, we are in a terminal state
                    move_sequences.append(
                        [(piece_coordinate[0], piece_coordinate[1]), (move[0][0], move[0][1])])

                elif move[1] == 2:
                    intermediate_move = [
                        (piece_coordinate[0], piece_coordinate[1]), (move[0][0], move[0][1])]
                    new_moves = self.explore_one_cost_moves(
                        piece_coordinate, move[0], player)
                    move_sequences.extend(self.generate_move_sequences(
                        intermediate_move, new_moves, player))

                elif move[1] == 1:
                    intermediate_move = [
                        (piece_coordinate[0], piece_coordinate[1]), (move[0][0], move[0][1])]
                    new_moves = self.explore_two_and_one_cost_moves(
                        piece_coordinate, move[0], player)
                    move_sequences.extend(self.generate_move_sequences(
                        intermediate_move, new_moves, player))

        return move_sequences

    def explore_one_cost_moves(self, piece_coordinate, move, player):
        """
        Explores all possible one cost moves from the current move.
        """
        self.move_piece(piece_coordinate[0],
                        piece_coordinate[1], move[0], move[1])
        new_moves = self.get_all_moves(player)
        one_cost_moves = {}
        for new_piece_coordinate, moves in new_moves.items():
            for new_move in moves:
                if new_move[1] == 1:
                    one_cost_moves[(new_piece_coordinate[0], new_piece_coordinate[1])] = (
                        (new_move[0][0], new_move[0][1]), new_move[1])

        self.move_piece(move[0], move[1],
                        piece_coordinate[0], piece_coordinate[1])
        return one_cost_moves

    def explore_two_and_one_cost_moves(self, piece_coordinate, move, player):
        """
        Explores all possible two cost moves and corresponding one cost moves from the current move.
        """
        two_and_one_cost_moves = {}
        self.move_piece(piece_coordinate[0],
                        piece_coordinate[1], move[0], move[1])
        new_moves = self.get_all_moves(player)
        for new_piece_coordinate, moves in new_moves.items():
            for new_move in moves:
                if new_move[1] == 2:
                    # Found a terminal state
                    two_and_one_cost_moves[(new_piece_coordinate[0], new_piece_coordinate[1])] = (
                        (new_move[0][0], new_move[0][1]), new_move[1])
                elif new_move[1] == 1:
                    intermediate_move = [
                        (new_piece_coordinate[0], new_piece_coordinate[1]), (new_move[0][0], new_move[0][1])]
                    one_cost_moves = self.explore_one_cost_moves(
                        new_piece_coordinate, new_move[0], player)
                    two_and_one_cost_moves |= {
                        intermediate_move + (one_cost_move,)
                        for one_cost_move in one_cost_moves
                    }

        self.move_piece(move[0], move[1],
                        piece_coordinate[0], piece_coordinate[1])
        return two_and_one_cost_moves

    def generate_move_sequences(self, intermediate_move, new_moves, player):
        """
        Generates all possible move sequences from the given intermediate move and new moves.
        """
        move_sequences = []
        for new_piece_coordinate, move in new_moves.items():
            if move[1] == 2:
                # Found a terminal state
                move_sequences.append(
                    intermediate_move + [(new_piece_coordinate[0], new_piece_coordinate[1]), (move[0][0], move[0][1])])
            elif move[1] == 1:
                second_intermediate_move = intermediate_move + \
                    [(new_piece_coordinate[0], new_piece_coordinate[1]),
                     (move[0][0], move[0][1])]
                one_cost_moves = self.explore_one_cost_moves(
                    new_piece_coordinate, move[0], player)
                move_sequences.extend(self.generate_move_sequences(
                    second_intermediate_move, one_cost_moves, player))

        return move_sequences

    def move_piece(self, xi, yi, xf, yf, cost=0):
        self.move_credits -= cost
        self.board.board[xf][yf].value = self.board.board[xi][yi].value
        self.board.board[xi][yi].value = 0

        if self.curr_player == 1:
            self.board.p1_pieces.remove(self.board.board[xi][yi])
            self.board.p1_pieces.append(self.board.board[xf][yf])
        else:
            self.board.p2_pieces.remove(self.board.board[xi][yi])
            self.board.p2_pieces.append(self.board.board[xf][yf])

        if self.move_credits == 0:
            self.curr_player = 1 if self.curr_player == 2 else 2
            self.move_credits = MOVE_CREDITS

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

    def evaluate(self, player):
        # Given a specific board state, evaluate it for the player passed as parameter
        # Evaluation: manhattan distance to opponent corner
        evaluation = 0
        if player == 1:
            for piece in self.board.p1_pieces:
                evaluation -= manhattan_distance(piece, player)
        if player == 2:
            for piece in self.board.p2_pieces:
                evaluation -= manhattan_distance(piece, player)
        return evaluation

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
