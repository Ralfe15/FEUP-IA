import game

if __name__ == '__main__':
    g1 = game.Game(1)
    g1.state.print_board()

    # print(g1.state.get_moves(0, 1))
    # print(g1.state.p1_pieces)
    # print(g1.state.evaluate(1))
    # g1.state.move_piece(0, 1, 2, 1)
    # print(g1.state.p1_pieces)
    # print(g1.state.evaluate(1))

    # g1.state.print_board()

    print(g1.state.get_all_moves(2))
