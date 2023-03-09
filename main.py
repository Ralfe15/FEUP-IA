import game

if __name__ == '__main__':
    g1 = game.Game(1)
    g1.state.print_board()
    # print(g1.state.get_moves(0, 1))
    tile = game.Tile()
    print(tile.walls)
    # print(g1.state.p2_pieces)
    # g1.state.move_piece(0, 1, 2, 1)
    # g1.state.print_board()
