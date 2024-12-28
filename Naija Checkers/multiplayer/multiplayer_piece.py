
class Piece:
    white_directions = [(-1, 1), (-1, -1)]
    black_directions = [(1, -1), (1, 1)]
    opponent_color_dict = {"W": 'B', "B": 'W'}
    opponent_king_color_dict = {"W": 'BK', "B": 'WK'}
    enemy_pieces_dict = {"W": ['BK', "B"], "B": ['WK', "W"]}
    color_king_dict = {"W": 'WK', "B": 'BK'}

    def __init__(self, row, column, color, is_king, piece_id):
        self.row = row
        self.column = column
        self.color = color
        self.is_king = is_king
        self.piece_id = piece_id

    def get_captured_piece(board, from_coord, to_coord):
        capture_directions = [(-2, 2), (-2, -2), (2, -2), (2, 2)]
        all_directions = Piece.white_directions + Piece.black_directions
        from_row, from_col = from_coord
        x, y = to_coord
        to_row, to_col = int(x), int(y)

        for index, value in enumerate(capture_directions):
            r, c = value
            if (from_row+r, from_col+c) == (to_row, to_col):
                d1, d2 = all_directions[index]
                return from_row+d1, from_col+d2

    def get_piece_king_just_captured(board, from_coord, to_coord, piece_color):
        x, y = to_coord
        to_row, to_col = int(x), int(y)
        constant = from_coord

        direction = Piece.get_capture_direction(from_coord, (to_row, to_col))
        dy, dx = direction

        while True:
            nxt_row, nxt_col = constant[0]+dy, constant[1]+dx
            if board[nxt_row][nxt_col] in Piece.enemy_pieces_dict[piece_color]:
                break

            constant = nxt_row, nxt_col

        return nxt_row, nxt_col

    def get_capture_direction(from_coord, to_coord):
        all_directions = Piece.black_directions + Piece.white_directions

        for dir in all_directions:
            dy, dx = dir[0], dir[1]
            constant = from_coord

            while True:
                nxt_row, nxt_col = constant[0]+dy, constant[1]+dx
                if (nxt_row, nxt_col) == to_coord:
                    return dir

                if not Piece.square_is_within_bounds(nxt_row, nxt_col):
                    break

                constant = nxt_row, nxt_col

    def able_to_move(board, row, col, player_color):
        if player_color == "W":
            return Piece.check_white_movements(board, row, col)
        else:
            return Piece.check_black_movements(board, row, col)

    def check_captures_in_all_directions(board, row, col, color):
        capture_squares = []
        capture_pieces = []
        all_directions = Piece.black_directions + Piece.white_directions

        for dy, dx in all_directions:
            new_row, new_col = row + dy, col + dx
            if Piece.square_is_within_bounds(new_row, new_col):
                if board[new_row][new_col] in Piece.enemy_pieces_dict[color]:
                    n_row, n_col = new_row + dy, new_col + dx
                    if Piece.square_is_free_and_legal(board, n_row, n_col):
                        capture_squares.append((n_row, n_col))
                        capture_pieces.append((row, col))

        return (capture_pieces, capture_squares)

    def check_if_king_can_move(board, row, col):
        directions = Piece.black_directions + Piece.white_directions
        free_squares = []

        for dir in directions:
            dy, dx = dir[0], dir[1]
            new_constant = row, col

            while True:
                new_row, new_col = new_constant[0] + dy, new_constant[1] + dx
                if not Piece.square_is_free_and_legal(board, new_row, new_col):
                    break

                new_constant = new_row, new_col
                free_squares.append((new_row, new_col))

        return free_squares

    def check_if_king_can_capture(board, kings, piece_color):
        directions = Piece.black_directions + Piece.white_directions
        capture_squares = []

        for king in kings:
            row, col = king.row, king.column
            for dir in directions:
                dy, dx = dir[0], dir[1]
                new_constant = row, col

                while True:
                    nxt_row, nxt_col = new_constant[0] + \
                        dy, new_constant[1] + dx
                    # if the square is outside the board bounds
                    if not Piece.square_is_within_bounds(nxt_row, nxt_col):
                        break
                    # if the piece on square is same piece color
                    if board[nxt_row][nxt_col] == piece_color:
                        break
                    # if the piece on square is same king color
                    if board[nxt_row][nxt_col] == Piece.color_king_dict[piece_color]:
                        break
                    # if enemy is on the square
                    if board[nxt_row][nxt_col] in Piece.enemy_pieces_dict[piece_color]:
                        n_row, n_col = nxt_row + dy, nxt_col + dx
                        # check if the next square is free
                        if Piece.square_is_free_and_legal(board, n_row, n_col):
                            capture_squares.append((row, col))
                            break
                        else:
                            break
                    # if the square is free
                    if board[nxt_row][nxt_col] == " ":
                        # stay on the path and keep checking for opponent
                        new_constant = nxt_row, nxt_col

        return list(set(capture_squares))

    def check_king_capture_movement(board, row, col, piece_color):
        capture_squares = []
        directions = Piece.black_directions + Piece.white_directions

        for dir in directions:
            dy, dx = dir[0], dir[1]
            constant = row, col

            while True:
                nxt_row, nxt_col = constant[0] + dy, constant[1] + dx
                # if the square is outside the board bounds
                if not Piece.square_is_within_bounds(nxt_row, nxt_col):
                    break
                # if the piece on square is same piece color
                if board[nxt_row][nxt_col] == piece_color:
                    break
                # if the piece on square is same king color
                if board[nxt_row][nxt_col] == Piece.color_king_dict[piece_color]:
                    break
                # if the square is free
                if board[nxt_row][nxt_col] == " ":
                    # stay on the path and keep checking for opponent
                    constant = nxt_row, nxt_col
                # if enemy is on the square
                if board[nxt_row][nxt_col] in Piece.enemy_pieces_dict[piece_color]:
                    n_row, n_col = nxt_row + dy, nxt_col + dx
                    # check if the next square is free
                    if Piece.square_is_free_and_legal(board, n_row, n_col):
                        # keep checking for other captures on the same diagonal
                        # until the edge of the board or a piece is reach
                        # (keep saving the squares)
                        # check the diagonals of each saved squares
                        # if all the saved squares have no captures:
                        # king can jump to any of the squares
                        # else:
                        # save those squares (they are mandatory)
                        same_diagonal = Piece.check_same_diagonal(
                            board, dir, n_row, n_col)
                        other_diagonals = Piece.check_other_diagonals(
                            board, dir, same_diagonal, piece_color)
                        if other_diagonals:
                            capture_squares.extend(other_diagonals)
                        else:
                            capture_squares.extend(same_diagonal)
                        break
                    else:
                        break

        return capture_squares

    def check_single_king_capture(board, row, col, piece_color):
        directions = Piece.black_directions + Piece.white_directions

        for dir in directions:
            dy, dx = dir[0], dir[1]
            constant = row, col

            while True:
                nxt_row, nxt_col = constant[0] + dy, constant[1] + dx
                # if the square is outside the board bounds
                if not Piece.square_is_within_bounds(nxt_row, nxt_col):
                    break
                # if the piece on square is same piece color
                if board[nxt_row][nxt_col] == piece_color:
                    break
                # if the piece on square is same king color
                if board[nxt_row][nxt_col] == Piece.color_king_dict[piece_color]:
                    break
                # if the square is free
                if board[nxt_row][nxt_col] == " ":
                    # stay on the path and keep checking for opponent
                    constant = nxt_row, nxt_col
                # if enemy is on the square
                if board[nxt_row][nxt_col] in Piece.enemy_pieces_dict[piece_color]:
                    n_row, n_col = nxt_row + dy, nxt_col + dx
                    # check if the next square is free
                    if Piece.square_is_free_and_legal(board, n_row, n_col):
                        return ([[(row, col), (n_row, n_col)]])

        return []

    def check_for_mandatory_captures(board, pieces, color):
        capture_squares = []
        capture_pieces = []

        for id, obj in pieces:
            r, c = obj.row, obj.column
            row, col = int(r), int(c)

            can_capture = Piece.check_captures_in_all_directions(
                board, row, col, color)

            if can_capture:
                piece, square = can_capture[0], can_capture[1]
                capture_squares.extend(square)
                capture_pieces.extend(piece)

        return list(set(capture_pieces))

    def check_white_movements(board, row, col):
        available_squares = []

        for dy, dx in Piece.white_directions:
            new_row, new_col = row + dy, col + dx
            if Piece.square_is_free_and_legal(board, new_row, new_col):
                available_squares.append((new_row, new_col))

        return available_squares

    def check_black_movements(board, row, col):
        available_squares = []

        for dy, dx in Piece.black_directions:
            new_row, new_col = row + dy, col + dx
            if Piece.square_is_free_and_legal(board, new_row, new_col):
                available_squares.append((new_row, new_col))

        return available_squares

    def check_same_diagonal(board, dir, row, col):
        dy, dx = dir[0], dir[1]
        constant = row, col
        all_diagonals_after_capture = [constant]

        while True:
            nxt_row, nxt_col = constant[0]+dy, constant[1]+dx
            # if the square is outside the board bounds or a piece is reached
            if not Piece.square_is_free_and_legal(board, nxt_row, nxt_col):
                break

            constant = nxt_row, nxt_col
            all_diagonals_after_capture.append((constant))

        return all_diagonals_after_capture

    def check_other_diagonals(board, direction, diagonals, piece_color):
        captures = []
        if direction in [(1, 1), (-1, -1)]:
            other_directions = [(1, -1), (-1, 1)]
        else:
            other_directions = [(1, 1), (-1, -1)]

        for diag in diagonals:
            constant = diag[0], diag[1]
            for dir in other_directions:
                dy, dx = dir[0], dir[1]

                while True:
                    nxt_row, nxt_col = constant[0]+dy, constant[1]+dx
                    # if the square is outside the board bounds
                    if not Piece.square_is_within_bounds(nxt_row, nxt_col) or board[nxt_row][nxt_col] == piece_color or board[nxt_row][nxt_col] == Piece.color_king_dict[piece_color]:
                        break
                    if board[nxt_row][nxt_col] == " ":
                        # stay on the path and keep checking for opponent
                        constant = nxt_row, nxt_col
                    # if enemy is on the square
                    if board[nxt_row][nxt_col] in Piece.enemy_pieces_dict[piece_color]:
                        n_row, n_col = nxt_row + dy, nxt_col + dx
                        # check if the next square is free
                        if Piece.square_is_free_and_legal(board, n_row, n_col):
                            captures.append(diag)
                            break
                        else:
                            break

        return captures

    def square_is_within_bounds(row, col):
        return row >= 0 and col >= 0 and row <= 9 and col <= 9

    def square_is_free_and_legal(board, row, col):
        return (row >= 0 and col >= 0 and row <= 9 and col <= 9) and board[row][col] == " "
