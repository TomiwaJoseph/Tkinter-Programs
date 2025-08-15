from tkinter import Label, Frame, Canvas, Button, Menu, StringVar
from game_logic import Logic
import time
from game_card import Card
from PIL import ImageTk, Image
from random import randrange


# ====== Backdrop Themes ===========
backgdrop_color_schemes = {
    'Default': '#006633',
    'Soft Brown': '#A67B5B',
    'Desert Blue': '#336699',
    'Walnut': '#663300',
    'Brown': '#996633',
}
# ====== Card Back Themes ===========
card_schemes = {
    'Default': 'spider',
    'Flower': 'flower',
    'Star': 'star',
    'Geometric': 'geometric',
}


class MainPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.master = root
        self.master.geometry("750x680+308+20")
        self.master.resizable(0, 0)
        # ============== Variables ==================
        self.backdrop_choice = StringVar()
        self.card_theme_choice = StringVar()
        # ============== Starter Functions ==================
        self.create_menubar()
        self.create_backdrop()
        Logic.reset_all_variables()
        self.load_card_theme()
        self.init_suit_images()
        self.generate_random_stacks()
        self.create_stock_pile()
        self.create_tableau()
        self.show_playable_cards()
        self.game_start_time = time.time()
        self.about_app_veil = Frame(width=750, height=680)
        self.about_developer_veil = Frame(width=750, height=680)

    def show_playable_cards(self):
        for value in Logic.TABLEAU_CARDS.values():
            topmost_card = value[-1]
            topmost_card.status = "visible"
            card_id, card_value = topmost_card.id, topmost_card.value
            card_type = f"{Logic.suit_dict.get(card_value, card_value)}_of_{Logic.SUIT_TYPE}"
            image = self.card_suit_images[card_type]
            self.game_canvas.itemconfig(card_id, image=image)

    def create_tableau(self):
        table_numbers = [("stack_1", 6), ("stack_2", 6), ("stack_3", 6), ("stack_4", 6), ("stack_5", 5),
                         ("stack_6", 5), ("stack_7", 5), ("stack_8", 5), ("stack_9", 5), ("stack_10", 5)]
        x = 60
        y = 180

        for idx, val in enumerate(table_numbers):
            stack, i = val
            suit_values = Logic.TABLEAU_LISTS[stack]
            values = []
            cards = []
            stack_number = stack.split("_")[1]
            for j in range(i):
                new_card = self.game_canvas.create_image(
                    x, y, image=self.card_theme_image, tags=f"stack_{stack_number}")
                self.game_canvas.addtag_withtag(
                    f"card-{new_card}", new_card)
                self.game_canvas.addtag_withtag(f"{x}-{y}", new_card)
                suit_value = suit_values[j]
                values.append(suit_value)
                the_card = Card(new_card, "tableau-card", suit_value)
                cards.append(the_card)

                # Bind events to each rectangle tag
                self.game_canvas.tag_bind(
                    new_card, "<Button-1>", lambda event, instance=self: Logic.handle_tableau_card_click(instance, event))
                self.game_canvas.tag_bind(
                    new_card, "<B1-Motion>", lambda event, instance=self: Logic.handle_tableau_drag_card(instance, event))
                self.game_canvas.tag_bind(
                    new_card, "<ButtonRelease-1>", lambda event, instance=self: Logic.handle_tableau_drop_card(instance, event))

                y += 10

            x += 70
            y = 180
            Logic.TABLEAU_CARDS[stack] = cards

    def generate_random_stacks(self):
        all_numbers = [j for i in range(8) for j in range(1, 14)]

        covered_1 = self.select_random_elements(all_numbers, 10)
        covered_2 = self.select_random_elements(covered_1[1], 10)
        covered_3 = self.select_random_elements(covered_2[1], 10)
        covered_4 = self.select_random_elements(covered_3[1], 10)
        covered_5 = self.select_random_elements(covered_4[1], 10)

        stack_1 = self.select_random_elements(covered_5[1], 6)
        stack_2 = self.select_random_elements(stack_1[1], 6)
        stack_3 = self.select_random_elements(stack_2[1], 6)
        stack_4 = self.select_random_elements(stack_3[1], 6)
        stack_5 = self.select_random_elements(stack_4[1], 5)
        stack_6 = self.select_random_elements(stack_5[1], 5)
        stack_7 = self.select_random_elements(stack_6[1], 5)
        stack_8 = self.select_random_elements(stack_7[1], 5)
        stack_9 = self.select_random_elements(stack_8[1], 5)
        stack_10 = stack_9[1]

        # save suits to the tableau
        Logic.TABLEAU_LISTS = {"stack_1": stack_1[0], "stack_2": stack_2[0], "stack_3": stack_3[0], "stack_4": stack_4[0], "stack_5": stack_5[0],
                               "stack_6": stack_6[0], "stack_7": stack_7[0], "stack_8": stack_8[0], "stack_9": stack_9[0], "stack_10": stack_10}

        # save suits to the stock pile
        Logic.STOCK_PILE_LISTS = [covered_1[0], covered_2[0],
                                  covered_3[0], covered_4[0], covered_5[0]]

        # print(Logic.TABLEAU_LISTS)

    def load_card_theme(self):
        current_card_theme = card_schemes[Logic.CURRENT_CARD_THEME]
        image = Image.open(
            f"./static/card_themes/{current_card_theme}.png")
        width, height = image.size
        image = image.resize((width//2, height//2))
        self.card_theme_image = ImageTk.PhotoImage(image)

    def init_suit_images(self):
        # Load all suites
        self.card_suit_images = {}
        card_values = ["ace", "2", "3", "4", "5", "6",
                       "7", "8", "9", "10", "king", "queen", "jack"]

        suit = Logic.SUIT_TYPE
        for value in card_values:
            name = f"{value}_of_{suit}"
            image = Image.open(
                f"./static/cards/{suit}/{name}.png")
            width, height = image.size
            image = image.resize((width//6, height//6))
            self.card_suit_images[name] = ImageTk.PhotoImage(image)

    def create_stock_pile(self):
        placement = 690
        for i in range(5):
            stock_pile = self.game_canvas.create_image(
                placement, 70, image=self.card_theme_image)
            self.game_canvas.addtag_withtag(
                f"stockpile-{str(stock_pile)}", stock_pile)
            the_card = Card(stock_pile, "stock-pile",
                            Logic.STOCK_PILE_LISTS[i])
            Logic.STOCK_PILE_CARDS.append(the_card)
            self.game_canvas.tag_bind(
                stock_pile, "<Button-1>", lambda x: Logic.handle_stock_pile_click(self))
            placement -= 15

    def create_menubar(self):
        menubar = Menu()
        # ===================================
        game_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Game', menu=game_menu)
        game_menu.add_command(
            label='New Game', command=lambda: self.master.switch_frame(MainPage))
        # Add line between New Game and Exit
        game_menu.add_separator()
        game_menu.add_command(label='Exit', command=self.master.destroy)
        self.master.config(menu=menubar)
        # ===================================
        options_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Options', menu=options_menu)
        backdrop_themes_menu = Menu(options_menu, tearoff=0)
        options_menu.add_cascade(label='Backdrops', menu=backdrop_themes_menu)

        self.backdrop_choice.set('Default')
        for keys in backgdrop_color_schemes:
            backdrop_themes_menu.add_radiobutton(
                label=keys, variable=self.backdrop_choice, command=self.change_backdrop)
            backdrop_themes_menu.add_separator()
        options_menu.add_separator()

        card_theme_menu = Menu(options_menu, tearoff=0)
        options_menu.add_cascade(label='Card Back', menu=card_theme_menu)
        self.card_theme_choice.set('Default')
        for keys in card_schemes:
            card_theme_menu.add_radiobutton(
                label=keys, variable=self.card_theme_choice, command=self.change_card_theme)
            card_theme_menu.add_separator()
        # ===================================
        info_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Help', menu=info_menu)
        info_menu.add_command(label="About app", command=self.show_about_app)
        info_menu.add_command(label="About Developer",
                              command=self.show_about_developer)

    def create_backdrop(self):
        backdrop_color = backgdrop_color_schemes[Logic.CURRENT_BACKDROP_THEME]
        self.game_canvas = Canvas(width=750, height=680, bg=backdrop_color)
        self.game_canvas.place(relx=0.5, rely=0.5, anchor="center")

    def change_backdrop(self):
        new_backdrop = self.backdrop_choice.get()
        Logic.CURRENT_BACKDROP_THEME = new_backdrop
        backdrop_color = backgdrop_color_schemes[new_backdrop]
        self.game_canvas.config(bg=backdrop_color)
        self.about_developer_veil.configure(bg=backdrop_color)
        self.about_app_veil.configure(bg=backdrop_color)

    def change_card_theme(self):
        new_card_theme = self.card_theme_choice.get()
        Logic.CURRENT_CARD_THEME = new_card_theme
        card_theme = card_schemes[new_card_theme]
        image = Image.open(
            f"./static/card_themes/{card_theme}.png")
        width, height = image.size
        image = image.resize((width//2, height//2))
        self.card_theme_image = ImageTk.PhotoImage(image)

        for card in Logic.STOCK_PILE_CARDS:
            card_id = card.id
            self.game_canvas.itemconfigure(
                card_id, image=self.card_theme_image)

        for stack in Logic.TABLEAU_CARDS.values():
            for card in stack:
                if card.status == "hidden":
                    self.game_canvas.itemconfig(
                        card.id, image=self.card_theme_image)

    def reveal_game_outcome(self, outcome):
        game_end_time = time.time()
        backdrop = backgdrop_color_schemes[Logic.CURRENT_BACKDROP_THEME]
        game_result_veil = Frame(bg=backdrop, width=750, height=680)
        game_result_veil.place(x=0, y=0)
        game_time = self.formatted_game_time(
            self.game_start_time, game_end_time)
        results_frame = Frame(bg="white", width=580,
                              height=250, bd=3, relief="ridge")
        results_frame.place(relx=0.5, rely=0.5, anchor="center")
        Label(results_frame, text="Congrats. You completed the game!", bg="#fff", fg="#181818", font=(
            "Mosk Medium 500", 18)).place(relx=0.06, rely=0.18, anchor="w")
        Label(results_frame, text=f"Moves count: {outcome["moves_count"]}", bg="#fff", fg="#181818", font=(
            "Mosk Medium 500", 18)).place(relx=0.06, rely=0.36, anchor="w")
        Label(results_frame, text=f"Time used: {game_time}", bg="#fff", fg="#181818", font=(
            "Mosk Medium 500", 18)).place(relx=0.06, rely=0.54, anchor="w")
        Button(results_frame, text='Play again', width=16, font=('fira code medium', 13),
               bd=0, bg='#0A1310', fg='#fff', command=self.start_new_game).place(relx=0.06, rely=0.78, anchor="w")
        Button(results_frame, text='Exit game', width=16, font=('fira code medium', 13),
               bd=0, bg='#0A1310', fg='#fff', command=lambda: self.master.destroy()).place(relx=0.4, rely=0.78, anchor="w")

    def show_about_app(self):
        self.hide_about_app_veil()
        self.hide_about_developer_veil()
        backdrop_color = backgdrop_color_schemes.get(
            Logic.CURRENT_BACKDROP_THEME)
        self.about_app_veil = Frame(width=750, height=680, bg=backdrop_color)
        self.about_app_veil.place(x=0, y=0)
        help_canvas = Canvas(self.about_app_veil, width=670,  height=500,
                             border=3, relief="ridge", borderwidth=3)
        help_canvas.place(relx=0.5, rely=0.46, anchor='center')

        a = "A single suit solitaire application"
        b = "Features includes:"
        c = "◾ One single suit (heart, spade, club or diamond)"
        d = "◾ Tap-to-move and drag-and-drop functionality"
        e = "◾ Moves card to foundation when possible"
        f = "◾ Multiple color schemes and card back designs... and others."

        g = "Future improvements & updates:"
        h = "◾ Undo function"
        i = "◾ Hints"
        j = "◾ Allow multiple suits"
        k = "◾ Calming ambient background music"

        help_canvas.create_text(
            60, 45, anchor="w", fill="#0A1310", text=a, font=("Mosk Normal 400", 16))
        help_canvas.create_text(
            60, 90, anchor="w", fill="#0A1310", text=b, font=("Mosk Bold 700", 16))
        help_canvas.create_text(
            60, 130, anchor="w", fill="#0A1310", text=c, font=("Mosk Normal 400", 16))
        help_canvas.create_text(
            60, 170, anchor="w", fill="#0A1310", text=d, font=("Mosk Normal 400", 16))
        help_canvas.create_text(
            60, 210, anchor="w", fill="#0A1310", text=e, font=("Mosk Normal 400", 16))
        help_canvas.create_text(
            60, 250, anchor="w", fill="#0A1310", text=f, font=("Mosk Normal 400", 16))

        help_canvas.create_text(
            60, 295, anchor="w", fill="#0A1310", text=g, font=("Mosk Bold 700", 16))
        help_canvas.create_text(
            60, 340, anchor="w", fill="#0A1310", text=h, font=("Mosk Normal 400", 16))
        help_canvas.create_text(
            60, 380, anchor="w", fill="#0A1310", text=i, font=("Mosk Normal 400", 16))
        help_canvas.create_text(
            60, 420, anchor="w", fill="#0A1310", text=j, font=("Mosk Normal 400", 16))
        help_canvas.create_text(
            60, 460, anchor="w", fill="#0A1310", text=k, font=("Mosk Normal 400", 16))

        Button(self.about_app_veil, text="Close", bd=0, fg='#fff', bg='#101820', font=(
            "fira code medium", 13), width=16, command=self.hide_about_app_veil).place(relx=0.5, rely=0.9, anchor="center")

    def show_about_developer(self):
        self.hide_about_app_veil()
        self.hide_about_developer_veil()
        backdrop_color = backgdrop_color_schemes.get(
            Logic.CURRENT_BACKDROP_THEME)
        self.about_developer_veil = Frame(
            width=750, height=680, bg=backdrop_color)
        self.about_developer_veil.place(x=0, y=0)

        help_canvas = Canvas(self.about_developer_veil, width=670, height=390,
                             border=3, relief="ridge", borderwidth=3)
        help_canvas.place(relx=0.5, rely=0.45, anchor='center')
        help_canvas.create_text(60, 50, font=("Mosk Normal 400", 18), fill="#0A1310",
                                anchor='w', text="I am Tomiwa Joseph, an experienced software developer.")
        help_canvas.create_text(60, 100, font=(
            "Mosk Bold 700", 18), fill="#0A1310", anchor="w", text="Here is my portfolio:")
        help_canvas.create_text(60, 150, font=(
            "Mosk Normal 400", 18), fill="#0A1310", anchor="w", text="https://tomiwajoseph.vercel.app")
        help_canvas.create_text(60, 200, font=(
            "Mosk Bold 700", 18), fill="#0A1310", anchor="w", text="My socials:")
        help_canvas.create_text(60, 250, font=(
            "Mosk Normal 400", 18), fill="#0A1310", anchor="w", text="https://github.com/TomiwaJoseph")
        help_canvas.create_text(60, 300, font=("Mosk Normal 400", 18), fill="#0A1310",
                                anchor="w", text="https://www.linkedin.com/in/tomiwa-joseph/")
        help_canvas.create_text(60, 350, font=(
            "Mosk Normal 400", 18), fill="#0A1310", anchor="w", text="https://www.x.com/tomiwajoseph10/")

        Button(self.about_developer_veil, text="Close", bd=0, fg='#fff', bg='#0A1310', font=("fira code medium",
               13), width=16, command=self.hide_about_developer_veil).place(relx=0.5, rely=0.8, anchor="center")

    def start_new_game(self):
        return self.master.switch_frame(MainPage)

    def formatted_game_time(self, start_time, end_time):
        total_seconds = int(end_time - start_time)
        sec = total_seconds % (24 * 3600)
        hour = sec // 3600
        minute = sec // 60
        sec %= 60

        return f"{hour} hour(s), {minute} minute(s) and {sec} second(s)"

    def hide_about_app_veil(self):
        self.about_app_veil.place_forget()

    def hide_about_developer_veil(self):
        self.about_developer_veil.place_forget()

    def select_random_elements(self, input_list, num_to_select):
        selected_elements = []
        temp_list = list(input_list)

        for _ in range(num_to_select):
            random_index = randrange(len(temp_list))
            selected_elements.append(temp_list.pop(random_index))

        input_list[:] = temp_list
        return selected_elements, input_list
