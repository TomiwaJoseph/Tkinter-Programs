from .multiplayer_piece import Piece


class Logic:
    # ============ Multiplayer Variables =============
    white_pieces = []
    black_pieces = []
    highlighted_squares = []
    clicked_piece = None
    must_capture = False
    last_move = {}
    move_count = 0
    draw_position_count = 0
    piece_was_captured = False
    current_player_color = "W"
    BOARD_DARK_COLOUR = "#AF8968"
    piece_type_dict = {True: "king", False: "piece"}
    color_dict = {"W": 'white', "B": '#1a1a1a'}
    opponent_color_dict = {"W": 'B', "B": 'W'}
    all_positions = []  # takes record of all moves
    white_crown_squares = [(0, 0), (0, 2), (0, 4), (0, 6), (0, 8)]
    black_crown_squares = [(9, 1), (9, 3), (9, 5), (9, 7), (9, 9)]
    piece_color_dict = {"W": white_pieces, "B": black_pieces}
    draw_position = [
        {
            "player_1": {"kings": 2, "minors": 0},
            "player_2": {"kings": 1, "minors": 0},
        },
        {
            "player_1": {"kings": 1, "minors": 0},
            "player_2": {"kings": 1, "minors": 0},
        }
    ]
    draw_position_for_16_moves = [
        {
            "player_1": {"kings": 3, "minors": 0},
            "player_2": {"kings": 1, "minors": 0},
        },
        {
            "player_1": {"kings": 2, "minors": 1},
            "player_2": {"kings": 1, "minors": 0},
        },
        {
            "player_1": {"kings": 1, "minors": 2},
            "player_2": {"kings": 1, "minors": 0},
        }
    ]

    def reset_all_variables():
        Logic.white_pieces = []
        Logic.black_pieces = []
        Logic.highlighted_squares = []
        Logic.clicked_piece = None
        Logic.must_capture = False
        Logic.last_move = {}
        Logic.move_count = 0
        Logic.draw_position_count = 0
        Logic.piece_was_captured = False
        Logic.current_player_color = "W"
        Logic.all_positions = []
        Logic.piece_color_dict = {
            "W": Logic.white_pieces, "B": Logic.black_pieces}

    def handle_piece_click(self):
        """ handle event from a piece click """

        clicked_piece = self.game_canvas.gettags("current")
        id_value = self.game_canvas.find_withtag(clicked_piece[2])[0]
        piece_object = Logic.get_piece_object(id_value)

        if piece_object and piece_object.color == Logic.current_player_color:
            Logic.reset_event_states(self)
            row, col = piece_object.row, piece_object.column

            if Logic.must_capture:
                if piece_object.is_king:
                    squares_capture_can_happen = Piece.check_king_capture_movement(
                        self.board, row, col, Logic.current_player_color)
                    Logic.display_visuals_for_piece(
                        self, piece_object, squares_capture_can_happen)
                    Logic.piece_was_captured = True
                else:
                    squares_capture_can_happen = Piece.check_captures_in_all_directions(
                        self.board, row, col, Logic.current_player_color)
                    squares = squares_capture_can_happen[1]
                    Logic.display_visuals_for_piece(
                        self, piece_object, squares)
                    Logic.piece_was_captured = True
                return

            if piece_object.is_king:
                squares_king_can_move_to = Piece.check_if_king_can_move(
                    self.board, row, col)
                if squares_king_can_move_to:
                    Logic.display_visuals_for_piece(
                        self, piece_object, squares_king_can_move_to)
            else:
                squares_piece_can_move = Piece.able_to_move(
                    self.board, row, col, Logic.current_player_color)
                if squares_piece_can_move:
                    Logic.display_visuals_for_piece(
                        self, piece_object, squares_piece_can_move)

    def display_visuals_for_piece(self, obj, squares):
        """ display visual cues for the selected piece """

        Logic.highlight_selected_piece_square(self, obj)
        Logic.draw_dot_on_available_squares(self, squares)

    def highlight_selected_piece_square(self, obj):
        """ highlight the selected piece's square """

        x, y = obj.row, obj.column
        parsed_row_col = Logic.parse_row_col(x, y)
        piece_square = self.game_canvas.find_withtag(parsed_row_col)
        self.game_canvas.itemconfig(piece_square, fill='green')
        Logic.clicked_piece = obj

    def draw_dot_on_available_squares(self, available_squares):
        """ draw dots on squares currently selected piece can move to """

        for r, c in available_squares:
            parsed_row_col = Logic.parse_row_col(r, c)
            highlighted_square = self.game_canvas.find_withtag(parsed_row_col)
            # bind the square to event listener
            self.game_canvas.tag_bind(
                highlighted_square, "<Button-1>", lambda e: Logic.move_piece_to_square(self))

            available = self.game_canvas.coords(parsed_row_col)
            x0, y0 = available[0], available[1]

            # Draw the highlight circle
            radius = 8
            the_dot = self.game_canvas.create_oval(x0+30-radius, y0+30-radius, x0+30+radius, y0+30+radius, tags=(
                parsed_row_col, (r, c), 'dot'), fill=f'{Logic.color_dict.get(Logic.current_player_color)}', outline="")
            self.game_canvas.tag_bind(
                the_dot, "<Button-1>", lambda e: Logic.move_piece_to_square(self))

            Logic.highlighted_squares.append((r, c))

    def get_piece_object(value):
        color = Logic.current_player_color
        for id, obj in Logic.piece_color_dict[color]:
            if id == value:
                return obj

        return None

    def get_coordinate_center(coordinate):
        x1, y1, x2, y2 = coordinate
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        return cx, cy

    def get_animation_directon(origin, destination):
        dx, dy = 0, 0
        ori_x, ori_y = origin
        dest_x, dest_y = destination
        dx = -1 if ori_x > dest_x else 1
        dy = -1 if ori_y > dest_y else 1
        return dx, dy

    def animate_piece(self, piece_id, destination, direction, other_details):
        piece_position = self.game_canvas.coords(piece_id)
        current_x, current_y = piece_position
        dx, dy = direction
        self.game_canvas.move(piece_id, dx, dy)

        if round(current_x, 1) != destination:
            # Logic.animation_is_done = False
            self.game_canvas.after(
                2, Logic.animate_piece, self, piece_id, destination, direction, other_details)
        else:
            r, c, x0, y0 = other_details
            the_piece = Logic.move_selected_piece(self, r, c, x0, y0)
            the_piece_obj = Logic.get_piece_object(the_piece)

            if Logic.piece_was_captured:
                # check if more captures can be made
                if the_piece_obj.is_king:
                    piece_can_still_capture = Piece.check_if_king_can_capture(
                        self.board, [the_piece_obj], Logic.current_player_color)
                else:
                    piece_can_still_capture = Piece.check_captures_in_all_directions(
                        self.board, the_piece_obj.row, the_piece_obj.column, Logic.current_player_color)

                if type(piece_can_still_capture) == list:  # piece is king
                    piece_square = piece_can_still_capture
                else:
                    piece_square = piece_can_still_capture[0]

                if piece_square:  # more captures
                    Logic.reset_event_states(self)
                    Logic.remove_all_highlights(self)

                    # highlight the piece that just captured
                    Logic.highlight_mandatory_capture_pieces(
                        self, piece_square)
                    # make sure only that piece can move
                    the_piece_id = [
                        id for id, obj in Logic.piece_color_dict[Logic.current_player_color] if obj == the_piece_obj][0]
                    Logic.unbind_all_except_mandatory_pieces(
                        self, [the_piece_id])
                else:  # no more caputures
                    # check if the just moved piece has
                    # no more captures and can be crowned
                    can_be_crowned = Logic.know_if_piece_can_be_crowned(r, c)
                    if can_be_crowned and not the_piece_obj.is_king:
                        Logic.crown_moved_piece(self, the_piece)

                    Logic.switch_current_player()
                    # Logic.all_positions.append(self.board)
                    Logic.remove_all_highlights(self)
                    Logic.must_capture = False
                    Logic.bind_all_pieces(self)
                    Logic.check_if_next_move_is_mandatory(self)
            else:
                # check if the just moved piece can be crowned
                can_be_crowned = Logic.know_if_piece_can_be_crowned(r, c)
                if can_be_crowned and not the_piece_obj.is_king:
                    Logic.crown_moved_piece(self, the_piece)

                Logic.must_capture = False
                Logic.switch_current_player()
                # Logic.all_positions.append(self.board)
                Logic.check_if_next_move_is_mandatory(self)

            game_over, status = Logic.check_game_is_over(
                self.board, Logic.current_player_color, Logic.opponent_color_dict[Logic.current_player_color])
            if game_over and not Logic.must_capture:
                return Logic.reveal_game_outcome(self, status)

    def move_piece_to_square(self):
        clicked_squared = self.game_canvas.gettags("current")
        piece_id = Logic.clicked_piece.piece_id
        piece_to_move_coords = self.game_canvas.coords(
            f"{Logic.current_player_color}{Logic.clicked_piece.row}{Logic.clicked_piece.column}")
        r, c = clicked_squared[1].split(' ')
        the_square_clicked = clicked_squared[0]

        destination_coords = self.game_canvas.coords(the_square_clicked)
        destination_center = Logic.get_coordinate_center(destination_coords)
        x0, y0, = destination_coords[0], destination_coords[1]
        direction = Logic.get_animation_directon(
            piece_to_move_coords, destination_center)
        other_details = [r, c, x0, y0]
        Logic.animate_piece(
            self, piece_id, destination_center[0], direction, other_details)

    def move_selected_piece(self, r, c, x0, y0):
        piece_is_king = Logic.clicked_piece.is_king

        if Logic.current_player_color == "W":
            if Logic.clicked_piece.is_king:
                the_piece = self.game_canvas.create_image(
                    x0+30, y0+30, image=self.all_images['light_king'], tags=('W', (r, c), f"W{r}{c}", "BKING"))
            else:
                the_piece = self.game_canvas.create_image(
                    x0+30, y0+30, image=self.all_images['light_piece'], tags=('W', (r, c), f"W{r}{c}"))
        else:
            if Logic.clicked_piece.is_king:
                the_piece = self.game_canvas.create_image(
                    x0+30, y0+30, image=self.all_images['dark_king'], tags=('B', (r, c), f"B{r}{c}", "BKING"))
            else:
                the_piece = self.game_canvas.create_image(
                    x0+30, y0+30, image=self.all_images['dark_piece'], tags=('B', (r, c), f"B{r}{c}"))

        self.game_canvas.tag_bind(
            the_piece, "<Button-1>", lambda e: Logic.handle_piece_click(self))

        x, y = Logic.clicked_piece.row, Logic.clicked_piece.column

        # delete previous white piece or black piece
        if Logic.current_player_color == "W":
            previous_piece = self.game_canvas.find_withtag(f'W{x}{y}')
        else:
            previous_piece = self.game_canvas.find_withtag(f'B{x}{y}')

        self.game_canvas.delete(previous_piece)

        # know if a capture just happened
        if Logic.piece_was_captured:
            if piece_is_king:
                captured_piece = Piece.get_piece_king_just_captured(
                    self.board, (x, y), (r, c), Logic.current_player_color)
            else:
                captured_piece = Piece.get_captured_piece(
                    self.board, (x, y), (r, c))

            row, col = captured_piece
            self.board[row][col] = " "
            piece_color = Logic.opponent_color_dict[Logic.current_player_color]
            piece_to_be_deleted = self.game_canvas.find_withtag(
                f'{piece_color}{row}{col}')
            self.game_canvas.delete(piece_to_be_deleted)

            # delete object from piece's list of objects
            for piece in Logic.piece_color_dict[Logic.opponent_color_dict[Logic.current_player_color]]:
                id, obj = piece[0], piece[1]
                if id == piece_to_be_deleted[0]:
                    break

            Logic.piece_color_dict[Logic.opponent_color_dict[Logic.current_player_color]].remove(
                piece)

        Logic.reset_event_states(self)
        # update game board state
        Logic.update_game_board_state(self, piece_is_king, (x, y), (r, c))
        # update piece object states
        Logic.update_piece_state(
            Logic.clicked_piece.piece_id, the_piece, r, c, piece_is_king)

        return the_piece

    def reset_event_states(self):
        """ reset the gui to its neutral state """

        # delete the dot(s)
        self.game_canvas.delete('dot')
        # remove previous click highlights
        Logic.remove_previous_click_highlights(self)
        # unbind all squares with highlighted dots
        Logic.unbind_all_squares_with_highlighted_dots(self)

    def update_game_board_state(self, piece_is_king, previous, new):
        king_dict = {"W": "WK", "B": "BK"}
        x, y = previous
        r, c = new
        self.board[x][y] = " "

        if piece_is_king:
            self.board[int(r)][int(
                c)] = king_dict[Logic.current_player_color]
        else:
            self.board[int(r)][int(c)] = Logic.current_player_color

        board_copy = [r[:] for r in self.board]
        Logic.all_positions.append(board_copy)

    def update_piece_state(old_piece_id, new_piece, r, c, piece_state):
        for piece_id in range(len(Logic.piece_color_dict[Logic.current_player_color])):
            if Logic.piece_color_dict[Logic.current_player_color][piece_id][1].piece_id == old_piece_id:
                break

        # delete the previous piece object and create new piece
        piece = Piece(int(r), int(c), Logic.current_player_color,
                      piece_state, new_piece)
        Logic.piece_color_dict[Logic.current_player_color].pop(piece_id)
        Logic.piece_color_dict[Logic.current_player_color].append(
            (new_piece, piece))

    def unbind_all_squares_with_highlighted_dots(self):
        for r, c in Logic.highlighted_squares:
            parsed_row_col = Logic.parse_row_col(r, c)
            highlights = self.game_canvas.find_withtag(parsed_row_col)
            self.game_canvas.tag_unbind(highlights, "<Button-1>")

        Logic.highlighted_squares = []

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
            self.show_game_outcome(None, reason)

    def check_if_next_move_is_mandatory(self):
        pieces = [(id, obj)
                  for id, obj in Logic.piece_color_dict[Logic.current_player_color] if not obj.is_king]
        kings = [
            obj for id, obj in Logic.piece_color_dict[Logic.current_player_color] if obj.is_king]
        mandatory_king_capture = []
        if kings:
            mandatory_king_capture = Piece.check_if_king_can_capture(
                self.board, kings, Logic.current_player_color)

        mandatory_piece_capture = Piece.check_for_mandatory_captures(
            self.board, pieces, Logic.current_player_color)
        mandatory_captures = mandatory_king_capture + mandatory_piece_capture

        if mandatory_captures != []:
            # highlight the mandatory capture piece square(s)
            Logic.highlight_mandatory_capture_pieces(
                self, mandatory_captures)
            # remove click events from all pieces excluding the mandatory pieces
            pieces_to_bind = [piece[0] for piece in Logic.piece_color_dict[Logic.current_player_color]
                              if (piece[1].row, piece[1].column) in mandatory_captures]
            Logic.unbind_all_except_mandatory_pieces(self, pieces_to_bind)
            Logic.must_capture = True
        else:
            Logic.must_capture = False
            Logic.bind_all_pieces(self)

    def bind_all_pieces(self):
        """ bind all pieces to click event listeners """

        white_pieces = self.game_canvas.find_withtag("W")
        black_pieces = self.game_canvas.find_withtag("B")

        for i in white_pieces:
            self.game_canvas.tag_bind(
                i, "<Button-1>", lambda e: Logic.handle_piece_click(self))

        for i in black_pieces:
            self.game_canvas.tag_bind(
                i, "<Button-1>", lambda e: Logic.handle_piece_click(self))

    def remove_previous_click_highlights(self):
        """ remove highlights from previous clicked piece's square """

        if Logic.clicked_piece:
            x, y = Logic.clicked_piece.row, Logic.clicked_piece.column
            parsed_row_col = Logic.parse_row_col(int(x), int(y))
            the_square = self.game_canvas.find_withtag(parsed_row_col)
            self.game_canvas.itemconfig(
                the_square, fill=Logic.BOARD_DARK_COLOUR)

    def know_if_piece_can_be_crowned(r, c):
        color_dict = {"W": Logic.white_crown_squares,
                      "B": Logic.black_crown_squares}

        if (int(r), int(c)) in color_dict[Logic.current_player_color]:
            return True

        return False

    def crown_moved_piece(self, value):
        """ turn moved piece to a king """

        color = Logic.current_player_color

        piece_obj = Logic.get_piece_object(value)
        r, c = piece_obj.row, piece_obj.column
        parse_row_col = Logic.parse_row_col(r, c)
        the_square = self.game_canvas.find_withtag(parse_row_col)
        coords = self.game_canvas.coords(the_square)
        x0, y0, x1, y1 = coords

        # delete the piece
        get_piece = self.game_canvas.find_withtag(f'{color}{r}{c}')
        self.game_canvas.delete(get_piece)

        if color == "W":
            new_piece = self.game_canvas.create_image(
                x0+30, y0+30, image=self.all_images['light_king'], tags=('W', (r, c), f"W{r}{c}", "WKING"))
            self.board[r][c] = "WK"
        else:
            new_piece = self.game_canvas.create_image(
                x0+30, y0+30, image=self.all_images['dark_king'], tags=('B', (r, c), f"B{r}{c}", "BKING"))
            self.board[r][c] = "BK"

        self.game_canvas.tag_bind(
            new_piece, "<Button-1>", lambda e: Logic.handle_piece_click(self))
        Logic.update_piece_state(value, new_piece, r, c, True)

    def switch_current_player():
        Logic.piece_was_captured = False
        if Logic.current_player_color == "W":
            Logic.current_player_color = "B"
        else:
            Logic.current_player_color = "W"

    def parse_row_col(r, c):
        positions = {
            0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F',  6: 'G', 7: 'H', 8: 'I', 9: 'J'
        }
        return f'{positions.get(c)}{r}'

    def remove_all_highlights(self):
        all_pieces = Logic.white_pieces + Logic.black_pieces
        for id, obj in all_pieces:
            x, y = obj.row, obj.column
            parsed_row_col = Logic.parse_row_col(int(x), int(y))
            the_square = self.game_canvas.find_withtag(parsed_row_col)
            self.game_canvas.itemconfig(
                the_square, fill=Logic.BOARD_DARK_COLOUR)

    def highlight_mandatory_capture_pieces(self, pieces):
        """ highlight the mandatory capture square(s) """

        for piece in pieces:
            the_tags = self.game_canvas.gettags(piece)
            x, y = the_tags[1].split(" ")
            parse_row_col = Logic.parse_row_col(int(x), int(y))
            the_square = self.game_canvas.find_withtag(parse_row_col)
            self.game_canvas.itemconfig(the_square, fill='orangered')

    def unbind_all_except_mandatory_pieces(self, squares):
        """ unbind all pieces except the mandatory piece(s) """

        for i in squares:
            the_tag = self.game_canvas.find_withtag(i)
            self.game_canvas.tag_bind(
                the_tag, "<Button-1>", lambda e: Logic.handle_piece_click(self))

    def check_game_is_over(board, current_player, opponent_player):
        piece_can_move = []
        for id, obj in Logic.piece_color_dict[Logic.current_player_color]:
            row, col = obj.row, obj.column
            if obj.is_king:
                piece_can_move.extend(
                    Piece.check_if_king_can_move(board, row, col))
                piece_can_move.extend(Piece.check_if_king_can_capture(
                    board, [obj], Logic.current_player_color))
            else:
                piece_can_move.extend(Piece.able_to_move(
                    board, row, col, Logic.current_player_color))
                piece_can_move.extend(Piece.check_captures_in_all_directions(
                    board, row, col, Logic.current_player_color)[0])

        if len(Logic.piece_color_dict[current_player]) == 0 or not piece_can_move:
            return True, ["win", opponent_player]
        if len(Logic.piece_color_dict[opponent_player]) == 0:
            return True, ["win", current_player]

        draw, reason = Logic.check_game_is_a_draw()
        if draw:
            return True, ["draw", reason]

        return False, "playing"

    def check_game_is_a_draw():
        Logic.start_move_counter()
        if Logic.move_count >= 25:
            return True, "No capture in the last 25 moves"
        if Logic.get_draw_positions():
            return True, "Remaining pieces will lead to a draw"

        Logic.start_draw_position_counter()
        if Logic.draw_position_count >= 16:
            return True, "Insufficient pieces for the last 16 moves"
        return False, None

    def start_move_counter():
        the_last_move = Logic.last_move
        if the_last_move != {}:
            piece = the_last_move['piece_type']
            piece_movement = the_last_move['movement_type']
            if piece == "king" and piece_movement == "movement":
                Logic.move_count += 1
            else:
                Logic.move_count = 0

    def get_draw_positions():
        # if the board has the position return true
        if Logic.check_occurence(Logic.draw_position):
            return True
        else:
            return False

    def start_draw_position_counter():
        # if the board has the 16 move position, start the counter
        if Logic.check_occurence(Logic.draw_position_for_16_moves):
            Logic.draw_position_count += 1
        else:
            Logic.draw_position_count = 0

    def check_occurence(position):
        p1_color = Logic.current_player_color
        p2_color = Logic.opponent_color_dict[Logic.current_player_color]
        player_one_kings = [
            obj for id, obj in Logic.piece_color_dict[p1_color] if obj.is_king]
        player_one_minors = len(
            Logic.piece_color_dict[p1_color]) - len(player_one_kings)
        player_two_kings = [
            obj for id, obj in Logic.piece_color_dict[p2_color] if obj.is_king]
        player_two_minors = len(
            Logic.piece_color_dict[p2_color]) - len(player_two_kings)

        for pieces in position:
            players = list(pieces.keys())
            for player in players:
                opponent = players[0] if players[1] else players[1]
                if (pieces[player]["kings"] == len(player_one_kings) and pieces[player]["minors"] == player_one_minors and pieces[opponent]["kings"] == len(player_two_kings) and pieces[opponent]["minors"] == player_two_minors) or (pieces[opponent]["kings"] == len(player_one_kings) and pieces[opponent]["minors"] == player_one_minors and pieces[player]["kings"] == len(player_two_kings) and pieces[player]["minors"] == player_two_minors):
                    return True
        return False

    def display_board(board):
        for i in board:
            print(i, end='\n')
        print()
