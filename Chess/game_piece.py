# from copy import deepcopy


class Piece:
    black_pawns_init_positon = [(1, i) for i in range(8)]
    white_pawns_init_positon = [(6, i) for i in range(8)]
    white_pawn_diagonals = [(-1, -1), (-1, 1)]
    black_pawn_diagonals = [(1, -1), (1, 1)]
    white_first_double_moves = [(3, i) for i in range(8)]
    black_first_double_moves = [(4, i) for i in range(8)]
    white_promotion_squares = [(0, i) for i in range(8)]
    black_promotion_squares = [(7, i) for i in range(8)]
    white_king_init_position = (7, 4)
    black_king_init_position = (0, 4)
    double_pawn_move = None
    promotion_choice = None
    white_king_has_moved = False
    black_king_has_moved = False
    white_king_rook_has_moved = False
    white_queen_rook_has_moved = False
    black_king_rook_has_moved = False
    black_queen_rook_has_moved = False
    king_init_positon_dict = {
        "W": white_king_init_position, "B": black_king_init_position}
    init_color_dict = {"W": white_pawns_init_positon,
                       "B": black_pawns_init_positon}
    opponent_color_dict = {"W": 'B', "B": 'W'}
    white_partner_pieces = ["wP", "wB", "wK", "wQ", "wN", "wR"]
    black_partner_pieces = ["bP", "bB", "bK", "bQ", "bN", "bR"]
    opponent_king_dict = {"W": "bK", "B": "wK"}
    piece_type_dict = {"R": "rook", "N": "knight", "B": "bishop", "Q": "queen",
                       "K": "king", "P": "pawn"}
    piece_symbol_dict = {"rook": "R", "knight": "N",
                         "pawn": "P", "king": "K", "queen": "Q", "bishop": "B"}
    # all_color_pieces = white_partner_pieces + black_partner_pieces
    partners_dict = {"W": white_partner_pieces, "B": black_partner_pieces}
    promotion_dict = {"W": white_promotion_squares,
                      "B": black_promotion_squares}
    diagonals_dict = {"W": white_pawn_diagonals, "B": black_pawn_diagonals}

    def __init__(self, row, column, piece_type, piece_id, piece_color, alt_name=None):
        self.row = row
        self.column = column
        self.piece_type = piece_type
        self.piece_id = piece_id
        self.piece_color = piece_color
        self.alt_name = alt_name

    def check_if_piece_can_move(board, row, col, piece_type, player_color):
        # print('piece type:', piece_type)
        if piece_type == "pawn":
            checker = Piece.squares_pawn_can_move_to(
                board, row, col, player_color)
        if piece_type == "queen":
            checker = Piece.squares_queen_can_move_to(
                board, row, col, player_color)
        if piece_type == "king":
            checker = Piece.squares_king_can_move_to(
                board, row, col, player_color)
        if piece_type == "bishop":
            checker = Piece.squares_bishop_can_move_to(
                board, row, col, player_color)
        if piece_type == "rook":
            checker = Piece.squares_rook_can_move_to(
                board, row, col, player_color)
        if piece_type == "knight":
            checker = Piece.squares_knight_can_move_to(
                board, row, col, player_color)

        return checker

    def check_if_king_is_in_check(board, color):
        opponent_color = Piece.opponent_color_dict[color]

        for r in range(8):
            for c in range(8):
                if board[r][c] in Piece.partners_dict[opponent_color]:
                    piece = board[r][c]
                    # print('piece:', piece)
                    is_in_check = Piece.check_piece_check(
                        board, r, c, Piece.piece_type_dict[piece[-1]], opponent_color)
                    if is_in_check:
                        return is_in_check
                    continue

        return False

    def make_temp_move(board, origin, destination):
        # print('origin:', origin)
        # print('destination:', destination)
        # print('the piece:', board[origin[0]][origin[1]])
        # board_copy = deepcopy(board)
        board_copy = [r[:] for r in board]
        ori_row, ori_col = origin
        dest_row, dest_col = destination
        the_piece = board[ori_row][ori_col]
        board_copy[ori_row][ori_col] = " "
        board_copy[dest_row][dest_col] = the_piece
        return board_copy

    def make_enpassant_move(board, origin, destination, piece_to_remove):
        # print(origin, destination, piece_to_remove)
        board_copy = [r[:] for r in board]
        ori_row, ori_col = origin
        dest_row, dest_col = destination
        a, b = piece_to_remove
        the_piece = board[ori_row][ori_col]
        board_copy[a][b] = " "
        board_copy[ori_row][ori_col] = " "
        board_copy[dest_row][dest_col] = the_piece
        return board_copy

    def get_king_location(board, color):
        king_dict = {"W": "wK", "B": "bK"}
        for r in range(8):
            for c in range(8):
                if board[r][c] == king_dict[color]:
                    return (r, c)

    def check_piece_check(board, row, col, piece_type, color):
        # Piece.display_board(board)
        # print('piece type:', piece_type)
        if piece_type == "king":
            return Piece.check_king_space(board, row, col, color)
        if piece_type == "queen":
            return Piece.get_queen_check(board, row, col, color)
        if piece_type == "rook":
            return Piece.get_rook_check(board, row, col, color)
        if piece_type == "bishop":
            return Piece.get_bishop_check(board, row, col, color)
        if piece_type == "knight":
            return Piece.get_knight_check(board, row, col, color)
        if piece_type == "pawn":
            return Piece.get_pawn_check(board, row, col, color)

    def check_king_space(board, row, col, player_color):
        # print(player_color)
        # Piece.display_board(board)
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1),
                      (-1, 1), (-1, -1), (1, -1), (1, 1)]
        for dy, dx in directions:
            constant = row, col
            new_row, new_col = constant[0] + dy, constant[1] + dx
            if not Piece.square_is_within_bounds(new_row, new_col):
                break

            # print('opponent king:', Piece.opponent_king_dict[player_color])
            if board[new_row][new_col] == Piece.opponent_king_dict[player_color]:
                return True

        return False

    def get_queen_check(board, row, col, color):
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1),
                      (-1, 1), (-1, -1), (1, -1), (1, 1)]

        for dy, dx in directions:
            constant = row, col
            while True:
                new_row, new_col = constant[0] + dy, constant[1] + dx
                if not Piece.square_is_within_bounds(new_row, new_col):
                    break

                piece = board[new_row][new_col]
                if piece != Piece.opponent_king_dict[color] and piece != " ":
                    break
                if piece == Piece.opponent_king_dict[color]:
                    return True

                constant = new_row, new_col

        return False

    def get_rook_check(board, row, col, color):
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for dy, dx in directions:
            constant = row, col
            while True:
                new_row, new_col = constant[0] + dy, constant[1] + dx
                if not Piece.square_is_within_bounds(new_row, new_col):
                    break

                piece = board[new_row][new_col]
                if piece != Piece.opponent_king_dict[color] and piece != " ":
                    break
                if piece == Piece.opponent_king_dict[color]:
                    return True

                constant = new_row, new_col

        return False

    def get_bishop_check(board, row, col, color):
        directions = [(-1, 1), (-1, -1), (1, -1), (1, 1)]

        for dy, dx in directions:
            constant = row, col
            while True:
                new_row, new_col = constant[0] + dy, constant[1] + dx
                if not Piece.square_is_within_bounds(new_row, new_col):
                    break

                piece = board[new_row][new_col]
                if piece != Piece.opponent_king_dict[color] and piece != " ":
                    break
                if piece == Piece.opponent_king_dict[color]:
                    return True

                constant = new_row, new_col

        return False

    def get_knight_check(board, row, col, color):
        directions = [(-2, 1), (-1, 2), (2, 1), (1, 2),
                      (-1, -2), (-2, -1), (1, -2), (2, -1)]

        for dy, dx in directions:
            constant = row, col
            new_row, new_col = constant[0] + dy, constant[1] + dx
            if not Piece.square_is_within_bounds(new_row, new_col):
                continue

            if board[new_row][new_col] == Piece.opponent_king_dict[color]:
                return True

        return False

    def get_pawn_check(board, row, col, color):
        # check if pawn can check diagonally
        for dy, dx in Piece.diagonals_dict[color]:
            new_row, new_col = row + dy, col + dx
            if Piece.square_is_within_bounds(new_row, new_col):
                if board[new_row][new_col] == Piece.opponent_king_dict[color]:
                    return True

        return False

    def squares_pawn_can_move_to(board, row, col, player_color):
        valid_moves = []
        legal_moves = []

        # check if pawn can capture diagonally
        for dy, dx in Piece.diagonals_dict[player_color]:
            new_row, new_col = row + dy, col + dx
            if Piece.square_is_within_bounds(new_row, new_col):
                if board[new_row][new_col] not in Piece.partners_dict[player_color] and \
                    board[new_row][new_col] != Piece.opponent_king_dict[player_color] and \
                        board[new_row][new_col] != " ":
                    valid_moves.append((new_row, new_col))

        # check if the pawn hasn't been moved
        if (row, col) in Piece.init_color_dict[player_color]:
            if player_color == "W":
                # check if the squares ahead are free
                if board[row-1][col] == " ":
                    valid_moves.append((row-1, col))
                if board[row-1][col] == " " and board[row-2][col] == " ":
                    valid_moves.append((row-2, col))
            else:
                # check if the squares ahead are free
                if board[row+1][col] == " ":
                    valid_moves.append((row+1, col))
                if board[row+1][col] == " " and board[row+2][col] == " ":
                    valid_moves.append((row+2, col))
        else:
            if player_color == "W":
                if board[row-1][col] == " ":
                    valid_moves.append((row-1, col))
            else:
                if board[row+1][col] == " ":
                    valid_moves.append((row+1, col))

        # check for En passant
        if Piece.double_pawn_move:
            opponent_color = Piece.opponent_color_dict[player_color]
            r, c = Piece.double_pawn_move[0]
            if (player_color == "W" and row == 3) or (player_color == "B" and row == 4):
                if Piece.double_pawn_move[1] == opponent_color and abs(col-c) == 1:
                    if player_color == "W":
                        en_passant_move = r-1, c
                    else:
                        en_passant_move = r+1, c

                    # print('en_passant_move:', en_passant_move)
                    new_board = Piece.make_enpassant_move(
                        board, (row, col), en_passant_move, (r, c))
                    king_will_be_in_check = Piece.check_if_king_is_in_check(
                        new_board, player_color)
                    if not king_will_be_in_check:
                        if player_color == "W":
                            legal_moves.append((r-1, c))
                        else:
                            legal_moves.append((r+1, c))

        if valid_moves:  # if available moves
            # check if any move by the piece will expose the king
            for move in valid_moves:
                new_board = Piece.make_temp_move(board, (row, col), move)
                king_will_be_in_check = Piece.check_if_king_is_in_check(
                    new_board, player_color)
                if not king_will_be_in_check:
                    legal_moves.append(move)

        return legal_moves

    def squares_queen_can_move_to(board, row, col, player_color):
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1),
                      (-1, 1), (-1, -1), (1, -1), (1, 1)]
        valid_moves = []
        legal_moves = []
        for dy, dx in directions:
            constant = row, col
            while True:
                new_row, new_col = constant[0] + dy, constant[1] + dx
                if not Piece.square_is_within_bounds(new_row, new_col):
                    break

                piece = board[new_row][new_col]
                opponent_color = Piece.opponent_color_dict[player_color]

                # if piece is an enemy, it can be captured
                if piece in Piece.partners_dict[opponent_color]:
                    constant = new_row, new_col
                    valid_moves.append((new_row, new_col))
                    break
                # if piece is a partner, it cannot be jumped
                if piece in Piece.partners_dict[player_color]:
                    break

                constant = new_row, new_col
                valid_moves.append((new_row, new_col))

        if valid_moves:  # if available moves
            # check if any move by the piece will expose the king
            for move in valid_moves:
                new_board = Piece.make_temp_move(board, (row, col), move)
                king_will_be_in_check = Piece.check_if_king_is_in_check(
                    new_board, player_color)
                if not king_will_be_in_check:
                    legal_moves.append(move)

        return legal_moves

    def squares_rook_can_move_to(board, row, col, player_color):
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        valid_moves = []
        legal_moves = []
        for dy, dx in directions:
            constant = row, col
            while True:
                new_row, new_col = constant[0] + dy, constant[1] + dx
                if not Piece.square_is_within_bounds(new_row, new_col):
                    break

                piece = board[new_row][new_col]
                opponent_color = Piece.opponent_color_dict[player_color]

                # if piece is an enemy, it can be captured
                if piece in Piece.partners_dict[opponent_color]:
                    constant = new_row, new_col
                    valid_moves.append((new_row, new_col))
                    break
                # if piece is a partner, it cannot be jumped
                if piece in Piece.partners_dict[player_color]:
                    break

                constant = new_row, new_col
                valid_moves.append((new_row, new_col))

        # print('valid moves:', valid_moves)

        if valid_moves:  # if available moves
            # check if any move by the piece will expose the king
            for move in valid_moves:
                new_board = Piece.make_temp_move(board, (row, col), move)
                king_will_be_in_check = Piece.check_if_king_is_in_check(
                    new_board, player_color)
                if not king_will_be_in_check:
                    legal_moves.append(move)

        return legal_moves

    def squares_bishop_can_move_to(board, row, col, player_color):
        directions = [(-1, 1), (-1, -1), (1, -1), (1, 1)]
        valid_moves = []
        legal_moves = []
        for dy, dx in directions:
            constant = row, col
            while True:
                new_row, new_col = constant[0] + dy, constant[1] + dx
                if not Piece.square_is_within_bounds(new_row, new_col):
                    break

                piece = board[new_row][new_col]
                opponent_color = Piece.opponent_color_dict[player_color]

                # if piece is an enemy, it can be captured
                if piece in Piece.partners_dict[opponent_color]:
                    constant = new_row, new_col
                    valid_moves.append((new_row, new_col))
                    break
                # if piece is a partner, it cannot be jumped
                if piece in Piece.partners_dict[player_color]:
                    break

                constant = new_row, new_col
                valid_moves.append((new_row, new_col))

        if valid_moves:  # if available moves
            # check if any move by the piece will expose the king
            for move in valid_moves:
                new_board = Piece.make_temp_move(board, (row, col), move)
                king_will_be_in_check = Piece.check_if_king_is_in_check(
                    new_board, player_color)
                if not king_will_be_in_check:
                    legal_moves.append(move)

        return legal_moves

    def squares_knight_can_move_to(board, row, col, player_color):
        directions = [(-2, 1), (-1, 2), (2, 1), (1, 2),
                      (-1, -2), (-2, -1), (1, -2), (2, -1)]
        valid_moves = []
        legal_moves = []
        for dy, dx in directions:
            constant = row, col
            new_row, new_col = constant[0] + dy, constant[1] + dx
            if not Piece.square_is_within_bounds(new_row, new_col):
                continue

            piece = board[new_row][new_col]
            opponent_color = Piece.opponent_color_dict[player_color]

            if piece in Piece.partners_dict[opponent_color] or piece == " ":
                valid_moves.append((new_row, new_col))

        if valid_moves:  # if available moves
            # check if any move by the piece will expose the king
            for move in valid_moves:
                new_board = Piece.make_temp_move(board, (row, col), move)
                king_will_be_in_check = Piece.check_if_king_is_in_check(
                    new_board, player_color)
                if not king_will_be_in_check:
                    legal_moves.append(move)

        return legal_moves

    def squares_king_can_move_to(board, row, col, player_color):
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1),
                      (-1, 1), (-1, -1), (1, -1), (1, 1)]
        result = []
        valid_moves = []
        legal_moves = []

        # check for castling squares
        if player_color == "W":
            if not Piece.white_king_has_moved and not Piece.white_king_rook_has_moved:
                if board[7][5] == " " and board[7][6] == " ":
                    for r, c in [(7, 5), (7, 6)]:
                        new_board = Piece.make_temp_move(
                            board, (row, col), (r, c))
                        result.append(Piece.check_if_king_is_in_check(
                            new_board, player_color))
                        if result == [False, False]:
                            legal_moves.append((7, 5))
                            legal_moves.append((7, 6))
            if not Piece.white_king_has_moved and not Piece.white_queen_rook_has_moved:
                if board[7][1] == " " and board[7][2] == " " and board[7][3] == " ":
                    for r, c in [(7, 2), (7, 3)]:
                        new_board = Piece.make_temp_move(
                            board, (row, col), (r, c))
                        result.append(Piece.check_if_king_is_in_check(
                            new_board, player_color))
                        if result == [False, False]:
                            valid_moves.append((7, 2))
                            valid_moves.append((7, 3))
        else:
            if not Piece.black_king_has_moved and not Piece.black_king_rook_has_moved:
                if board[0][5] == " " and board[0][6] == " ":
                    for r, c in [(0, 5), (0, 6)]:
                        new_board = Piece.make_temp_move(
                            board, (row, col), (r, c))
                        result.append(Piece.check_if_king_is_in_check(
                            new_board, player_color))
                        if result == [False, False]:
                            valid_moves.append((0, 5))
                            valid_moves.append((0, 6))
            if not Piece.black_king_has_moved and not Piece.black_queen_rook_has_moved:
                if board[0][1] == " " and board[0][2] == " " and board[0][3] == " ":
                    for r, c in [(0, 2), (0, 3)]:
                        new_board = Piece.make_temp_move(
                            board, (row, col), (r, c))
                        result.append(Piece.check_if_king_is_in_check(
                            new_board, player_color))
                        if result == [False, False]:
                            valid_moves.append((0, 2))
                            valid_moves.append((0, 3))

        for dy, dx in directions:
            constant = row, col
            new_row, new_col = constant[0] + dy, constant[1] + dx
            if not Piece.square_is_within_bounds(new_row, new_col):
                continue

            if board[new_row][new_col] in Piece.partners_dict[player_color]:
                continue

            constant = new_row, new_col
            valid_moves.append((new_row, new_col))

        if valid_moves:  # if available moves
            # check if any move by the piece will expose the king
            for move in valid_moves:
                new_board = Piece.make_temp_move(board, (row, col), move)
                king_will_be_in_check = Piece.check_if_king_is_in_check(
                    new_board, player_color)
                # print('king cannot go there...:', king_will_be_in_check)
                # print()
                if not king_will_be_in_check:
                    legal_moves.append(move)

        return list(set(legal_moves))

    # def check_neigbor_is_a_king(board, row, col, color):
    #     directions = [(-1, 0), (1, 0), (0, 1), (0, -1),
    #                   (-1, 1), (-1, -1), (1, -1), (1, 1)]
    #     opponent_king = Piece.opponent_king_dict[color]
    #     for i, j in directions:
    #         constant = row, col
    #         new_row, new_col = constant[0] + i, constant[1] + j
    #         if not Piece.square_is_within_bounds(new_row, new_col):
    #             break
    #         if board[new_row][new_col] == opponent_king:
    #             return True

    #     return False

    def square_is_within_bounds(row, col):
        return row >= 0 and col >= 0 and row <= 7 and col <= 7

    def square_is_free_and_legal(board, row, col):
        try:
            return (row >= 0 and col >= 0 and row <= 7 and col <= 7) and board[row][col] == " "
        except IndexError:
            return False

    def display_board(board):
        for i in board:
            print(i, end='\n')
        # print()


board = [
    # 0    1    2    3    4    5    6    7
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 0
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 1
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 2
    [' ', ' ', ' ', 'bR', 'bR', ' ', ' ', ' '],  # 3
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 4
    [' ', ' ', ' ', ' ', 'wK', 'wN', ' ', ' '],  # 5
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 6
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 7
]

# situation where opponent king is near
# situation where the piece is protected
# situation where the piece is not protected and the king can capture


# Piece.white_king_has_moved = True
# a = Piece.check_if_piece_can_move(board, 5, 5, 'knight',  'W')
# a = Piece.check_if_piece_can_move(board, 5, 4, 'king',  'W')
# print(a)
