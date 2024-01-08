from tkinter import Label, Frame, Tk, Canvas, Button, CENTER, IntVar, Checkbutton, messagebox
from PIL import ImageTk, Image
import copy

root = Tk
GAME_DIFFICULTY = 0
AI_TO_PLAY_BLACK = False


class Switch(root):
    def __init__(self):
        root.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(x=0, y=0, relheight=1, relwidth=1)


class StartPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.configure(self, bg="#101820")
        self.root = root
        self.root.title("Intro Page")
        self.root.geometry('530x350+368+179')
        self.root.resizable(0, 0)
        # ======= Title =====================
        Label(self.master, text='Othello', font=('fira code', 40),
              fg='#505050', bg='#fff').place(relx=0.5, rely=0.32, anchor="center")
        Label(self.master, text='Othello', font=('fira code', 40),
              fg='#fff', bg='#101820').place(relx=0.5, rely=0.305, anchor="center")
        Button(self.master, text='AI', width=10, font=('fira code medium', 14), bd=0, fg='#101820', bg='#fff',
               command=lambda: self.master.switch_frame(SettingsPage)).place(relx=0.32, rely=0.59, anchor="center")
        Button(self.master, text='2 Players', width=14, font=('fira code medium', 14), bd=0, fg='#101820', bg='#fff',
               command=lambda: self.master.switch_frame(HumanPage)).place(relx=0.63, rely=0.59, anchor="center")


class SettingsPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.configure(self, bg="#101820")
        self.root = root
        self.root.title("Othello | Human Page")
        self.root.geometry('530x350+368+179')
        # self.root.geometry('1000x700+200+20')
        self.root.resizable(0, 0)
        # ============ UI =============
        self.canvas = Canvas(bg='#101820', width=400, height=150)
        self.canvas.place(relx=0.5, rely=0.42, anchor=CENTER)

        # one star image
        self.one_star = Image.open('./assets/one-star.png')
        self.one_star = self.one_star.resize(
            (80, 80), Image.LANCZOS)
        self.one_star = ImageTk.PhotoImage(self.one_star)
        # two star image
        self.two_star = Image.open('./assets/two-star.png')
        self.two_star = self.two_star.resize(
            (80, 80), Image.LANCZOS)
        self.two_star = ImageTk.PhotoImage(self.two_star)
        # three star image
        self.three_star = Image.open('./assets/three-star.png')
        self.three_star = self.three_star.resize(
            (80, 80), Image.LANCZOS)
        self.three_star = ImageTk.PhotoImage(self.three_star)

        # one star checked image
        self.one_star_checked = Image.open('./assets/one-star-checked.png')
        self.one_star_checked = self.one_star_checked.resize(
            (80, 80), Image.LANCZOS)
        self.one_star_checked = ImageTk.PhotoImage(self.one_star_checked)
        # two star checked image
        self.two_star_checked = Image.open('./assets/two-star-checked.png')
        self.two_star_checked = self.two_star_checked.resize(
            (80, 80), Image.LANCZOS)
        self.two_star_checked = ImageTk.PhotoImage(self.two_star_checked)
        # three star checked image
        self.three_star_checked = Image.open('./assets/three-star-checked.png')
        self.three_star_checked = self.three_star_checked.resize(
            (80, 80), Image.LANCZOS)
        self.three_star_checked = ImageTk.PhotoImage(self.three_star_checked)

        self.canvas.create_image(
            80, 60, image=self.one_star, tags="one_star")
        self.canvas.create_image(
            200, 60, image=self.two_star, tags="two_star")
        self.canvas.create_image(
            320, 60, image=self.three_star, tags="three_star")

        self.canvas.tag_bind("one_star", "<Button-1>",
                             lambda dummy=0: self.set_difficulty(1))
        self.canvas.tag_bind("two_star", "<Button-1>",
                             lambda dummy=0: self.set_difficulty(4))
        self.canvas.tag_bind(
            "three_star", "<Button-1>", lambda dummy=0: self.set_difficulty(6))
        # ======== AI Start First? ============
        self.know_if_computer_first = IntVar()
        self.ai_to_play_first = Checkbutton(self.canvas, text=' Allow AI to use black', font=("Fira Code", 14), activebackground='#101820',
                                            activeforeground='#f2aa4c', fg='#f2aa4c', bg='#101820', var=self.know_if_computer_first, command=self.know_if_checked)
        self.ai_to_play_first.place(anchor=CENTER, relx=0.5, rely=0.8)

        # Start Button
        Button(text='Start', width=18, font=('fira code medium', 14), bd=0, fg='#101820', bg='#fff',
               command=self.play_with_ai).place(relx=0.5, rely=0.76, anchor="center")

    def know_if_checked(self):
        check = self.know_if_computer_first.get()
        if check:
            self.ai_to_play_first.config(activeforeground='#0f0', fg='#0f0')
        else:
            self.ai_to_play_first.config(
                activeforeground='#f2aa4c', fg='#f2aa4c')

    def set_difficulty(self, difficulty):
        global GAME_DIFFICULTY

        if difficulty == 1:
            self.canvas.delete("two_star_checked")
            self.canvas.delete("three_star_checked")
            self.canvas.create_image(
                80, 60, image=self.one_star_checked, tags="one_star_checked")
        elif difficulty == 4:
            self.canvas.delete("one_star_checked")
            self.canvas.delete("three_star_checked")
            self.canvas.create_image(
                200, 60, image=self.two_star_checked, tags="two_star_checked")
        elif difficulty == 6:
            self.canvas.delete("one_star_checked")
            self.canvas.delete("two_star_checked")
            self.canvas.create_image(
                320, 60, image=self.three_star_checked, tags="three_star_checked")

        GAME_DIFFICULTY = difficulty

    def play_with_ai(self):
        global AI_TO_PLAY_BLACK
        if GAME_DIFFICULTY == 0:
            messagebox.showinfo("No difficulty selected",
                                "Please select a difficulty to play")
        else:
            check = self.know_if_computer_first.get()
            if check:
                AI_TO_PLAY_BLACK = True

            self.master.switch_frame(AIPage)


class AIPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.configure(self, bg="#101820")
        self.root = root
        self.root.title("Othello | AI VS Human")
        self.root.geometry('1000x700+200+20')
        self.root.resizable(0, 0)
        # ============ UI =============
        self.canvas = Canvas(bg='#038f39', width=500, height=500)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.canvas.bind("<Button-1>", self.drop_disc)
        self.game_has_started = True
        self.player_dict = {1: "B", 2: "W"}
        self.current_player = 1
        self.whose_turn = 'human'
        self.AI_is_using = "W"
        self.game_over = False
        self.animation_is_done = True
        self.black_score = 0
        self.white_score = 0
        self.reduction_rate = 0
        self.n = 8
        self.minEvalBoard = -1  # min - 1
        self.maxEvalBoard = self.n * self.n + 4 * self.n + 4 + 1  # max + 1
        # white disc instantialization
        self.white_disc_img = Image.open('./assets/white-disc.png')
        self.white_disc_resize = self.white_disc_img.resize(
            (50, 50), Image.LANCZOS)
        self.white_disc = ImageTk.PhotoImage(self.white_disc_resize)
        # black disc instantialization
        self.black_disc_img = Image.open('./assets/black-disc.png')
        self.black_disc_resize = self.black_disc_img.resize(
            (50, 50), Image.LANCZOS)
        self.black_disc = ImageTk.PhotoImage(self.black_disc_resize)
        # ======== Show game winner and restart button ========
        self.winner_label = Label(
            text=" ", bg="#fff", fg="#101820", font=("Concert One", 32))
        self.restart_button = Button(
            text="Restart", width=15, command=self.restart_game, bg="#fff", fg="#101820", font=("fira code", 16))
        # ======== Back Button ============
        self.back_image = Image.open('./assets/back_icon.png')
        self.back_bg = self.back_image.resize((35, 35), Image.LANCZOS)
        self.back_bg = ImageTk.PhotoImage(self.back_bg)
        Button(image=self.back_bg, bg="#fff",
               command=self.go_back).place(relx=0.1, rely=0.08, anchor=CENTER)
        # ======== Help Button ========
        self.help_image = Image.open('./assets/help_icon.png')
        self.help_bg = self.help_image.resize((35, 35), Image.LANCZOS)
        self.help_bg = ImageTk.PhotoImage(self.help_bg)
        Button(image=self.help_bg, bg="#fff", command=self.show_help).place(
            relx=0.9, rely=0.08, anchor=CENTER)
        # ======== starter functions ========
        self.create_board()
        self.draw_game_board()
        self.draw_score_board()
        self.create_center_discs()
        self.show_available_moves()
        self.check_if_ai_plays_first()

    def check_if_ai_plays_first(self):
        if AI_TO_PLAY_BLACK:
            self.current_player = 2
            self.player_dict = {1: "W", 2: "B"}
            self.whose_turn = 'ai'
            self.AI_is_using = "B"
            self.make_AI_move()

    def make_AI_move(self):
        positions = {
            0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'
        }
        if self.AI_is_using == "W":
            color = "W"
            the_tag = 'white'
        else:
            color = "B"
            the_tag = 'black'

        row, col = self.get_best_AI_move(self.board)
        tag_to_find = positions[row] + str(col+1)
        disc_coordinates = self.canvas.coords(tag_to_find)
        x0, x1, y0, y1 = disc_coordinates
        self.update_game_board(self.board, row, col, color)
        if self.AI_is_using == "B":
            self.canvas.create_image(
                x0+30, x1+30, image=self.black_disc, tag=f'{the_tag}-disc-{tag_to_find}')
        else:
            self.canvas.create_image(
                x0+30, x1+30, image=self.white_disc, tag=f'{the_tag}-disc-{tag_to_find}')
        self.flip_captured_discs(row, col)
        self.update_score_board()
        human_has_a_move = self.check_if_opponent_can_move()
        if human_has_a_move:  # Human has a move
            self.current_player = 3 - self.current_player
            self.whose_turn = "human"
            self.show_available_moves()
        else:  # Human has no move
            available_moves = self.find_legal_moves()  # check if ai has available moves
            if not available_moves:  # ai also has no move
                self.game_over = True
                self.declare_winner()
            else:
                self.whose_turn = "ai"
                self.make_AI_move()

    def EvalBoard(self, board, player):
        n = 8
        tot = 0
        for y in range(n):
            for x in range(n):
                if board[y][x] == player:
                    if (x == 0 or x == n - 1) and (y == 0 or y == n - 1):
                        tot += 4  # corner
                    elif (x == 0 or x == n - 1) or (y == 0 or y == n - 1):
                        tot += 2  # side
                    else:
                        tot += 1
        return tot

    def IsTerminalNode(self):
        return bool(self.find_legal_moves())

    def play_AI_move(self, board, x, y):
        n = 8
        dirx = [-1, 0, 1, -1, 1, -1, 0, 1]
        diry = [-1, -1, -1, 0, 0, 1, 1, 1]
        board[x][y] = self.AI_is_using
        for d in range(8):  # 8 directions
            ctr = 0
            for i in range(n):
                dx = x + dirx[d] * (i + 1)
                dy = y + diry[d] * (i + 1)
                if dx < 0 or dx > n - 1 or dy < 0 or dy > n - 1:
                    ctr = 0
                    break
                elif board[dy][dx] == self.AI_is_using:
                    break
                elif board[dy][dx] == ' ':
                    ctr = 0
                    break
                else:
                    ctr += 1
            for i in range(ctr):
                dx = x + dirx[d] * (i + 1)
                dy = y + diry[d] * (i + 1)
                board[dy][dx] = self.AI_is_using

        return board

    def get_best_AI_move(self, board):
        maxPoints = 0
        mx = -1
        my = -1
        for x in range(8):
            for y in range(8):
                if self.is_legal_move(x, y):
                    points = self.AlphaBeta(
                        board, GAME_DIFFICULTY, self.minEvalBoard, self.maxEvalBoard, True)
                    if points > maxPoints:
                        maxPoints = points
                        mx = x
                        my = y

        return (mx, my)

    def AlphaBeta(self, board, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.IsTerminalNode():
            return self.EvalBoard(board, self.AI_is_using)
        if maximizingPlayer:
            v = self.minEvalBoard
            for y in range(8):
                for x in range(8):
                    if self.is_legal_move(board, x, y):
                        boardTemp = self.play_AI_move(
                            copy.deepcopy(board), x, y)
                        v = max(v, self.AlphaBeta(
                            boardTemp, depth - 1, alpha, beta, False))
                        alpha = max(alpha, v)
                        if beta <= alpha:
                            break  # beta cut-off
            return v
        else:  # minimizingPlayer
            v = self.maxEvalBoard
            for y in range(8):
                for x in range(8):
                    if self.is_legal_move(board, x, y):
                        boardTemp = self.play_AI_move(
                            copy.deepcopy(board), x, y)
                        v = min(v, self.AlphaBeta(
                            boardTemp, depth - 1, alpha, beta, True))
                        beta = min(beta, v)
                        if beta <= alpha:
                            break  # alpha cut-off
            return v

    def restart_game(self):
        self.canvas.delete('all')
        self.game_has_started = True
        self.animation_is_done = True
        self.game_over = False
        self.n = 8
        self.player_dict = {1: "B", 2: "W"}
        self.current_player = 1
        self.whose_turn = 'human'
        self.AI_is_using = "W"
        self.black_score = 0
        self.white_score = 0
        self.reduction_rate = 0
        self.minEvalBoard = -1  # min - 1
        self.maxEvalBoard = self.n * self.n + 4 * self.n + 4 + 1  # max + 1
        self.winner_label.place_forget()
        self.restart_button.place_forget()
        self.create_board()
        self.draw_game_board()
        self.draw_score_board()
        self.create_center_discs()
        self.show_available_moves()
        self.check_if_ai_plays_first()

    def draw_score_board(self):
        self.score_white_disc = Image.open('./assets/white-disc.png')
        self.score_white_disc = self.score_white_disc.resize(
            (70, 70), Image.LANCZOS)
        self.score_white_disc = ImageTk.PhotoImage(self.score_white_disc)

        self.score_black_disc = Image.open('./assets/black-disc.png')
        self.score_black_disc = self.score_black_disc.resize(
            (70, 70), Image.LANCZOS)
        self.score_black_disc = ImageTk.PhotoImage(self.score_black_disc)
        # ======== disc owners ============
        first_player = 'AI' if AI_TO_PLAY_BLACK else "You"
        second_player = 'You' if AI_TO_PLAY_BLACK else "AI"
        self.player1_title = Label(
            text=first_player, font=("Concert One", 28), bg="#101820", fg="#fff")
        self.player1_title.place(relx=0.12, rely=0.37, anchor=CENTER)
        self.player1_title = Label(
            text=second_player, font=("Concert One", 28), bg="#101820", fg="#fff")
        self.player1_title.place(relx=0.88, rely=0.37, anchor=CENTER)
        # ======== disc ============
        self.player1_canvas = Canvas(bg='#101820', width=150, height=170)
        self.player1_canvas.place(relx=0.12, rely=0.54, anchor=CENTER)
        self.player1_canvas.create_image(
            75, 55, image=self.score_black_disc)
        self.player1_score = Label(self.player1_canvas,
                                   text="2", bg='#101820', fg='#cbcbcb', font=('Concert One', 32))
        self.player1_score.place(relx=0.5, rely=0.7, anchor=CENTER)

        self.player2_canvas = Canvas(bg='#101820', width=150, height=170)
        self.player2_canvas.place(relx=0.88, rely=0.54, anchor=CENTER)
        self.player2_canvas.create_image(
            75, 55, image=self.score_white_disc)
        self.player2_score = Label(self.player2_canvas,
                                   text="2", bg='#101820', fg='#cbcbcb', font=('Concert One', 32))
        self.player2_score.place(relx=0.5, rely=0.7, anchor=CENTER)

    def show_available_moves(self):
        all_new_tags = self.canvas.find_withtag("new")
        for i in all_new_tags:
            self.canvas.delete(i)
        available_moves = self.find_legal_moves()
        positions = {
            1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H'
        }

        for single in available_moves:
            letter_number = f"{positions[single[0]+1]}{single[1]+1}"
            the_tag = self.canvas.find_withtag(letter_number)
            the_coords = self.canvas.coords(the_tag[-1])
            x0, x1, y0, y1 = the_coords
            r = 5
            if self.AI_is_using == "B":
                self.canvas.create_oval(
                    x0+30-r, x1+30-r, x0+30+r, x1+30+r, fill="white", outline="", tags=f"new {letter_number}")
            else:
                self.canvas.create_oval(
                    x0+30-r, x1+30-r, x0+30+r, x1+30+r, fill="black", outline="", tags=f"new {letter_number}")

    def create_center_discs(self):
        self.canvas.create_image(
            190+30, 190+30, image=self.white_disc, tag='white-disc-D4')
        self.canvas.create_image(
            250+30, 190+30, image=self.black_disc, tag='black-disc-E4')
        self.canvas.create_image(
            190+30, 250+30, image=self.black_disc, tag='black-disc-D5')
        self.canvas.create_image(
            250+30, 250+30, image=self.white_disc, tag='white-disc-E5')

    def create_board(self):
        self.board = [[" "]*8 for _ in range(8)]
        self.board[3][3] = "W"
        self.board[3][4] = "B"
        self.board[4][3] = "B"
        self.board[4][4] = "W"

    def update_game_board(self, board, row, col, piece):
        board[row][col] = piece

    def update_score_board(self):
        black_score = 0
        white_score = 0
        for r in self.board:
            for j in r:
                if j == "B":
                    black_score += 1
                elif j == "W":
                    white_score += 1

        self.black_score = black_score
        self.white_score = white_score

        self.player1_score.config(text=self.black_score)
        self.player2_score.config(text=self.white_score)

    def flip_captured_discs(self, row, col):
        flipped_pieces = []

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                pieces_to_flip = []

                while 0 <= r < len(self.board) and 0 <= c < len(self.board[0]) and self.board[r][c] == self.player_dict[3 - self.current_player]:
                    pieces_to_flip.append((r, c))
                    r += dr
                    c += dc

                if len(pieces_to_flip) > 0 and 0 <= r < len(self.board) and 0 <= c < len(self.board[0]) and self.board[r][c] == self.player_dict[self.current_player]:
                    flipped_pieces.extend(pieces_to_flip)

        for r, c in flipped_pieces:
            self.board[r][c] = self.player_dict[self.current_player]

        self.flip_captured_images(flipped_pieces)

    def flip_captured_images(self, pieces):
        images_to_change = []
        positions = {
            1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H'
        }

        for r, c in pieces:
            images_to_change.append(f"{positions[r+1]}{c+1}")

        if self.whose_turn == 'ai' and self.AI_is_using == "B":
            color = "W"
        elif self.whose_turn == 'ai' and self.AI_is_using == "W":
            color = "B"
        elif self.whose_turn == 'human' and self.AI_is_using == "B":
            color = "B"
        elif self.whose_turn == 'human' and self.AI_is_using == "W":
            color = "W"

        self.animate_flipped_discs(images_to_change, color)

    def animate_flipped_discs(self, tiles, color):
        """ animate the discs that are currently being flipped """

        for r, c in tiles:
            if color == "W":
                image = self.canvas.find_withtag(f'white-disc-{r}{c}')
                coords = self.canvas.coords(image)
                x, y = coords
                self.canvas.delete(image)
            else:
                image = self.canvas.find_withtag(f'black-disc-{r}{c}')
                coords = self.canvas.coords(image)
                x, y = coords
                self.canvas.delete(image)

            # Shrinking the disc
            if color == "W":
                white_disc_img = Image.open('./assets/white-disc.png')
                new_disc_resize = white_disc_img.resize(
                    (50, 50), Image.LANCZOS)
                new_disc = ImageTk.PhotoImage(new_disc_resize)
                self.canvas.create_image(
                    x, y, image=new_disc, tag='animated')
            else:
                black_disc_img = Image.open('./assets/black-disc.png')
                new_disc_resize = black_disc_img.resize(
                    (50, 50), Image.LANCZOS)
                new_disc = ImageTk.PhotoImage(new_disc_resize)
                self.canvas.create_image(
                    x, y, image=new_disc, tag='animated')

            for i in range(40):
                shrinked_disc = new_disc_resize.resize(
                    (new_disc_resize.width - i, new_disc_resize.height - i))
                self.shrink_render = ImageTk.PhotoImage(shrinked_disc)
                image = self.canvas.find_withtag("animated")
                self.canvas.itemconfig(image, image="")
                self.canvas.itemconfig(
                    image, image=self.shrink_render)

                self.canvas.update()

            self.canvas.delete("animated")

            # Enlarging the disc
            if color == "W":
                black_disc_img = Image.open('./assets/black-disc.png')
                new_disc_resize = black_disc_img.resize(
                    (20, 20), Image.LANCZOS)
                self.new_disc = ImageTk.PhotoImage(new_disc_resize)
                self.canvas.create_image(
                    x, y, image=self.new_disc, tag='animated')
            else:
                white_disc_img = Image.open('./assets/white-disc.png')
                new_disc_resize = white_disc_img.resize(
                    (20, 20), Image.LANCZOS)
                self.new_disc = ImageTk.PhotoImage(new_disc_resize)
                self.canvas.create_image(
                    x, y, image=self.new_disc, tag='animated')

            for i in range(40):
                if color == "W":
                    resized = black_disc_img.resize(
                        (10+i, 10+i), Image.LANCZOS)
                else:
                    resized = white_disc_img.resize(
                        (10+i, 10+i), Image.LANCZOS)
                self.enlarged = ImageTk.PhotoImage(resized)
                image = self.canvas.find_withtag("animated")
                self.canvas.itemconfig(image, image="")
                self.canvas.itemconfig(
                    image, image=self.enlarged)

                self.canvas.update()

            self.canvas.delete("animated")

            # Create the new disc
            if color == "W":
                self.canvas.create_image(
                    x, y, image=self.black_disc, tag=f'black-disc-{r}{c}')
            else:
                self.canvas.create_image(
                    x, y, image=self.white_disc, tag=f'white-disc-{r}{c}')

    def drop_disc(self, event):
        current_tag = self.canvas.gettags('current')
        positions = {
            'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5,  'G': 6, 'H': 7
        }

        if len(current_tag) > 1 and not self.game_over:
            if "new" == current_tag[0]:
                current_tag = current_tag[1]
                move_is_legal = self.is_legal_move(
                    positions[current_tag[0]], int(current_tag[1])-1)
            elif 'white-disc' in current_tag[0] or 'black-disc' in current_tag[0]:
                current_tag = current_tag[0].split('-')[2]
                move_is_legal = self.is_legal_move(
                    positions[current_tag[0]], int(current_tag[1])-1)
            else:
                move_is_legal = self.is_legal_move(
                    positions[current_tag[0][0]], int(current_tag[0][1]) - 1)

            if move_is_legal:
                # if self.game_has_started == True:
                #     self.ai_to_play_first.place_forget()

                if type(current_tag) == tuple:
                    tag_to_find = current_tag[0]
                    current_tag = tag_to_find
                else:
                    tag_to_find = current_tag
                    current_tag = tag_to_find

                if self.AI_is_using == "B":
                    color = "W"
                    the_tag = 'white'
                else:
                    color = "B"
                    the_tag = 'black'

                disc_coordinates = self.canvas.coords(tag_to_find)
                x0, x1, y0, y1 = disc_coordinates

                row, col = positions[current_tag[0]], int(
                    current_tag[1]) - 1
                self.update_game_board(self.board, row, col, color)
                if self.AI_is_using == "W":
                    self.canvas.create_image(
                        x0+30, x1+30, image=self.black_disc, tag=f'{the_tag}-disc-{current_tag}')
                else:
                    self.canvas.create_image(
                        x0+30, x1+30, image=self.white_disc, tag=f'{the_tag}-disc-{current_tag}')
                self.flip_captured_discs(row, col)
                self.update_score_board()
                ai_has_a_move = self.check_if_opponent_can_move()
                if ai_has_a_move:  # AI has a move
                    self.current_player = 3 - self.current_player
                    self.whose_turn = "ai"
                    self.make_AI_move()
                else:  # AI has no move
                    available_moves = self.find_legal_moves()  # check if human has available moves
                    if not available_moves:  # human also has no move
                        self.game_over = True
                        self.declare_winner()
                    else:
                        self.whose_turn = "human"
                        self.show_available_moves()

    def check_if_opponent_can_move(self):
        self.current_player = 3 - self.current_player
        moves = self.find_legal_moves()
        self.current_player = 3 - self.current_player
        return moves

    def declare_winner(self):
        self.winner_label.place(relx=0.5, rely=0.08, anchor=CENTER)
        self.restart_button.place(relx=0.5, rely=0.93, anchor=CENTER)

        if self.AI_is_using == "B":
            if self.black_score > self.white_score:
                self.winner_label.configure(
                    text=" " * 5 + "AI wins!" + " " * 5)
            elif self.black_score == self.white_score:
                self.winner_label.configure(
                    text=" " * 5 + "It is a tie!" + " " * 5)
            else:
                self.winner_label.configure(
                    text=" " * 2 + "Congratulations! You win." + " " * 2)
        elif self.AI_is_using == "W":
            if self.white_score > self.black_score:
                self.winner_label.configure(
                    text=" " * 5 + "AI wins!" + " " * 5)
            elif self.black_score == self.white_score:
                self.winner_label.configure(
                    text=" " * 5 + "It is a tie!" + " " * 5)
            else:
                self.winner_label.configure(
                    text=" " * 2 + "Congratulations! You win." + " " * 2)

    def is_legal_move(self, row, col):
        # if there is a piece there already
        if self.board[row][col] != " ":
            return False

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (-1, -1), (1, -1), (-1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.player_dict[3-self.current_player]:
                while 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r][c] == " ":
                        break
                    if self.board[r][c] == self.player_dict[self.current_player]:
                        return True
                    r, c = r + dr, c + dc

        return False

    def find_legal_moves(self):
        legal_moves = []
        for r in range(8):
            for c in range(8):
                if self.is_legal_move(r, c):
                    legal_moves.append((r, c))

        return legal_moves

    def draw_game_board(self):
        distance = 60
        for i, value in enumerate("ABCDEFGH"):
            chip_number = 1
            x0 = 10 + (i * distance)
            x1 = x0 + 60
            for j in range(8):
                y0 = 10 + j * distance
                y1 = y0 + 60
                self.canvas.create_rectangle(
                    x0, y0, x1, y1, fill='#038f39', outline='black',
                    width=3, tags=f'{value}{chip_number}')
                chip_number += 1

    def go_back(self):
        global GAME_DIFFICULTY, AI_TO_PLAY_BLACK
        GAME_DIFFICULTY = 0
        AI_TO_PLAY_BLACK = False
        self.master.switch_frame(StartPage)

    def show_help(self):
        self.game_help_veil = Frame(width=1000, height=700, bg='#101820')
        self.game_help_veil.place(x=0, y=0)
        self.about_bg = Image.open('./assets/back_icon.png')
        self.about_bg = self.about_bg.resize((30, 30), Image.LANCZOS)
        self.about_bg = ImageTk.PhotoImage(self.about_bg)
        Button(self.game_help_veil, image=self.about_bg, bg="#fff",
               command=self.hide_game_help).place(relx=0.05, rely=0.06, anchor=CENTER)

        a = f"The object of the game is to have the majority of your\n discs' color facing up on the board at the end of the game"
        b = "\n\n How to move:\n A move consist of \"outflanking\" your opponent's disc(s), then\n flipping the outflanked disc(s) to your color"
        c = "\nTo outflank means to place your disc on the board in a way\n that the opposing color is bordered at each end by a disc of your color"
        d = "\n\n Rules: \n==> Black always moves first\n==> If you cannot outflank any disc on your turn, \nyou forfeit your turn and your opponent moves"
        e = "\n==> You cannot skip over your own color to outflank an opposing disc"
        f = "\n==> If both players cannot move, the game is over"
        g = "\n\n Enjoy!"
        about_text = a + b + c + d + e + f + g
        Label(self.game_help_veil, text=about_text, font=("fira code", 16), fg='#fff', bg='#101820').place(
            relx=0.5, rely=0.5, anchor="center")

    def hide_game_help(self):
        self.game_help_veil.place_forget()


class HumanPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.configure(self, bg="#101820")
        self.root = root
        self.root.title("Othello | Human Page")
        self.root.geometry('1000x700+200+20')
        self.root.resizable(0, 0)
        # ============ UI =============
        self.canvas = Canvas(bg='#038f39', width=500, height=500)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.canvas.bind("<Button-1>", self.drop_disc)
        self.player_turn = "B"
        self.current_player = 1
        self.player_dict = {1: "B", 2: "W"}
        self.game_over = False
        self.animation_is_done = True
        self.black_score = 0
        self.white_score = 0
        self.reduction_rate = 0
        # white disc instantialization
        self.white_disc_img = Image.open('./assets/white-disc.png')
        self.white_disc_resize = self.white_disc_img.resize(
            (50, 50), Image.LANCZOS)
        self.white_disc = ImageTk.PhotoImage(self.white_disc_resize)
        # black disc instantialization
        self.black_disc_img = Image.open('./assets/black-disc.png')
        self.black_disc_resize = self.black_disc_img.resize(
            (50, 50), Image.LANCZOS)
        self.black_disc = ImageTk.PhotoImage(self.black_disc_resize)
        # utility buttons
        self.turn_label = Label(
            text=" " * 8 + "Black to play" + " " * 8, bg="#fff", fg="#101820", font=("Concert One", 28))
        self.turn_label.place(relx=0.5, rely=0.08, anchor=CENTER)
        self.winner_label = Label(
            text=" ", bg="#fff", fg="#101820", font=("Concert One", 32))
        self.restart_button = Button(
            text="Restart", width=15, command=self.restart_game, bg="#fff", fg="#101820", font=("fira code", 16))
        # ======== Back Button ============
        self.back_image = Image.open('./assets/back_icon.png')
        self.back_bg = self.back_image.resize((35, 35), Image.LANCZOS)
        self.back_bg = ImageTk.PhotoImage(self.back_bg)
        Button(image=self.back_bg, bg="#fff",
               command=self.go_back).place(relx=0.1, rely=0.08, anchor=CENTER)
        # ======== Help Button ============
        self.help_image = Image.open('./assets/help_icon.png')
        self.help_bg = self.help_image.resize((35, 35), Image.LANCZOS)
        self.help_bg = ImageTk.PhotoImage(self.help_bg)
        Button(image=self.help_bg, bg="#fff", command=self.show_help).place(
            relx=0.9, rely=0.08, anchor=CENTER)
        # ======== starter functions ========
        self.create_board()
        self.draw_game_board()
        self.draw_score_board()
        self.create_center_discs()
        self.show_available_moves()

    def restart_game(self):
        self.canvas.delete('all')
        self.player_turn = "B"
        self.current_player = 1
        self.game_over = False
        self.animation_is_done = True
        self.black_score = 0
        self.white_score = 0
        self.winner_label.place_forget()
        self.restart_button.place_forget()
        self.turn_label.config(text=" " * 8 + "Black to play" + " " * 8)
        self.turn_label.place(relx=0.5, rely=0.08, anchor=CENTER)
        self.create_board()
        self.draw_game_board()
        self.draw_score_board()
        self.create_center_discs()
        self.show_available_moves()

    def draw_score_board(self):
        self.score_white_disc = Image.open('./assets/white-disc.png')
        self.score_white_disc = self.score_white_disc.resize(
            (70, 70), Image.LANCZOS)
        self.score_white_disc = ImageTk.PhotoImage(self.score_white_disc)

        self.score_black_disc = Image.open('./assets/black-disc.png')
        self.score_black_disc = self.score_black_disc.resize(
            (70, 70), Image.LANCZOS)
        self.score_black_disc = ImageTk.PhotoImage(self.score_black_disc)

        # ======== disc and Time ============
        self.player1_canvas = Canvas(bg='#101820', width=150, height=170)
        self.player1_canvas.place(relx=0.12, rely=0.5, anchor=CENTER)
        self.player1_canvas.create_image(
            75, 55, image=self.score_black_disc)
        self.player1_score = Label(self.player1_canvas,
                                   text="2", bg='#101820', fg='#cbcbcb', font=('Concert One', 32))
        self.player1_score.place(relx=0.5, rely=0.7, anchor=CENTER)

        self.player2_canvas = Canvas(bg='#101820', width=150, height=170)
        self.player2_canvas.place(relx=0.88, rely=0.5, anchor=CENTER)
        self.player2_canvas.create_image(
            75, 55, image=self.score_white_disc)
        self.player2_score = Label(self.player2_canvas,
                                   text="2", bg='#101820', fg='#cbcbcb', font=('Concert One', 32))
        self.player2_score.place(relx=0.5, rely=0.7, anchor=CENTER)

    def show_available_moves(self):
        all_new_tags = self.canvas.find_withtag("new")
        for i in all_new_tags:
            self.canvas.delete(i)
        available_moves = self.find_legal_moves()
        positions = {
            1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H'
        }

        for single in available_moves:
            letter_number = f"{positions[single[0]+1]}{single[1]+1}"
            the_tag = self.canvas.find_withtag(letter_number)
            the_coords = self.canvas.coords(the_tag[-1])
            x0, x1, y0, y1 = the_coords
            r = 5
            if self.player_turn == "W":
                self.canvas.create_oval(
                    x0+30-r, x1+30-r, x0+30+r, x1+30+r, fill="white", outline="", tags=f"new {letter_number}")
            else:
                self.canvas.create_oval(
                    x0+30-r, x1+30-r, x0+30+r, x1+30+r, fill="black", outline="", tags=f"new {letter_number}")

    def create_center_discs(self):
        self.canvas.create_image(
            190+30, 190+30, image=self.white_disc, tag='white-disc-D4')
        self.canvas.create_image(
            250+30, 190+30, image=self.black_disc, tag='black-disc-E4')
        self.canvas.create_image(
            190+30, 250+30, image=self.black_disc, tag='black-disc-D5')
        self.canvas.create_image(
            250+30, 250+30, image=self.white_disc, tag='white-disc-E5')

    def is_legal_move(self, row, col):
        # if there is a piece there already
        if self.board[row][col] != " ":
            return False

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (-1, -1), (1, -1), (-1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.player_dict[3-self.current_player]:
                while 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r][c] == " ":
                        break
                    if self.board[r][c] == self.player_dict[self.current_player]:
                        return True
                    r, c = r + dr, c + dc

        return False

    def create_board(self):
        self.board = [[" "]*8 for i in range(8)]
        self.board[3][3] = "W"
        self.board[3][4] = "B"
        self.board[4][3] = "B"
        self.board[4][4] = "W"

    def update_game_board(self, board, row, col, piece):
        board[row][col] = piece

    def update_score_board(self):
        black_score = 0
        white_score = 0
        for r in self.board:
            for j in r:
                if j == "B":
                    black_score += 1
                elif j == "W":
                    white_score += 1

        self.black_score = black_score
        self.white_score = white_score

        self.player1_score.config(text=self.black_score)
        self.player2_score.config(text=self.white_score)

    def update_turn_indicator(self):
        if self.player_turn == "B":
            self.turn_label.config(text=" " * 8 + "Black to play" + " " * 8)
        else:
            self.turn_label.config(text=" " * 8 + "White to play" + " " * 8)

    def flip_captured_discs(self, row, col):
        flipped_pieces = []

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                pieces_to_flip = []

                while 0 <= r < len(self.board) and 0 <= c < len(self.board[0]) and self.board[r][c] == self.player_dict[3 - self.current_player]:
                    pieces_to_flip.append((r, c))
                    r += dr
                    c += dc

                if len(pieces_to_flip) > 0 and 0 <= r < len(self.board) and 0 <= c < len(self.board[0]) and self.board[r][c] == self.player_dict[self.current_player]:
                    flipped_pieces.extend(pieces_to_flip)

        for r, c in flipped_pieces:
            self.board[r][c] = self.player_dict[self.current_player]

        self.flip_captured_images(
            flipped_pieces, self.player_dict[3-self.current_player])

    def flip_captured_images(self, pieces, color):
        images_to_change = []
        positions = {
            1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H'
        }

        for r, c in pieces:
            images_to_change.append(f"{positions[r+1]}{c+1}")

        self.animate_flipped_discs(images_to_change, color)

    def animate_flipped_discs(self, tiles, color):
        """ animate the discs that are currently being flipped """

        for r, c in tiles:
            if color == "W":
                image = self.canvas.find_withtag(f'white-disc-{r}{c}')
                coords = self.canvas.coords(image)
                x, y = coords
                self.canvas.delete(image)
            else:
                image = self.canvas.find_withtag(f'black-disc-{r}{c}')
                coords = self.canvas.coords(image)
                x, y = coords
                self.canvas.delete(image)

            # Shrinking the disc
            if color == "W":
                white_disc_img = Image.open('./assets/white-disc.png')
                new_disc_resize = white_disc_img.resize(
                    (50, 50), Image.LANCZOS)
                new_disc = ImageTk.PhotoImage(new_disc_resize)
                self.canvas.create_image(
                    x, y, image=new_disc, tag='animated')
            else:
                black_disc_img = Image.open('./assets/black-disc.png')
                new_disc_resize = black_disc_img.resize(
                    (50, 50), Image.LANCZOS)
                new_disc = ImageTk.PhotoImage(new_disc_resize)
                self.canvas.create_image(
                    x, y, image=new_disc, tag='animated')

            for i in range(40):
                shrinked_disc = new_disc_resize.resize(
                    (new_disc_resize.width - i, new_disc_resize.height - i))
                self.shrink_render = ImageTk.PhotoImage(shrinked_disc)
                image = self.canvas.find_withtag("animated")
                self.canvas.itemconfig(image, image="")
                self.canvas.itemconfig(
                    image, image=self.shrink_render)

                self.canvas.update()

            self.canvas.delete("animated")

            # Enlarging the disc
            if color == "W":
                black_disc_img = Image.open('./assets/black-disc.png')
                new_disc_resize = black_disc_img.resize(
                    (20, 20), Image.LANCZOS)
                self.new_disc = ImageTk.PhotoImage(new_disc_resize)
                self.canvas.create_image(
                    x, y, image=self.new_disc, tag='animated')
            else:
                white_disc_img = Image.open('./assets/white-disc.png')
                new_disc_resize = white_disc_img.resize(
                    (20, 20), Image.LANCZOS)
                self.new_disc = ImageTk.PhotoImage(new_disc_resize)
                self.canvas.create_image(
                    x, y, image=self.new_disc, tag='animated')

            for i in range(40):
                if color == "W":
                    resized = black_disc_img.resize(
                        (10+i, 10+i), Image.LANCZOS)
                else:
                    resized = white_disc_img.resize(
                        (10+i, 10+i), Image.LANCZOS)
                self.enlarged = ImageTk.PhotoImage(resized)
                image = self.canvas.find_withtag("animated")
                self.canvas.itemconfig(image, image="")
                self.canvas.itemconfig(
                    image, image=self.enlarged)

                self.canvas.update()

            self.canvas.delete("animated")

            # Create the new disc
            if color == "W":
                self.canvas.create_image(
                    x, y, image=self.black_disc, tag=f'black-disc-{r}{c}')
            else:
                self.canvas.create_image(
                    x, y, image=self.white_disc, tag=f'white-disc-{r}{c}')

    def drop_disc(self, event):
        current_tag = self.canvas.gettags('current')
        positions = {
            'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5,  'G': 6, 'H': 7
        }

        if len(current_tag) > 1 and not self.game_over:
            if "new" == current_tag[0]:
                current_tag = current_tag[1]
                move_is_legal = self.is_legal_move(
                    positions[current_tag[0]], int(current_tag[1])-1)
            elif 'white-disc' in current_tag[0] or 'black-disc' in current_tag[0]:
                current_tag = current_tag[0].split('-')[2]
                move_is_legal = self.is_legal_move(
                    positions[current_tag[0]], int(current_tag[1])-1)
            else:
                move_is_legal = self.is_legal_move(
                    positions[current_tag[0][0]], int(current_tag[0][1]) - 1)

            if move_is_legal:
                if type(current_tag) == tuple:
                    tag_to_find = current_tag[0]
                    current_tag = tag_to_find
                else:
                    tag_to_find = current_tag
                    current_tag = tag_to_find

                disc_coordinates = self.canvas.coords(tag_to_find)
                x0, x1, y0, y1 = disc_coordinates
                if self.player_turn == "W" and self.animation_is_done:
                    row, col = positions[current_tag[0]], int(
                        current_tag[1]) - 1
                    self.update_game_board(self.board, row, col, "W")
                    self.canvas.create_image(
                        x0+30, x1+30, image=self.white_disc, tag=f'white-disc-{current_tag}')
                    self.flip_captured_discs(row, col)
                    self.update_score_board()
                    next_player_can_play = self.check_if_opponent_can_move()
                    if next_player_can_play:  # black has a move
                        self.player_turn = "B"
                        self.update_turn_indicator()
                        self.show_available_moves()
                    else:  # black has no move
                        self.current_player = 3 - self.current_player  # switch current player to white
                        available_moves = self.find_legal_moves()  # check white's available moves
                        if not available_moves:  # white also has no move
                            self.game_over = True
                            self.declare_winner()
                        else:
                            self.show_available_moves()
                elif self.player_turn == "B" and self.animation_is_done:
                    row, col = positions[current_tag[0]], int(
                        current_tag[1]) - 1
                    self.update_game_board(self.board, row, col, "B")
                    self.canvas.create_image(
                        x0+30, x1+30, image=self.black_disc, tag=f'black-disc-{current_tag}')
                    self.flip_captured_discs(row, col)
                    self.update_score_board()
                    next_player_can_play = self.check_if_opponent_can_move()
                    if next_player_can_play:  # white has a move
                        self.player_turn = "W"
                        self.update_turn_indicator()
                        self.show_available_moves()
                    else:  # white has no move
                        self.current_player = 3 - self.current_player  # switch current player to black
                        available_moves = self.find_legal_moves()  # check black's available moves
                        if not available_moves:  # black also has no move
                            self.game_over = True
                            self.declare_winner()
                        else:
                            self.show_available_moves()

    def check_if_opponent_can_move(self):
        self.current_player = 3 - self.current_player
        moves = self.find_legal_moves()
        return moves

    def declare_winner(self):
        self.turn_label.place_forget()
        self.winner_label.place(relx=0.5, rely=0.08, anchor=CENTER)
        self.restart_button.place(relx=0.5, rely=0.93, anchor=CENTER)
        if self.black_score > self.white_score:
            self.winner_label.configure(
                text=" " * 8 + "Black wins!" + " " * 8)
        elif self.black_score < self.white_score:
            self.winner_label.configure(
                text=" " * 8 + "White wins!" + " " * 8)
        else:
            self.winner_label.configure(
                text=" " * 8 + "It is a tie!" + " " * 8)

    def find_legal_moves(self):
        legal_moves = []
        for r in range(8):
            for c in range(8):
                if self.is_legal_move(r, c):
                    legal_moves.append((r, c))

        return legal_moves

    def draw_game_board(self):
        distance = 60
        for i, value in enumerate("ABCDEFGH"):
            chip_number = 1
            x0 = 10 + (i * distance)
            x1 = x0 + 60
            for j in range(8):
                y0 = 10 + j * distance
                y1 = y0 + 60
                self.canvas.create_rectangle(
                    x0, y0, x1, y1, fill='#038f39', outline='black',
                    width=3, tags=f'{value}{chip_number}')
                chip_number += 1

    def go_back(self):
        self.master.switch_frame(StartPage)

    def show_help(self):
        self.game_help_veil = Frame(width=1000, height=700, bg='#101820')
        self.game_help_veil.place(x=0, y=0)
        self.about_bg = Image.open('./assets/back_icon.png')
        self.about_bg = self.about_bg.resize((30, 30), Image.LANCZOS)
        self.about_bg = ImageTk.PhotoImage(self.about_bg)
        Button(self.game_help_veil, image=self.about_bg, bg="#fff",
               command=self.hide_game_help).place(relx=0.05, rely=0.06, anchor=CENTER)

        a = f"The object of the game is to have the majority of your\n discs' color facing up on the board at the end of the game"
        b = "\n\n How to move:\n A move consist of \"outflanking\" your opponent's disc(s), then\n flipping the outflanked disc(s) to your color"
        c = "\nTo outflank means to place your disc on the board in a way\n that the opposing color is bordered at each end by a disc of your color"
        d = "\n\n Rules: \n==> Black always moves first\n==> If you cannot outflank any disc on your turn, \nyou forfeit your turn and your opponent moves"
        e = "\n==> You cannot skip over your own color to outflank an opposing disc"
        f = "\n==> If both players cannot move, the game is over"
        g = "\n\n Enjoy!"
        about_text = a + b + c + d + e + f + g
        Label(self.game_help_veil, text=about_text, font=("fira code", 16), fg='#fff', bg='#101820').place(
            relx=0.5, rely=0.5, anchor="center")

    def hide_game_help(self):
        self.game_help_veil.place_forget()


if __name__ == '__main__':
    app = Switch()
    app.mainloop()
