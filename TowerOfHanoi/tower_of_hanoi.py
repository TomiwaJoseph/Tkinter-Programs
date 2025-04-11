from tkinter import Label, Frame, Tk, Canvas, Button, Menu, StringVar, Entry, messagebox
from PIL import ImageTk, Image
from random import shuffle

root = Tk
DISC_COUNT = 0


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
        Frame.configure(self, bg='#101820')
        self.root = root
        self.root.title('Intro Page')
        self.root.geometry('630x410+368+179')
        self.root.resizable(0, 0)
        # ======= Title =====================
        Label(self.master, text='Tower of Hanoi', font='montserrat 40',
              fg='#505050', bg='#fff').place(relx=0.5, rely=0.42, anchor="center")
        Label(self.master, text='Tower of Hanoi', font='montserrat 40',
              fg='#fff', bg='#101820').place(relx=0.5, rely=0.41, anchor="center")
        Button(self.master, text='Start', width=10, font=('montserrat medium', 14), bd=0, fg='#101820', bg='#fff',
               command=lambda: self.master.switch_frame(SetDiscs)).place(relx=0.5, rely=0.59, anchor="center")


class SetDiscs(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.configure(self, bg='#101820')
        self.root = root
        self.root.title('Settings Page')
        self.root.geometry('530x310+418+229')
        self.root.config(menu=" ")
        self.root.resizable(0, 0)
        # ======== Variables ==========
        self.disc_variable = StringVar()
        self.disc_variable.set("3")
        # ============ UI =============
        Label(text='Number of disc(s):', font=('fira code', 14),
              bg='#101820', fg='white').place(relx=0.435, rely=0.4, anchor="center")
        self.disc_number = Entry(textvariable=self.disc_variable, width=4,
                                 font=('fira code', 14), justify="center")
        self.disc_number.place(relx=0.685, rely=0.4, anchor="center")

        Button(text='Start Solving!', font=('fira code', 14), bg='#101820', fg='orange', width=17,
               command=self.validate_input).place(relx=0.5, rely=0.6, anchor="center")

    def validate_input(self):
        global DISC_COUNT
        try:
            disc_count_entry = int(self.disc_variable.get())
            if disc_count_entry > 9:
                messagebox.showerror(
                    "Info", "Please type in a number less than 10.")
                return
            elif disc_count_entry < 1:
                messagebox.showerror(
                    "Info", "Please type in a number greater than 0.")
                return
            DISC_COUNT = disc_count_entry
            self.master.switch_frame(MainPage)
        except ValueError:
            messagebox.showerror("Error", "Type in a number, stupe!")


class MainPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.configure(self, bg='#101820')
        self.root = root
        self.root.title('Tower of Hanoi')
        self.root.geometry('830x610+268+79')
        self.root.resizable(0, 0)
        # ======= Varibles =======
        self.moves_count = 0
        self.source_pole_state = []
        self.auxillary_pole_state = []
        self.destination_pole_state = []
        self.images_ref = []
        self.tag_and_id = {}
        self.disc_depths = {}
        self.drag_parameters = {}
        self.animation_done = True
        self.menu_option_is_open = False
        # ========= Info about Game ==============
        self.menubar = Menu()
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='About Puzzle', command=self.about_game)
        self.menubar.add_cascade(
            label='About Developer', command=self.about_developer)
        self.root.config(menu=self.menubar)
        # ======== Back Button ============
        self.bg = Image.open('./static/back_arrow.png')
        self.bg = self.bg.resize((35, 35), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.bg)
        Button(image=self.bg, bg="#fff",
               command=self.go_back).place(x=20, y=20)
        # ======= Moves Counter ============
        self.moves = Label(text=f'{self.moves_count} move(s)', fg="white", font=(
            "fira code", 20), bg="#101820")
        self.moves.place(relx=0.95, rely=0.065, anchor="e")
        # ======= Win Message and Restart Button ============
        self.win_message = Label(text='Congrats! You have solved the puzzle.', fg="white", font=(
            "fira code", 20), bg="#101820")
        self.restart_button = Button(text='Restart', font=(
            "fira code", 16), width=12, bg="#fff", command=self.restart_puzzle)
        # ======= Canvas ============
        self.canvas = Canvas(width=600, height=350,
                             background="#101820", bd=0, highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.47, anchor="center")
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        self.canvas_width, self.canvas_height = self.root.getint(
            self.canvas['width']), self.root.getint(self.canvas['height'])

        self.generate_poles()
        self.generate_disc()

    def about_game(self):
        if self.menu_option_is_open:
            self.about_developer_veil.place_forget()
        self.menu_option_is_open = True
        self.about_game_veil = Frame(width=830, height=610, bg='#101820')
        self.about_game_veil.place(x=0, y=0)
        self.about_bg = Image.open('./static/back_arrow.png')
        self.about_bg = self.about_bg.resize((35, 35), Image.LANCZOS)
        self.about_bg = ImageTk.PhotoImage(self.about_bg)
        Button(self.about_game_veil, image=self.about_bg, bg="#fff",
               command=lambda: self.hide_menu_veil('about')).place(x=20, y=20)
        a = f"Welcome! \n\nCan you move the {DISC_COUNT} disc(s) to the second\n or third pole in order of largest to smallest?"
        b = "\n\n How to move:\n-> Click on a pole to move the smallest disc\n on that pole to the nearest valid pole"
        c = "\n-> You can also click and drag a disc to a valid\n pole to move it\n\n Enjoy!"
        about_text = a + b + c
        Label(self.about_game_veil, text=about_text, font=("fira code", 16), fg='#fff', bg='#101820').place(
            relx=0.5, rely=0.5, anchor="center")

    def hide_menu_veil(self, section):
        self.menu_option_is_open = False
        if section == 'about':
            self.about_game_veil.place_forget()
        else:
            self.about_developer_veil.place_forget()

    def about_developer(self):
        if self.menu_option_is_open:
            self.about_game_veil.place_forget()
        self.menu_option_is_open = True
        self.about_developer_veil = Frame(width=830, height=610, bg='#101820')
        self.about_developer_veil.place(x=0, y=0)
        self.dev_bg = Image.open('./static/back_arrow.png')
        self.dev_bg = self.dev_bg.resize((35, 35), Image.LANCZOS)
        self.dev_bg = ImageTk.PhotoImage(self.dev_bg)
        Button(self.about_developer_veil, image=self.dev_bg, bg="#fff",
               command=lambda: self.hide_menu_veil('developer')).place(x=20, y=20)
        a = "I am Tomiwa Joseph, a software developer."
        b = "\nI am passionate about bringing both "
        c = "the technical and \nvisual aspects of digital products to life. \nAs a "
        d = "software developer, I enjoy bridging the gap\nbetween development and design. "
        e = "My goal always is \nto build scalable, optimized user-friendly,"
        f = "interactive, \naccessible, secure, fast, responsive and feature-rich \napplications."
        about_text = a + b + c + d + e + f
        Label(self.about_developer_veil, text=about_text, justify='left', font=("fira code", 16), fg='#fff', bg='#101820').place(
            relx=0.05, rely=0.5, anchor="w")

    def check_for_win(self):
        if len(self.auxillary_pole_state) == DISC_COUNT or len(self.destination_pole_state) == DISC_COUNT:
            self.win_message.place(relx=0.5, rely=0.8, anchor="center")
            self.restart_button.place(relx=0.5, rely=0.9, anchor="center")

    def restart_puzzle(self):
        self.moves_count = 0
        self.source_pole_state = []
        self.auxillary_pole_state = []
        self.destination_pole_state = []
        self.images_ref = []
        self.tag_and_id = {}
        self.disc_depths = {}
        self.drag_parameters = {}
        self.animation_done = True
        self.menu_option_is_open = False
        self.win_message.place_forget()
        self.restart_button.place_forget()
        self.moves['text'] = f'{self.moves_count} move(s)'

        self.generate_disc()

    def find_clicked_disc_and_pole(self, tag):
        if tag not in ['source', 'auxillary', 'destination']:
            if int(tag) in self.source_pole_state:
                return self.source_pole_state[0], "source"
            elif int(tag) in self.auxillary_pole_state:
                return self.auxillary_pole_state[0], "auxillary"
            elif int(tag) in self.destination_pole_state:
                return self.destination_pole_state[0], "destination"
        else:
            return 0, ""

    def pole_is_clicked(self, event):
        current_tag = self.canvas.gettags('current')[0]
        least_disc = 0
        clicked_pole = ""
        if self.animation_done:
            if current_tag == 'source' and self.source_pole_state != []:
                least_disc = self.source_pole_state[0]
                clicked_pole = "source"
            elif current_tag == 'auxillary' and self.auxillary_pole_state != []:
                least_disc = self.auxillary_pole_state[0]
                clicked_pole = "auxillary"
            elif current_tag == 'destination' and self.destination_pole_state != []:
                least_disc = self.destination_pole_state[0]
                clicked_pole = "destination"
            else:
                least_disc, clicked_pole = self.find_clicked_disc_and_pole(
                    current_tag)

            if least_disc and clicked_pole:
                check_possible = self.check_if_possible(
                    least_disc, clicked_pole)
                if isinstance(check_possible, (tuple)):
                    valid, from_disc, direction, destination = check_possible
                    return self.move_disc_up(self.tag_and_id[least_disc], from_disc, direction, destination)

    def check_if_possible(self, disc, pole):
        if pole == "source":
            # if auxillary pole is empty
            if self.auxillary_pole_state == []:
                return True, "source", "right", "auxillary"
            # if auxillary pole is not empty
            elif self.auxillary_pole_state != []:
                # check if the first element of auxillary is greater than
                # the incomming number
                if self.auxillary_pole_state[0] > disc:
                    return True, "source", "right", "auxillary"
                else:
                    # check if destination pole is empty
                    if self.destination_pole_state == []:
                        return True, "source", "right right", "destination"
                    # if destination pole is not empty
                    elif self.destination_pole_state != []:
                        if self.destination_pole_state[0] > disc:
                            return True, "source", "right right", "destination"
            return False
        elif pole == "auxillary":
            # if destination pole is empty
            if self.destination_pole_state == []:
                return True, "auxillary", "right", "destination"
            # if destination pole is not empty
            elif self.destination_pole_state != []:
                # check if the first element of destination is greater than
                # the incomming number
                if self.destination_pole_state[0] > disc:
                    return True, "auxillary", "right", "destination"
                else:
                    # check if source pole is empty
                    if self.source_pole_state == []:
                        return True, "auxillary", "left", "source"
                    # if source pole is not empty
                    elif self.source_pole_state != []:
                        if self.source_pole_state[0] > disc:
                            return True, "auxillary", "left", "source"
            return False
        elif pole == "destination":
            # if auxillary pole is empty
            if self.auxillary_pole_state == []:
                return True, "destination", "left", "auxillary"
            # if auxillary pole is not empty
            elif self.auxillary_pole_state != []:
                # check if the first element of auxillary is greater than
                # the incomming number
                if self.auxillary_pole_state[0] > disc:
                    return True, "destination", "left", "auxillary"
                else:
                    # check if source pole is empty
                    if self.source_pole_state == []:
                        return True, "destination", "left left", "source"
                    # if source pole is not empty
                    elif self.source_pole_state != []:
                        if self.source_pole_state[0] > disc:
                            return True, "destination", "left left", "source"
            return False
        else:
            return False

    def get_disc_depth(self, dest):
        if dest == 'source':
            depth = self.disc_depths[len(self.source_pole_state)]
            pass
        elif dest == 'auxillary':
            depth = self.disc_depths[len(self.auxillary_pole_state)]
            pass
        else:
            depth = self.disc_depths[len(self.destination_pole_state)]

        return depth

    def move_disc_down(self, disc, the_low, dest):
        self.canvas.move(disc, 0, 1)
        pos = self.canvas.coords(disc)

        # Move the disc down
        if pos[1] != the_low:
            self.animation_done = False
            return self.canvas.after(1, self.move_disc_down, disc, the_low, dest)
        else:
            the_tag = [k for k, v in self.tag_and_id.items() if v == disc][0]
            if dest == 'source':
                self.source_pole_state.insert(0, the_tag)
            elif dest == 'auxillary':
                self.auxillary_pole_state.insert(0, the_tag)
            else:
                self.destination_pole_state.insert(0, the_tag)
            self.animation_done = True

        self.moves_count += 1
        self.moves['text'] = f"{self.moves_count} move(s)"
        self.check_for_win()

    def move_disc_to_side(self, disc, left_or_right, source, dest):
        if source == 'source':
            if left_or_right == 'right':
                stop_point = 300
            elif left_or_right == 'right right':
                stop_point = 467
        elif source == 'auxillary':
            if left_or_right == 'right':
                stop_point = 467
            elif left_or_right == 'left':
                stop_point = 133
        elif source == 'destination':
            if left_or_right == 'left':
                stop_point = 300
            elif left_or_right == 'left left':
                stop_point = 133

        if left_or_right in ['right', 'right right']:
            self.canvas.move(disc, 1, 0)
        else:
            self.canvas.move(disc, -1, 0)

        pos = self.canvas.coords(disc)

        # Move the disc up to the top of the next
        # or previous pole
        if pos[0] != stop_point:
            self.animation_done = False
            return self.canvas.after(1, self.move_disc_to_side, disc, left_or_right, source, dest)
        else:
            if source == 'source':
                del self.source_pole_state[0]
            elif source == 'auxillary':
                del self.auxillary_pole_state[0]
            else:
                del self.destination_pole_state[0]
            self.animation_done = True

        depth_down = self.get_disc_depth(dest)
        return self.move_disc_down(disc, depth_down, dest)

    def move_disc_up(self, disc, pole, direction, dest):
        self.canvas.move(disc, 0, -1)
        pos = self.canvas.coords(disc)

        # Lift the disc up to the top of the pole
        if pos[1] != 33:
            self.animation_done = False
            return self.canvas.after(1, self.move_disc_up, disc, pole, direction, dest)
        else:
            self.animation_done = True

        return self.move_disc_to_side(disc, direction, pole, dest)

    def generate_disc(self):
        y_position = 277
        depth_position = 277
        all_widths = [130]

        for i in range(DISC_COUNT-1):
            max_width = all_widths[-1]
            difference = max_width // DISC_COUNT
            new_width = max_width - difference
            all_widths.append(new_width)

        for i in range(DISC_COUNT):
            self.disc_depths[i] = depth_position
            new_position = depth_position - 22
            depth_position = new_position

        all_colors = [1, 2, 3, 4, 5]
        shuffle(all_colors)

        for i in range(len(all_widths), 0, -1):
            self.disc_img = Image.open(
                f'./static/disc-{all_colors[i % 5]}.png')
            self.disc_img = self.disc_img.resize(
                (all_widths[DISC_COUNT-i], 22), Image.LANCZOS)
            self.disc_img = ImageTk.PhotoImage(self.disc_img)
            self.images_ref.append(self.disc_img)
            disc = self.canvas.create_image(
                self.canvas_width//4.5, y_position, image=self.images_ref[-1], tags=all_widths[DISC_COUNT-i])
            self.tag_and_id[all_widths[DISC_COUNT-i]] = disc
            y_position -= 22
            self.canvas.tag_bind(disc, '<B1-Motion>',
                                 self.pole_or_disc_is_dragged)
            self.source_pole_state = all_widths[::-1]

    def on_canvas_click(self, event):
        x = event.x
        y = event.y
        closest_item = self.canvas.find_closest(x, y)[0]
        if closest_item >= 4:
            self.clicked_item = closest_item

    def on_canvas_release(self, event):
        if self.animation_done:
            if len(self.drag_parameters) == 3:
                disc = self.drag_parameters["disc"]
                pole_from = self.drag_parameters["pole_from"]
                pole_to = self.drag_parameters["pole_to"]

                if pole_from == "source" and pole_to != 1:
                    check_possible = self.check_if_drag_is_possible(
                        disc, pole_from, pole_to)
                elif pole_from == "auxillary" and pole_to != 2:
                    check_possible = self.check_if_drag_is_possible(
                        disc, pole_from, pole_to)
                elif pole_from == "destination" and pole_to != 3:
                    check_possible = self.check_if_drag_is_possible(
                        disc, pole_from, pole_to)
                else:
                    return

                if isinstance(check_possible, (tuple)):
                    valid, from_disc, direction, destination = check_possible
                    return self.move_disc_up(self.tag_and_id[disc], from_disc, direction, destination)

    def pole_or_disc_is_dragged(self, event):
        x = event.x
        y = event.y
        closest_item = self.canvas.find_closest(x, y)[0]
        if closest_item <= 3:
            self.drag_parameters['pole_to'] = closest_item

        disc_clicked = [
            k for k, v in self.tag_and_id.items() if v == self.clicked_item][0]
        self.drag_parameters['disc'] = disc_clicked

        if disc_clicked in self.source_pole_state:
            least_disc = min(self.source_pole_state)
            if disc_clicked == least_disc:
                self.drag_parameters['pole_from'] = 'source'
            else:
                self.drag_parameters = {}
        elif disc_clicked in self.auxillary_pole_state:
            least_disc = min(self.auxillary_pole_state)
            if disc_clicked == least_disc:
                self.drag_parameters['pole_from'] = 'auxillary'
            else:
                self.drag_parameters = {}
        elif disc_clicked in self.destination_pole_state:
            least_disc = min(self.destination_pole_state)
            if disc_clicked == least_disc:
                self.drag_parameters['pole_from'] = 'destination'
            else:
                self.drag_parameters = {}

    def check_if_drag_is_possible(self, disc, pole_from, pole_to):
        pole_map = {
            1: self.source_pole_state, 2: self.auxillary_pole_state,
            3: self.destination_pole_state
        }
        pole_string_map = {1: "source", 2: "auxillary", 3: "destination"}
        results = []

        if pole_from == "source":
            # check if the destination pole is possible
            dest = pole_map[pole_to]
            if dest == [] or dest and dest[0] > disc:
                results.extend([True, "source"])
        elif pole_from == "auxillary":
            # check if the destination pole is possible
            dest = pole_map[pole_to]
            if dest == [] or dest and dest[0] > disc:
                results.extend([True, "auxillary"])
        elif pole_from == "destination":
            # check if the destination pole is possible
            dest = pole_map[pole_to]
            if dest == [] or dest and dest[0] > disc:
                results.extend([True, "destination"])

        disc_destination = pole_string_map[pole_to]
        if pole_from == "source" and disc_destination == "auxillary":
            dir_and_dest = "right", "auxillary"
        elif pole_from == "source" and disc_destination == "destination":
            dir_and_dest = "right right", "destination"
        elif pole_from == "auxillary" and disc_destination == "destination":
            dir_and_dest = "right", "destination"
        elif pole_from == "auxillary" and disc_destination == "source":
            dir_and_dest = "left", "source"
        elif pole_from == "destination" and disc_destination == "auxillary":
            dir_and_dest = "left", "auxillary"
        elif pole_from == "destination" and disc_destination == "source":
            dir_and_dest = "left left", "source"

        if results:
            a, b = results
            c, d = dir_and_dest
            return a, b, c, d

        return False

    def generate_poles(self):
        # Generate pegs
        self.pole1_img = Image.open('./static/pole.png')
        self.pole1_img = self.pole1_img.resize((150, 250), Image.LANCZOS)
        self.pole1_img = ImageTk.PhotoImage(self.pole1_img)
        source = self.canvas.create_image(
            self.canvas_width//4.5, self.canvas_height//2, image=self.pole1_img, tags='source')
        auxillary = self.canvas.create_image(
            self.canvas_width//2, self.canvas_height//2, image=self.pole1_img, tags='auxillary')
        destination = self.canvas.create_image(
            self.canvas_width - self.canvas_width//4.5, self.canvas_height//2, image=self.pole1_img, tags='destination')

        self.canvas.tag_bind(source, '<Button-1>', self.pole_is_clicked)
        self.canvas.tag_bind(auxillary, '<Button-1>', self.pole_is_clicked)
        self.canvas.tag_bind(destination, '<Button-1>', self.pole_is_clicked)

    def go_back(self):
        self.master.switch_frame(SetDiscs)


if __name__ == '__main__':
    app = Switch()
    app.attributes("-alpha", 0.9)  # sets transparency
    app.attributes('-topmost', 1)  # stay on top
    app.mainloop()
