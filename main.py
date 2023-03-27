import game

if __name__ == '__main__':
    g1 = game.Game(1)
    # g1.state.print_board()

    # print(g1.state.get_all_moves(1))
    # g1.state.print_board()
    # print(g1.state.p1_pieces)
    # print(g1.state.evaluate(1))
    # g1.state = g1.state.move_piece(0, 1, 2, 1)
    print(g1.state.get_all_moves(1))
    terminal_states = g1.state.get_terminal_states(2)
    for i in terminal_states:
        i.print_board()
        print("===============")
        print(i.p1_pieces)
        print("===============")
        
    # print(g1.state.evaluate(1))

    # g1.state.print_board()

    # print(g1.state.get_all_moves(1))
