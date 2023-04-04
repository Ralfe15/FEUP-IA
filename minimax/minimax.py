BOARD_SIZE = 6
P1_CORNER = [(0, 0), (0, 1), (1, 0), (1, 1)]

P2_CORNER = [(BOARD_SIZE - 1, BOARD_SIZE - 1), (BOARD_SIZE - 1, BOARD_SIZE - 2),
             (BOARD_SIZE - 2, BOARD_SIZE - 1), (BOARD_SIZE - 2, BOARD_SIZE - 2)]

P1_CORNER = [(0, 0), (0, 1), (1, 0), (1, 1)]

P2_CORNER = [(BOARD_SIZE - 1, BOARD_SIZE - 1), (BOARD_SIZE - 1, BOARD_SIZE - 2),
             (BOARD_SIZE - 2, BOARD_SIZE - 1), (BOARD_SIZE - 2, BOARD_SIZE - 2)]

def curr_player_pieces(game):
    """
    returns a list of pieces on the board that belong to the current player. 
    """
    if game.state.curr_player == 1:
        return game.state.board.p1_pieces
    if game.state.curr_player == 2:
        return game.state.board.p2_pieces


def player_pieces(player, game):
    if player == 1:
        return game.state.board.p1_pieces
    if player == 2:
        return game.state.board.p2_pieces


def not_curr_player(game):
    if game.state.curr_player == 1:
        return 2
    if game.state.curr_player == 2:
        return 1


def set_saved_positions(player, saved_positions, game):
    pieces = player_pieces(player, game)
    pieces.clear()
    for i in range(4):
        pieces.append(
            game.state.board.board[saved_positions[i][0]][saved_positions[i][1]])


def get_saved_positions(player, game):
    return [
        (piece.index[0], piece.index[1]) for piece in player_pieces(player, game)
    ]


def evaluate(player, game):
    # Given a specific board state, evaluate it for the player passed as parameter
    # Evaluation: manhattan distance to opponent corner
    evaluation = 0
    pieces_in_spawn = 0
    pieces_in_target = 0
    enemy_pieces_in_target = 0
    if player == 1:
        for piece in game.state.board.p1_pieces:
            evaluation -= manhattan_distance(piece, player)
            if piece.index in P1_CORNER:
                pieces_in_spawn += 1
            if piece.index in P2_CORNER:
                pieces_in_target += 1

    if player == 2:
        for piece in game.state.board.p2_pieces:
            evaluation -= manhattan_distance(piece, player)
            if piece.index in P2_CORNER:
                pieces_in_spawn += 1
            if piece.index in P1_CORNER:
                enemy_pieces_in_target += 1
    return evaluation - (2 * pieces_in_spawn) + (5 * pieces_in_target) - (3 * enemy_pieces_in_target)



def manhattan_distance(coords_piece, player):

    if player == 2:
        return coords_piece.index[0] + coords_piece.index[1]
    elif player == 1:
        return (BOARD_SIZE - 1 - coords_piece.index[0]) + (BOARD_SIZE - 1 - coords_piece.index[1])


def undo_move_sequence(game, moves_seq, player):
    for move in moves_seq[::-1]:
        game.state.move_piece(move[1][0], move[1][1],
                              move[0][0], move[0][1], player=player)


def do_move_sequence(game, moves_seq, player):
    for move in moves_seq:
        game.state.move_piece(move[0][0], move[0][1],
                              move[1][0], move[1][1], player=player)

def minimax(depth, max_player, move_seq=None, alpha=float('-inf'), beta=float('inf'), game=None):
    if depth == 0 or game.state.game_over != 0:
        ev = evaluate(game.state.curr_player, game) if max_player else evaluate(not_curr_player(game), game)
        return ev, move_seq
    best_moves = None
    if max_player == True:
        saved_pos = get_saved_positions(game.state.curr_player, game)
        maxEval = float('-inf')
        for moves in get_terminal_states(game.state.curr_player, game):
            set_saved_positions(game.state.curr_player, saved_pos, game)
            do_move_sequence(game,moves,game.state.curr_player)
            evaluation = minimax(
                depth-1, False, moves, alpha=alpha, beta=beta, game=game)[0]
            undo_move_sequence(game,moves,game.state.curr_player)
            #set_saved_positions(game.state.curr_player, saved_pos, game)
            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
            if maxEval == evaluation:
                best_moves = moves
        return maxEval, best_moves
    else:
        saved_pos = get_saved_positions(not_curr_player(game), game)
        minEval = float('inf')
        for moves in get_terminal_states(not_curr_player(game), game):
            #set_saved_positions(not_curr_player(game), saved_pos, game)
            do_move_sequence(game,moves,not_curr_player(game))
            evaluation = minimax(depth-1, True, moves, alpha, beta, game)[0]
            undo_move_sequence(game,moves,not_curr_player(game))
            #set_saved_positions(not_curr_player(game), saved_pos, game)
            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
            if minEval == evaluation:
                best_moves = moves
        return minEval, best_moves
"""

def minimax(depth, max_player, move_seq=None, alpha=float('-inf'), beta=float('inf'), game=None):
    if depth == 0 or game.state.game_over != 0:
        ev = evaluate(2, game) if max_player else evaluate(1, game)
        return ev, move_seq
    
    best_moves = None
    if max_player == True:
        saved_pos = get_saved_positions(game.state.curr_player, game)
        maxEval = float('-inf')
        for moves in get_terminal_states(game.state.curr_player, game):
            set_saved_positions(game.state.curr_player, saved_pos, game)
            if game.state.game_over != 0:
                return moves
            do_move_sequence(game,moves,game.state.curr_player)
            evaluation = minimax(
                depth-1, False, moves, alpha=alpha, beta=beta, game=game)[0]
            #undo_move_sequence(game, moves,game.state.curr_player)
            set_saved_positions(game.state.curr_player, saved_pos, game)
            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
            if maxEval == evaluation:
                best_moves = moves
        return maxEval, best_moves
    else:
        saved_pos = get_saved_positions(not_curr_player(game), game)
        minEval = float('inf')
        for moves in get_terminal_states(not_curr_player, game):
            set_saved_positions(not_curr_player(game), saved_pos, game)
            if game.state.game_over != 0:
                return moves
            #for move in moves:
                #if len(move) != 2:
                    #game.state.move_piece(move[0][0], move[0][1],move[1][0], move[1][1], player=1)
            do_move_sequence(game,moves,1)
            evaluation = minimax(depth-1, True, moves, alpha, beta, game)[0]
            #undo_move_sequence(game,moves,not_curr_player(game))
            set_saved_positions(not_curr_player(game), saved_pos, game)
            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
            if minEval == evaluation:
                best_moves = moves
        return minEval, best_moves
"""


def get_all_moves_for_tile(tile, all_moves, game):
    # All possible moves with associated cost for player 1
    all_moves[tile.index] = game.state.get_moves_by_cost(
        tile.index[0], tile.index[1], 1)
    if game.state.move_credits >= 2:
        all_moves[tile.index] += game.state.get_moves_by_cost(
            tile.index[0], tile.index[1], 2)
    if game.state.move_credits == 3:
        all_moves[tile.index] += game.state.get_moves_by_cost(
            tile.index[0], tile.index[1], 3)


def get_all_moves(player, game):
    all_moves = {}
    if player == 1:
        for tile in game.state.board.p1_pieces:
            get_all_moves_for_tile(tile, all_moves, game)
    elif player == 2:
        for tile in game.state.board.p2_pieces:
            get_all_moves_for_tile(tile, all_moves, game)
    return all_moves


def get_terminal_states(player, game):
    # Returns a list of list, containing move sequences that use all 3 "move credits". Can be used as a stack and
    # pop moves to get order
    # The format is: [[((source_x1, source_y1), (dest_x1, dest_y1)), ((source_x2, source_y2), (dest_x2, dest_y2))]]
    move_sequences = []
    moves = get_all_moves(player, game)

    # Iterate over all pieces and their moves
    for piece_coordinate, moves in moves.items():
        # Check all moves of a particular piece for terminal states
        for move in moves:
            if move[1] == 3:
                # If move is a 3 cost, we are in a terminal state
                move_sequences.append(
                    [((piece_coordinate[0], piece_coordinate[1]), (move[0][0], move[0][1]))])

            elif move[1] == 2:
                # If a move is a 2 cost, we need to explore all possible one cost moves after it
                explore_one_cost_moves(
                    player, game, piece_coordinate, move, move_sequences)
            elif move[1] == 1:
                # If a move is a 1 cost, we need to explore all possible 2 cost moves after it and two 1 cost moves
                # after it too
                explore_two_cost_moves(
                    player, game, piece_coordinate, move, move_sequences)

    return move_sequences


def explore_one_cost_moves(player, game, piece_coordinate, move, move_sequences):
    """
    Given a piece coordinate and 2-cost move, explores all possible 1-cost moves 
    from destination of 2-cost move and returns move sequences for terminal states.
    """
    intermediate_move = [
        ((piece_coordinate[0], piece_coordinate[1]), (move[0][0], move[0][1]))]
    # Make move
    # Make move
    game.state.move_piece(
        piece_coordinate[0], piece_coordinate[1], move[0][0], move[0][1], player=player)

    # Explore all possible new 1 cost moves
    for new_piece_coordinate, new_moves in get_all_moves(player, game).items():
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
    game.state.move_piece(
        move[0][0], move[0][1], piece_coordinate[0], piece_coordinate[1], player=player)


def explore_two_cost_moves(player, game, piece_coordinate, move, move_sequences):
    """
    Given a piece coordinate and 1-cost move, explores all possible 2-cost and 1-cost moves 
    after it and returns move sequences for terminal states.
    """
    # If a move is a 1 cost, we need to explore all possible 2 cost moves after it and two 1 cost moves
    # after it too
    first_intermediate_move = [
        ((piece_coordinate[0], piece_coordinate[1]), (move[0][0], move[0][1]))]

    # Make move
    game.state.move_piece(
        piece_coordinate[0], piece_coordinate[1], move[0][0], move[0][1], player=player)

    # Explore all possible new 1 and 2 cost moves (2 cost are terminals)
    for new_piece_coordinate, new_moves in get_all_moves(player, game).items():
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
                game.state.move_piece(new_piece_coordinate[0], new_piece_coordinate[1], new_move[0][0],
                                      new_move[0][1], player=player)

                for new_layer2_piece_coordinate, new_layer2_moves in get_all_moves(player, game).items():
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
                game.state.move_piece(new_move[0][0], new_move[0][1], new_piece_coordinate[0],
                                      new_piece_coordinate[1], player=player)

    # Undo first layer move
    game.state.move_piece(
        move[0][0], move[0][1], piece_coordinate[0], piece_coordinate[1], player=player)
