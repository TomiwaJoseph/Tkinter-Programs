from game_piece import Piece


class Logic:
    player_turn = "W"
    white_pieces = []
    black_pieces = []
    king_is_in_check = False
    clicked_piece = None
    last_three_moves = []
    single_move = []
    fifty_move_counter = 0
    promotion_happenning = False
    color_dict = {"W": 'white', "B": 'black'}
    piece_color_dict = {"W": white_pieces, "B": black_pieces}
    light_squares = [(i, j) for i in range(8)
                     for j in range(8) if (i+j) % 2 == 0]
    draw_positions = [
        {
            "white": ["king"],
            "black": ["king"],
        },
        {
            "white": ["king", "bishop"],
            "black": ["king"],
        },
        {
            "white": ["king"],
            "black": ["king", "bishop"],
        },
        {
            "white": ["king", "knight"],
            "black": ["king"],
        },
        {
            "white": ["king"],
            "black": ["king", "knight"],
        },
        {
            "white": ["king", "bishop"],
            "black": ["king", "bishop"],
        },
    ]

    def handle_piece_click(self):
        # Piece.display_board(self.board)
        # Piece.black_king_has_moved = True
        # print(self.promotion_frame)
        if self.promotion_canvas:
            self.hide_promotion_option()
        clicked_piece = self.game_canvas.gettags("current")
        # print('clicked piece:', clicked_piece)
        id_value = self.game_canvas.find_withtag(clicked_piece[2])[0]
        # print('id value:', id_value)
        piece_object = Logic.get_piece_object(id_value)
        # print('piece object:', piece_object)
        # print('current player color:', Logic.player_turn)
        # if piece_object:
        #     print('piece color:', piece_object.piece_color)
        # print()

        if piece_object:
            Logic.reset_all_states(self)
            piece_type = piece_object.piece_type
            row, col = piece_object.row, piece_object.column
            if Logic.king_is_in_check:
                # check if the piece clicked can block or kill the attacker
                pass
            else:
                # check if the piece clicked is blocking a check
                piece_can_move = Piece.check_if_piece_can_move(
                    self.board, row, col, piece_type, Logic.player_turn)
                # print('squares:', piece_can_move)
                # print('piece_can_move:', piece_can_move)
                if piece_can_move:
                    squares_piece_can_move_to = piece_can_move
                    # print(squares_piece_can_move_to)
                    Logic.display_piece_visuals(
                        self, squares_piece_can_move_to, piece_object)

    def display_piece_visuals(self, squares, obj):
        """ display visual cues for the selected piece """

        Logic.highlight_selected_piece_square(self, obj)
        Logic.draw_dot_on_available_squares(self, squares)

    def highlight_selected_piece_square(self, obj):
        """ highlight the selected piece's square """

        x, y = obj.row, obj.column
        parsed_row_col = Logic.parse_row_col(x, y)
        piece_square = self.game_canvas.find_withtag(f"board-{parsed_row_col}")
        self.game_canvas.itemconfig(piece_square, fill='#3e9e3e')
        Logic.clicked_piece = obj

    def draw_dot_on_available_squares(self, squares):
        for r, c in squares:
            parsed_row_col = Logic.parse_row_col(r, c)
            square_coords = self.game_canvas.coords(f"board-{parsed_row_col}")
            # print("square_coords: ", square_coords)
            x1, y1, x2, y2 = square_coords
            invisible_rect = self.game_canvas.create_rectangle(
                x1, y1, x2, y2, fill="", outline="", tags=(parsed_row_col, (r, c), 'dot'))
            visible_rect = self.game_canvas.create_rectangle(
                x1, y1, x2, y2, width=3, outline='#f89c3b', tags=(parsed_row_col, (r, c), 'dot'))
            self.game_canvas.tag_bind(
                invisible_rect, "<Button-1>", lambda e: Logic.move_piece_to_square(self))
            c1, c2 = Logic.get_coordinate_center(square_coords)

            # Draw the highlight circle
            radius = 9
            the_dot = self.game_canvas.create_oval(c1-radius, c2-radius, c1+radius, c2+radius, tags=(
                parsed_row_col, (r, c), 'dot'), fill="#f89c3b", outline="")
            self.game_canvas.tag_bind(
                the_dot, "<Button-1>", lambda e: Logic.move_piece_to_square(self))

            # Logic.highlighted_squares.append((r, c))

    def move_piece_to_square(self):
        clicked_square = self.game_canvas.gettags("current")
        origin_x, origin_y = Logic.clicked_piece.row, Logic.clicked_piece.column
        clicked_piece_type = Logic.clicked_piece.piece_type
        # print('clicked square:', clicked_square)

        if clicked_square:
            destination_r, destination_c = clicked_square[1].split(' ')
            destination_r, destination_c = int(
                destination_r), int(destination_c)
            the_square_clicked = clicked_square[0]
            # print(f"board-{the_square_clicked[-2:]}")
            square_tag = self.game_canvas.find_withtag(
                f"board-{the_square_clicked[-2:]}")
            tag_coord = self.game_canvas.coords(square_tag[0])
            get_center = Logic.get_coordinate_center(tag_coord)
            dest_x, dest_y = get_center
            capture_happened = self.board[destination_r][destination_c] != " "

            if clicked_piece_type == "pawn" and (destination_r, destination_c) in Piece.promotion_dict[Logic.player_turn]:
                self.show_promotion_options(
                    Logic.player_turn, the_square_clicked, clicked_square[1])
                return
            else:
                Logic.move_selected_piece(
                    self, destination_r, destination_c, dest_x, dest_y, capture_happened)
                # save move to track threefold repetition
                Logic.save_move_for_threefold_repetition(
                    clicked_piece_type, (origin_x, origin_y), (destination_r, destination_c))
                Logic.save_last_single_move(
                    clicked_piece_type, capture_happened)
        else:  # pawn promotion
            piece_type = Piece.promotion_choice[0]
            player_color = Logic.player_turn.lower()
            tag1 = Piece.promotion_choice[1]
            dest_row, dest_col = Piece.promotion_choice[2].split(" ")
            square_tag = self.game_canvas.find_withtag(f"board-{tag1}")
            tag_coord = self.game_canvas.coords(square_tag[0])
            get_center = Logic.get_coordinate_center(tag_coord)
            dest_x, dest_y = get_center
            # create new promoted piece
            new_piece = self.game_canvas.create_image(dest_x, dest_y, image=self.all_images[f"{Logic.color_dict[Logic.player_turn]}_{piece_type}"], tags=(
                f'w{Piece.piece_symbol_dict[piece_type]}', tag1, f"{dest_row}-{dest_col}"))
            self.game_canvas.tag_bind(
                new_piece, "<Button-1>", lambda x: Logic.handle_piece_click(self))
            # delete previous pawn
            pawn_to_promote = self.game_canvas.find_withtag(
                f"{origin_x}-{origin_y}")
            self.game_canvas.delete(pawn_to_promote)
            # update piece objects
            Logic.update_piece_objects(Logic.clicked_piece.piece_id, new_piece, (int(
                dest_row), int(dest_col)), piece_type)
            # update board
            Logic.update_game_board(self, (origin_x, origin_y), (int(dest_row), int(
                dest_col)), f'{player_color}{Piece.piece_symbol_dict[piece_type]}')
            self.hide_promotion_option()
            Logic.save_move_for_threefold_repetition(
                clicked_piece_type, (origin_x, origin_y), (dest_row, dest_col))
            Logic.save_last_single_move('pawn', False)

        game_over, status = Logic.check_game_over(self.board)
        # print('game over status', (game_over, status), Logic.player_turn)
        # print()
        # if len(Logic.last_three_moves) == 6:
        #     print(Logic.last_three_moves)
        #     print()
        if not game_over:
            Logic.switch_current_player()
        else:
            # print("status:", status)
            Logic.reveal_game_outcome(self, status)

    def move_selected_piece(self, dest_row, dest_col, dest_x, dest_y, captured_happened):
        piece_symbol = {"rook": "R", "knight": "N", "pawn": "P",
                        "king": "K", "queen": "Q", "bishop": "B"}
        cols = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
        # captured_piece = self.game_canvas.find_withtag("2-5")
        # Piece.double_pawn_move = None
        piece_type = Logic.clicked_piece.piece_type
        # print('piece type:', piece_type)
        piece_id = Logic.clicked_piece.piece_id
        origin_x, origin_y = Logic.clicked_piece.row, Logic.clicked_piece.column
        just_castled_king_side = False
        just_castled_queen_side = False
        all_origin_positions = Piece.black_pawns_init_positon + \
            Piece.white_pawns_init_positon
        all_double_moves = Piece.white_first_double_moves + Piece.black_first_double_moves
        # set en passant option
        if (origin_x, origin_y) in all_origin_positions and (dest_row, dest_col) in all_double_moves:
            Piece.double_pawn_move = [(dest_row, dest_col), Logic.player_turn]
        # set casting option
        if piece_type == "rook":
            if Logic.player_turn == "W" and (origin_x, origin_y) == (7, 0):
                Piece.white_queen_rook_has_moved = True
            elif Logic.player_turn == "W" and (origin_x, origin_y) == (7, 7):
                Piece.white_king_rook_has_moved = True
            elif Logic.player_turn == "B" and (origin_x, origin_y) == (0, 0):
                Piece.black_queen_rook_has_moved = True
            elif Logic.player_turn == "B" and (origin_x, origin_y) == (0, 7):
                Piece.black_king_rook_has_moved = True

        if Piece.double_pawn_move:
            # print('reached here...')
            r, c = Piece.double_pawn_move[0]
            double_move_color = Piece.double_pawn_move[1]
            if Logic.player_turn != double_move_color:
                # print("reached too...")
                # print(dest_row, dest_col, (r, c))
                if ((dest_row+1, dest_col) == (r, c) and Logic.player_turn == "W") or (dest_row-1, dest_col) == (r, c) and Logic.player_turn == "B":
                    # print('reached here too...')
                    en_passant_piece = self.game_canvas.find_withtag(
                        f"{r}-{c}")
                    self.game_canvas.delete(en_passant_piece)
                    Logic.delete_piece_from_objects(r, c)

        if captured_happened:
            # get the piece in the destination
            captured_piece = self.game_canvas.find_withtag(
                f"{dest_row}-{dest_col}")
            # delete the piece from visuals
            self.game_canvas.delete(captured_piece)
            # delete the piece from piece objects
            Logic.delete_piece_from_objects(dest_row, dest_col)

        if Logic.player_turn == "W":
            # check if the moved piece is a king and can be castled
            if piece_type == "king" and not Piece.white_king_has_moved and not Piece.white_king_rook_has_moved and (dest_row, dest_col) == (7, 6):
                new_king = self.game_canvas.create_image(dest_x, dest_y, image=self.all_images[f"white_king"], tags=(
                    'wK', f"{cols[dest_col]}{dest_row}", f"{dest_row}-{dest_col}"))
                # print(f"{cols[dest_col]}{dest_row}")
                square_tag = self.game_canvas.find_withtag("board-F7")
                tag_coord = self.game_canvas.coords(square_tag[0])
                get_center = Logic.get_coordinate_center(tag_coord)
                rook_dest_x, rook_dest_y = get_center
                # print("root destination:", (rook_dest_x, rook_dest_y))
                new_rook = self.game_canvas.create_image(rook_dest_x, rook_dest_y, image=self.all_images[f"white_rook"], tags=(
                    'wR', "F7",  "7-5"))
                previous_king = self.game_canvas.find_withtag("7-4")
                previous_rook = self.game_canvas.find_withtag("7-7")
                self.game_canvas.delete(previous_king)
                self.game_canvas.delete(previous_rook)
                just_castled_king_side = True
            elif piece_type == "king" and not Piece.white_king_has_moved and not Piece.white_queen_rook_has_moved and (dest_row, dest_col) == (7, 2):
                new_king = self.game_canvas.create_image(dest_x, dest_y, image=self.all_images[f"white_king"], tags=(
                    'wK', f"{cols[dest_col]}{dest_row}", f"{dest_row}-{dest_col}"))
                # print(f"{cols[dest_col]}{dest_row}")
                square_tag = self.game_canvas.find_withtag("board-D7")
                tag_coord = self.game_canvas.coords(square_tag[0])
                get_center = Logic.get_coordinate_center(tag_coord)
                rook_dest_x, rook_dest_y = get_center
                # print("root destination:", (rook_dest_x, rook_dest_y))
                new_rook = self.game_canvas.create_image(rook_dest_x, rook_dest_y, image=self.all_images[f"white_rook"], tags=(
                    'wR', "D7",  "7-3"))
                previous_king = self.game_canvas.find_withtag("7-4")
                previous_rook = self.game_canvas.find_withtag("7-0")
                self.game_canvas.delete(previous_king)
                self.game_canvas.delete(previous_rook)
                just_castled_queen_side = True
            else:
                if piece_type == "pawn":
                    the_piece = self.game_canvas.create_image(dest_x, dest_y, image=self.all_images['white_pawn'], tags=(
                        'wP', f"{cols[dest_col]}{dest_row}", f"{dest_row}-{dest_col}"))
                else:
                    the_piece = self.game_canvas.create_image(dest_x, dest_y, image=self.all_images[f"white_{piece_type}"], tags=(
                        f'w{piece_symbol[piece_type]}', f"{cols[dest_col]}{dest_row}", f"{dest_row}-{dest_col}"))

            if just_castled_king_side:
                self.game_canvas.tag_bind(
                    new_king, "<Button-1>", lambda e: Logic.handle_piece_click(self))
                self.game_canvas.tag_bind(
                    new_rook, "<Button-1>", lambda e: Logic.handle_piece_click(self))
                # update the game board
                Logic.update_game_board(self, (7, 4), (7, 6), "wK")
                Logic.update_game_board(self, (7, 7), (7, 5), "wR")
                old_rook_obj = [
                    i for i in Logic.white_pieces if i.row == 7 and i.column == 7][0]
                Logic.update_piece_objects(piece_id, new_king, (7, 6), "king")
                Logic.update_piece_objects(
                    old_rook_obj.piece_id, new_rook, (7, 5), "rook")
            elif just_castled_queen_side:
                self.game_canvas.tag_bind(
                    new_king, "<Button-1>", lambda e: Logic.handle_piece_click(self))
                self.game_canvas.tag_bind(
                    new_rook, "<Button-1>", lambda e: Logic.handle_piece_click(self))
                # update the game board
                Logic.update_game_board(self, (7, 4), (7, 2), "wK")
                Logic.update_game_board(self, (7, 0), (7, 3), "wR")
                old_rook_obj = [
                    i for i in Logic.white_pieces if i.row == 7 and i.column == 0][0]
                Logic.update_piece_objects(piece_id, new_king, (7, 2), "king")
                Logic.update_piece_objects(
                    old_rook_obj.piece_id, new_rook, (7, 3), "rook")
            else:
                if piece_type == "king":
                    Piece.white_king_has_moved = True
                self.game_canvas.tag_bind(
                    the_piece, "<Button-1>", lambda e: Logic.handle_piece_click(self))
                # update the game board
                Logic.update_game_board(
                    self, (origin_x, origin_y), (dest_row, dest_col), f'w{piece_symbol[piece_type]}')
                origin_piece = self.game_canvas.find_withtag(
                    f"{origin_x}-{origin_y}")
                self.game_canvas.delete(origin_piece)
                Logic.update_piece_objects(
                    piece_id, the_piece, (dest_row, dest_col), piece_type)
        else:
            # check if the moved piece is a king and can be castled
            if piece_type == "king" and not Piece.black_king_has_moved and not Piece.black_king_rook_has_moved and (dest_row, dest_col) == (0, 6):
                new_king = self.game_canvas.create_image(dest_x, dest_y, image=self.all_images[f"black_king"], tags=(
                    'bK', f"{cols[dest_col]}{dest_row}", f"{dest_row}-{dest_col}"))
                # print(f"{cols[dest_col]}{dest_row}")
                square_tag = self.game_canvas.find_withtag("board-F0")
                tag_coord = self.game_canvas.coords(square_tag[0])
                get_center = Logic.get_coordinate_center(tag_coord)
                rook_dest_x, rook_dest_y = get_center
                new_rook = self.game_canvas.create_image(rook_dest_x, rook_dest_y, image=self.all_images[f"black_rook"], tags=(
                    'bR', "F0",  "0-5"))
                previous_king = self.game_canvas.find_withtag("0-4")
                previous_rook = self.game_canvas.find_withtag("0-7")
                self.game_canvas.delete(previous_king)
                self.game_canvas.delete(previous_rook)
                just_castled_king_side = True
            elif piece_type == "king" and not Piece.black_king_has_moved and not Piece.black_queen_rook_has_moved and (dest_row, dest_col) == (0, 2):
                new_king = self.game_canvas.create_image(dest_x, dest_y, image=self.all_images[f"black_king"], tags=(
                    'bK', f"{cols[dest_col]}{dest_row}", f"{dest_row}-{dest_col}"))
                # print(f"{cols[dest_col]}{dest_row}")
                square_tag = self.game_canvas.find_withtag("board-D0")
                tag_coord = self.game_canvas.coords(square_tag[0])
                get_center = Logic.get_coordinate_center(tag_coord)
                rook_dest_x, rook_dest_y = get_center
                # print("root destination:", (rook_dest_x, rook_dest_y))
                new_rook = self.game_canvas.create_image(rook_dest_x, rook_dest_y, image=self.all_images[f"black_rook"], tags=(
                    'bR', "C0",  "0-2"))
                previous_king = self.game_canvas.find_withtag("0-4")
                previous_rook = self.game_canvas.find_withtag("0-0")
                self.game_canvas.delete(previous_king)
                self.game_canvas.delete(previous_rook)
                just_castled_queen_side = True
            else:
                if piece_type == "pawn":
                    the_piece = self.game_canvas.create_image(dest_x, dest_y, image=self.all_images['black_pawn'], tags=(
                        'bP', f"{cols[dest_col]}{dest_row}", f"{dest_row}-{dest_col}"))
                else:
                    the_piece = self.game_canvas.create_image(dest_x, dest_y, image=self.all_images[f"black_{piece_type}"], tags=(
                        f'b{piece_symbol[piece_type]}', f"{cols[dest_col]}{dest_row}", f"{dest_row}-{dest_col}"))

            if just_castled_king_side:
                self.game_canvas.tag_bind(
                    new_king, "<Button-1>", lambda e: Logic.handle_piece_click(self))
                self.game_canvas.tag_bind(
                    new_rook, "<Button-1>", lambda e: Logic.handle_piece_click(self))
                # update the game board
                Logic.update_game_board(self, (0, 4), (0, 6), "bK")
                Logic.update_game_board(self, (0, 0), (0, 5), "bR")
                old_rook_obj = [
                    i for i in Logic.black_pieces if i.row == 0 and i.column == 7][0]
                Logic.update_piece_objects(piece_id, new_king, (0, 6), "king")
                Logic.update_piece_objects(
                    old_rook_obj.piece_id, new_rook, (0, 5), "rook")
            elif just_castled_queen_side:
                self.game_canvas.tag_bind(
                    new_king, "<Button-1>", lambda e: Logic.handle_piece_click(self))
                self.game_canvas.tag_bind(
                    new_rook, "<Button-1>", lambda e: Logic.handle_piece_click(self))
                # update the game board
                Logic.update_game_board(self, (0, 4), (0, 2), "bK")
                Logic.update_game_board(self, (0, 0), (0, 3), "bR")
                old_rook_obj = [
                    i for i in Logic.black_pieces if i.row == 0 and i.column == 0][0]
                Logic.update_piece_objects(piece_id, new_king, (0, 2), "king")
                Logic.update_piece_objects(
                    old_rook_obj.piece_id, new_rook, (0, 3), "rook")
            else:
                if piece_type == "king":
                    Piece.black_king_has_moved = True
                self.game_canvas.tag_bind(
                    the_piece, "<Button-1>", lambda e: Logic.handle_piece_click(self))
                # update the game board
                Logic.update_game_board(
                    self, (origin_x, origin_y), (dest_row, dest_col), f'b{piece_symbol[piece_type]}')
                origin_piece = self.game_canvas.find_withtag(
                    f"{origin_x}-{origin_y}")
                self.game_canvas.delete(origin_piece)
                Logic.update_piece_objects(
                    piece_id, the_piece, (dest_row, dest_col), piece_type)

        Logic.reset_all_states(self)

    def check_game_over(board):
        opponent_color = Piece.opponent_color_dict[Logic.player_turn]
        opponent_player_moves = Logic.get_player_moves(
            board, opponent_color)

        king_is_in_check = Piece.check_if_king_is_in_check(
            board, opponent_color)
        # winning move was made
        if king_is_in_check and not opponent_player_moves:
            return True, ["win", Logic.player_turn]
        # a stalemate occurred
        elif not king_is_in_check and not opponent_player_moves:
            return True, ["draw", "Stalemate"]

        draw, reason = Logic.check_game_is_a_draw()
        if draw:
            # print(draw, reason)
            return True, reason

        return False, "playing"

    def check_game_is_a_draw():
        if Logic.threefold_repetition():
            return True, ["draw", "Threefold repetition occurred..."]
        Logic.start_pawnless_move_counter()
        if Logic.fifty_move_counter >= 50:
            return True, ["draw", "No pawn move or capture in the last 50 move"]
        # Insufficient materials
        if Logic.insufficient_materials():
            return True, ["draw", "Insufficient materials to checkmate"]
        return False, None

    def insufficient_materials():
        pass

    def start_pawnless_move_counter():
        if len(Logic.single_move) == 2:
            # if the last move is a pawn move or a capture not made
            # restart the move counter
            white_move = Logic.single_move[0]
            black_move = Logic.single_move[1]
            if (white_move[0] == "pawn" or white_move[1] == True) or (black_move[0] == "pawn" or black_move[1] == True):
                Logic.fifty_move_counter = 0
            else:
                # increment the counter
                Logic.fifty_move_counter += 1
            Logic.single_move = []

    def threefold_repetition():
        if len(Logic.last_three_moves) != 6:
            return False
        return (Logic.last_three_moves[0] == Logic.last_three_moves[2] == Logic.last_three_moves[4]) and (Logic.last_three_moves[1] == Logic.last_three_moves[3])

    def reveal_game_outcome(self, status):
        game_status = status[0]
        if game_status == "win":
            winner_color = status[1]
            if winner_color == "W":
                self.show_game_outcome("White wins!")
            else:
                self.show_game_outcome("Black wins!")
        else:
            reason = status[1]
            # print('reason:', reason)
            self.show_game_outcome(None, reason)
        pass

    def get_player_moves(board, player_color):
        legal_moves = []
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece in Piece.partners_dict[player_color]:
                    piece_type = Piece.piece_type_dict[piece[-1]]
                    piece_can_move = Piece.check_if_piece_can_move(
                        board, row, col, piece_type, player_color)
                    if piece_can_move:
                        legal_moves.extend(piece_can_move)
        return legal_moves

    def save_move_for_threefold_repetition(piece, origin, destination):
        the_move = f"{piece}{origin}{destination}"
        # print(the_move)
        if Logic.last_three_moves == []:
            Logic.last_three_moves.append([the_move])
        else:
            if len(Logic.last_three_moves[-1]) == 1:
                Logic.last_three_moves[-1].append(the_move)
            else:
                Logic.last_three_moves.append([the_move])

        if len(Logic.last_three_moves) > 6:
            Logic.last_three_moves.pop(0)

    def save_last_single_move(piece, has_captured):
        activity = piece, has_captured
        Logic.single_move.append(activity)
        # if Logic.player_turn == "W":
        #     Logic.single_move = []

    def switch_current_player():
        if Logic.player_turn == "W":
            Logic.player_turn = "B"
        else:
            Logic.player_turn = "W"

    def update_game_board(self, origin, destination, piece):
        # print('origin, destination, piece')
        # print(origin, destination, piece)
        orig_r, orig_c = origin
        dest_r, dest_c = destination
        self.board[orig_r][orig_c] = " "
        self.board[dest_r][dest_c] = piece

    def delete_piece_from_objects(row, col):
        opponent_color = Piece.opponent_color_dict[Logic.player_turn]
        current_player_pieces = Logic.piece_color_dict[opponent_color]
        for index, piece in enumerate(current_player_pieces):
            if piece.row == row and piece.column == col:
                break

        Logic.piece_color_dict[opponent_color].pop(index)

    def update_piece_objects(old_id, new_id, destination, piece_type):
        current_player_pieces = Logic.piece_color_dict[Logic.player_turn]
        row, col = destination
        for index, value in enumerate(current_player_pieces):
            if value.piece_id == old_id:
                break

        # delete previous object and create new object
        piece = Piece(row, col, piece_type, new_id, Logic.player_turn)
        Logic.piece_color_dict[Logic.player_turn].pop(index)
        Logic.piece_color_dict[Logic.player_turn].append(piece)

    def parse_row_col(r, c):
        positions = {
            0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F',  6: 'G', 7: 'H', 8: 'I', 9: 'J'
        }
        return f'{positions.get(c)}{r}'

    def get_piece_object(id_value):
        color = Logic.player_turn
        for obj in Logic.piece_color_dict[color]:
            if obj.piece_id == id_value:
                return obj

        return None

    def reset_all_states(self):
        # delete the dot(s)
        self.game_canvas.delete('dot')
        # remove previous click highlights
        Logic.remove_previous_click_highlights(self)
        # unbind all squares with highlighted dots
        # Logic.unbind_all_squares_with_highlighted_dots(self)

    def remove_previous_click_highlights(self):
        """ remove highlights from previous clicked piece's square """

        if Logic.clicked_piece:
            x, y = Logic.clicked_piece.row, Logic.clicked_piece.column
            parsed_row_col = Logic.parse_row_col(int(x), int(y))
            the_square = self.game_canvas.find_withtag(
                f"board-{parsed_row_col}")
            if (x, y) in Logic.light_squares:
                self.game_canvas.itemconfig(
                    the_square, fill=self.BOARD_LIGHT_COLOUR)
            else:
                self.game_canvas.itemconfig(
                    the_square, fill=self.BOARD_DARK_COLOUR)

    def get_coordinate_center(coordinate):
        x1, y1, x2, y2 = coordinate
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        return cx, cy

    def display_board(board):
        for i in board:
            print(i, end='\n')
        print()
