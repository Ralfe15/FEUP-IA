# Game data structure representing a certain state of a LESS match
import copy
import random

BOARD_SIZE = 6
DEBUG = True
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

def generate_initial_state():
    # Returns a game in initial state: a 6x6 board with 4 players in top left and bottom right corners
    board = [[Tile() for _ in range(6)] for _ in range(6)]
    board[0][0] = board[0][1] = board[1][0] = board[1][1] = Tile(1)
    board[BOARD_SIZE - 1][BOARD_SIZE - 1] = board[BOARD_SIZE - 1][BOARD_SIZE - 2] = board[BOARD_SIZE - 2][
        BOARD_SIZE - 1] \
        = board[BOARD_SIZE - 2][BOARD_SIZE - 2] = Tile(2)
    return board

def manhattan_distance(coords_piece, player):
    if player == 2:
        return coords_piece[0] + coords_piece[1]
    elif player==1:
        return (BOARD_SIZE-1 - coords_piece[0]) + (BOARD_SIZE-1 -coords_piece[1])


class Game:
    def __init__(self, players):
        self.players = players
        # Generate new game state, fresh board and random starting player
        self.state = GameState(generate_initial_state(), random.randint(1, 2))


class Tile:
    def __init__(self, value=0):
        self.value = value
        self.walls = [1 if random.randint(
            0, 1) <= 0.3 else 0 for _ in range(4)]

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


class GameState:
    # To access a (x, y) coord on the board: self.board[y][x] starting at (0,0)
    def __init__(self, board, curr_player, move_credits = 3):
        self.board = board
        self.curr_player = curr_player
        self.p1_pieces = []
        self.p2_pieces = []
        self.move_credits = move_credits

        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j].value == 1:
                    self.p1_pieces.append([j, i])
                elif self.board[i][j].value == 2:
                    self.p2_pieces.append([j, i])

    # Get available moves for piece at coords (x, y)
    # Returns list of available moves [[(x, y), cost]]
    # Legal moves are: moving to an empty space left/right/up/down, leaping one piece to an empty space
    def get_moves_by_cost(self, x, y, cost):
        moves = []

        if x not in range(BOARD_SIZE) or y not in range(BOARD_SIZE) or self.board[x][y].value == 0:
            return []

        # Check up
        if y - 1 in range(BOARD_SIZE) and self.board[y - 1][x].value == 0:
            moves.append([(x, y - 1), self.check_walls_simple_move(x, y, UP)])

        # Check down
        if y + 1 in range(BOARD_SIZE) and self.board[y + 1][x].value == 0:
            moves.append([(x, y + 1), self.check_walls_simple_move(x,y, DOWN)])

        # Check right
        if x + 1 in range(BOARD_SIZE) and self.board[y][x + 1].value == 0:
            moves.append([(x + 1, y), self.check_walls_simple_move(x,y, RIGHT)])

        # Check left
        if x - 1 in range(BOARD_SIZE) and self.board[y][x - 1].value == 0:
            moves.append([(x - 1, y), self.check_walls_simple_move(x,y, LEFT)])


        # Check leap up
        if y - 2 in range(BOARD_SIZE) and self.board[y - 1][x].value != 0 and self.board[y - 2][x].value == 0 and self.check_can_leap(x, y, UP):
            moves.append([(x, y - 2), 1])

        # Check leap down
        if y + 2 in range(BOARD_SIZE) and self.board[y + 1][x].value != 0 and self.board[y + 2][x].value == 0 and self.check_can_leap(x, y, DOWN):
            moves.append([(x, y + 2), 1])

        # Check leap right
        if x + 2 in range(BOARD_SIZE) and self.board[y][x + 1].value != 0 and self.board[y][x + 2].value == 0 and self.check_can_leap(x, y, RIGHT):
            moves.append([(x + 2, y), 1])

        # Check leap left
        if x - 2 in range(BOARD_SIZE) and self.board[y][x - 1].value != 0 and self.board[y][x - 2].value == 0 and self.check_can_leap(x, y, LEFT):
            moves.append([(x - 2, y), 1])

        
        return [move for move in moves if move[1] == cost]
    
    def get_all_moves(self, player):
        all_moves = {}
        if player == 1:
            for coords in self.p1_pieces:
                # All possible moves with associated cost for player 1
                all_moves[coords[0], coords[1]] = self.get_moves_by_cost(coords[0], coords[1], 1)
                all_moves[coords[0], coords[1]] += self.get_moves_by_cost(coords[0], coords[1], 2)
                all_moves[coords[0], coords[1]] += self.get_moves_by_cost(coords[0], coords[1], 3)
        elif player==2:
            for coords in self.p2_pieces:
                all_moves[coords[0], coords[1]] = self.get_moves_by_cost(coords[0], coords[1], 1)
                all_moves[coords[0], coords[1]] += self.get_moves_by_cost(coords[0], coords[1], 2)
                all_moves[coords[0], coords[1]] += self.get_moves_by_cost(coords[0], coords[1], 3)
        return all_moves
    
    def get_terminal_states(self, player):
        #{(0, 0): [[(2, 0), 1]], (0, 1): [[(2, 1), 1], [(0, 2), 2]], (1, 0): [[(2, 0), 1]], (1, 1): [[(2, 1), 1], [(1, 2), 2]]}
        terminal_states = []
        intermediate_states_2_cost = []
        intermediate_states_1_cost = []
        aux_intermediate_states_1_cost = []
        moves = self.get_all_moves(player)
        for piece_coordinate, moves in moves.items():
            for move in moves:
                if move[1] == 3:
                    # If move is a 3 cost, we are in a terminal state
                    terminal_states.append(self.move_piece(piece_coordinate[0],piece_coordinate[1], move[0][0], move[0][1]))
                elif move[1] == 2:
                    # If a move is a 2 cost, we need to explore all possible one cost moves after it later
                    intermediate_states_2_cost.append(self.move_piece(piece_coordinate[0],piece_coordinate[1], move[0][0], move[0][1]))
                elif move[1] == 1:
                    # If a move is a 1 cost, we need to explore all possible 2 cost moves after it and two 1 cost moves after it too
                    intermediate_states_1_cost.append(self.move_piece(piece_coordinate[0],piece_coordinate[1], move[0][0], move[0][1]))
        
        # Explore possible 1 cost moves withn our 2 cost states
        for state in intermediate_states_2_cost:
            moves = state.get_all_moves(player)
            for piece_coordinate, moves in moves.items():
                for move in moves:
                    if move[1] == 1:
                        # 1 cost move
                        terminal_states.append(state.move_piece(piece_coordinate[0],piece_coordinate[1], move[0][0], move[0][1]))

        # Explore possible 2 cost and 1 cost withn our 1 cost states
        for state in intermediate_states_1_cost:
            moves = state.get_all_moves(player)
            for piece_coordinate, moves in moves.items():
                for move in moves:
                    if move[1] == 1:
                        aux_intermediate_states_1_cost.append(state.move_piece(piece_coordinate[0],piece_coordinate[1], move[0][0], move[0][1]))
                    elif move[1] == 2:
                        # 2 cost move
                        terminal_states.append(state.move_piece(piece_coordinate[0],piece_coordinate[1], move[0][0], move[0][1]))
        
        # Finally, explore all 1 cost moves after witn our 2 sequential 1 cost plays
        for state in aux_intermediate_states_1_cost:
            moves = state.get_all_moves(player)
            for piece_coordinate, moves in moves.items():
                for move in moves:
                    if move[1] == 1:
                        terminal_states.append(state.move_piece(piece_coordinate[0],piece_coordinate[1], move[0][0], move[0][1]))

        return terminal_states
     
    def move_piece(self, xi, yi, xf, yf):
            new_board = copy.deepcopy(self.board)
            new_board[yf][xf],new_board[yi][xi] = self.board[yi][xi], self.board[yf][xf]
            return GameState(new_board, self.curr_player)

    def evaluate(self, player):
        # Given a specific board state, evaluate it for the player passed as parameter
        # Evaluation: manhattan distance to oponnent corner
        evaluation = 0
        if player == 1:
            for piece in self.p1_pieces:
                evaluation -= manhattan_distance(piece, player)
        if player == 2:
            for piece in self.p2_pieces:
                evaluation -= manhattan_distance(piece, player)
        return evaluation

    def check_walls_simple_move(self, source_x, source_y, direction):
        cost = 1
        if direction == UP:
            if self.board[source_y][source_x].has_wall_up():
                cost += 1
                if self.board[source_y-1][source_x].has_wall_down():
                    cost += 1
        if direction == DOWN:
            if self.board[source_y][source_x].has_wall_down():
                cost += 1
                if self.board[source_y+1][source_x].has_wall_up():
                    cost += 1
        if direction == LEFT:
            if self.board[source_y][source_x].has_wall_left():
                cost += 1
                if self.board[source_y][source_x-1].has_wall_right():
                    cost += 1
        if direction == RIGHT:
            if self.board[source_y][source_x].has_wall_right():
                cost += 1
                if self.board[source_y][source_x+1].has_wall_left():
                    cost += 1
        return cost
    
    def check_can_leap(self, source_x, source_y, direction):
        if direction == UP:
            return not (self.board[source_y][source_x].has_wall_up() or self.board[source_y-1][source_x].has_wall_down() or
                         self.board[source_y-1][source_x].has_wall_up() or self.board[source_y-2][source_x].has_wall_down())
        if direction == DOWN:
            return not (self.board[source_y][source_x].has_wall_up() or self.board[source_y+1][source_x].has_wall_down() or
                         self.board[source_y+1][source_x].has_wall_up() or self.board[source_y-2][source_x].has_wall_up())
        if direction == LEFT:
            return not (self.board[source_y][source_x].has_wall_left() and self.board[source_y][source_x-1].has_wall_left() and
                         self.board[source_y][source_x-1].has_wall_right() and self.board[source_y][source_x-2].has_wall_right())
        if direction == RIGHT:
            return not (self.board[source_y][source_x].has_wall_right() and self.board[source_y][source_x+1].has_wall_right() and
                         self.board[source_y][source_x+1].has_wall_left() and self.board[source_y][source_x+2].has_wall_left())

        

    def print_board(self):
        # print("   0  1  2  3  4  5 --> X")z
        for i in range(len(self.board)):
            # print(i, end=" ")
            for j in self.board[i]:
                print(j.value, end=" ")
            print("")
