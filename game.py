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
        return coords_piece.index[0] + coords_piece.index[1]
    elif player == 1:
        return (BOARD_SIZE - 1 - coords_piece.index[0]) + (BOARD_SIZE - 1 - coords_piece.index[1])


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

    def gameprint(self):
        player1_pos = [
            (piece.index[0], piece.index[1]) for piece in self.board.p1_pieces
        ]
        player2_pos = [
            (piece.index[0], piece.index[1]) for piece in self.board.p2_pieces
        ]
        print("Player 1 =", player1_pos)
        print("Player 2 =", player2_pos)

    def curr_player_pieces(self):
        """
        returns a list of pieces on the board that belong to the current player. 
        """
        if self.curr_player == 1:
            return self.board.p1_pieces
        if self.curr_player == 2:
            return self.board.p2_pieces

    def player_pieces(self, player):
        if player == 1:
            return self.board.p1_pieces
        if player == 2:
            return self.board.p2_pieces

    def not_curr_player(self):
        if self.curr_player == 1:
            return 2
        if self.curr_player == 2:
            return 1

    def set_saved_positions(self, player, saved_positions):
        pieces = self.player_pieces(player)
        pieces.clear()
        for i in range(4):
            pieces.append(
                self.board.board[saved_positions[i][0]][saved_positions[i][1]])

    def get_saved_positions(self, player):
        return [
            (piece.index[0], piece.index[1]) for piece in self.player_pieces(player)
        ]

    def minimax(self, depth, max_player, move_seq=None, alpha=float('-inf'), beta=float('inf')):
        if depth == 0 or self.game_over != 0:
            evaluate = self.evaluate(2) if max_player else self.evaluate(1)
            return evaluate, move_seq
        best_moves = None
        if max_player == True:
            saved_pos = self.get_saved_positions(self.curr_player)
            maxEval = float('-inf')
            for moves in self.get_terminal_states_old(self.curr_player):
                self.set_saved_positions(self.curr_player, saved_pos)
                for move in moves:
                    if len(move) != 2:
                        self.move_piece(move[0][0], move[0][1],
                                        move[1][0], move[1][1], player=self.curr_player)
                evaluation = self.minimax(
                    depth-1, False, moves, alpha=alpha, beta=beta)[0]
                self.set_saved_positions(self.curr_player, saved_pos)
                maxEval = max(maxEval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
                if maxEval == evaluation:
                    best_moves = moves
            return maxEval, best_moves
        else:
            saved_pos = self.get_saved_positions(self.not_curr_player())
            minEval = float('inf')
            for moves in self.get_terminal_states_old(self.not_curr_player()):
                self.set_saved_positions(self.not_curr_player(), saved_pos)
                for move in moves:
                    if len(move) != 2:
                        self.move_piece(move[0][0], move[0][1],
                                        move[1][0], move[1][1], player=1)
                evaluation = self.minimax(depth-1, True, moves, alpha, beta)[0]
                self.set_saved_positions(self.not_curr_player(), saved_pos)
                minEval = min(minEval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
                if minEval == evaluation:
                    best_moves = moves
            return minEval, best_moves

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

    def get_terminal_states_old(self, player):
        # Returns a list of list, containing move sequences that use all 3 "move credits". Can be used as a stack and
        # pop moves to get order
        # The format is: [[((source_x1, source_y1), (dest_x1, dest_y1)), ((source_x2, source_y2), (dest_x2, dest_y2))]]
        move_sequences = []
        moves = self.get_all_moves(player)
        for piece_coordinate, moves in moves.items():
            for move in moves:
                if move[1] == 3:
                    # If move is a 3 cost, we are in a terminal state
                    move_sequences.append(
                        [((piece_coordinate[0], piece_coordinate[1]), (move[0][0], move[0][1]))])

                elif move[1] == 2:
                    # If a move is a 2 cost, we need to explore all possible one cost moves after it
                    intermediate_move = [
                        ((piece_coordinate[0], piece_coordinate[1]), (move[0][0], move[0][1]))]

                    # Make move
                    self.move_piece(
                        piece_coordinate[0], piece_coordinate[1], move[0][0], move[0][1], player=player)

                    # Explore all possible new 1 cost moves
                    for new_piece_coordinate, new_moves in self.get_all_moves(player).items():
                        move_sequences.extend(
                            intermediate_move
                            + [
                                (
                                    (
                                        new_piece_coordinate[0],
                                        new_piece_coordinate[1],
                                    ),
                                    (new_move[0][0], new_move[0][1]),
                                )
                            ]
                            for new_move in new_moves
                            if new_move[1] == 1
                        )
                    # Undo move
                    self.move_piece(
                        move[0][0], move[0][1], piece_coordinate[0], piece_coordinate[1], player=player)

                elif move[1] == 1:
                    # If a move is a 1 cost, we need to explore all possible 2 cost moves after it and two 1 cost moves
                    # after it too
                    first_intermediate_move = [
                        ((piece_coordinate[0], piece_coordinate[1]), (move[0][0], move[0][1]))]

                    # Make move
                    self.move_piece(
                        piece_coordinate[0], piece_coordinate[1], move[0][0], move[0][1], player=player)

                    # Explore all possible new 1 and 2 cost moves (2 cost are terminals)
                    for new_piece_coordinate, new_moves in self.get_all_moves(player).items():
                        for new_move in new_moves:
                            if new_move[1] == 2:
                                # 2 cost move (terminal)
                                move_sequences.append(first_intermediate_move + [((new_piece_coordinate[0],
                                                                                   new_piece_coordinate[1]),
                                                                                  (new_move[0][0], new_move[0][1]))])

                            if new_move[1] == 1:
                                # 1 cost (explore one more layer)
                                second_intermediate_move = first_intermediate_move + [((new_piece_coordinate[0],
                                                                                        new_piece_coordinate[1]), (
                                    new_move[0][0],
                                    new_move[0][1]))]

                                # Make second 1 cost move
                                self.move_piece(new_piece_coordinate[0], new_piece_coordinate[1], new_move[0][0],
                                                new_move[0][1], player=player)

                                for new_layer2_piece_coordinate, new_layer2_moves in self.get_all_moves(player).items():
                                    move_sequences.extend(
                                        second_intermediate_move
                                        + [
                                            (
                                                (
                                                    new_layer2_piece_coordinate[0],
                                                    new_layer2_piece_coordinate[1],
                                                ),
                                                (
                                                    new_layer2_move[0][0],
                                                    new_layer2_move[0][1],
                                                ),
                                            )
                                        ]
                                        for new_layer2_move in new_layer2_moves
                                        if new_layer2_move[1] == 1
                                    )
                                # Undo second one cost move
                                self.move_piece(new_move[0][0], new_move[0][1], new_piece_coordinate[0],
                                                new_piece_coordinate[1], player=player)

                    # Undo first layer move
                    self.move_piece(
                        move[0][0], move[0][1], piece_coordinate[0], piece_coordinate[1], player=player)
        return move_sequences


    def move_piece(self, xi, yi, xf, yf, cost=0, player=None):

        self.move_credits -= cost
        self.board.board[xf][yf].value = self.board.board[xi][yi].value
        self.board.board[xi][yi].value = 0
        _player = player if player else self.curr_player
        if _player == 1:
            self.board.p1_pieces.remove(self.board.board[xi][yi])
            self.board.p1_pieces.append(self.board.board[xf][yf])
        else:
            self.board.p2_pieces.remove(self.board.board[xi][yi])
            self.board.p2_pieces.append(self.board.board[xf][yf])

        if self.move_credits == 0:
            _player = 1 if _player == 2 else 2
            if player is None:
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
