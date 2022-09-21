from tkinter import *
from random import shuffle
from PIL import Image, ImageTk
import simpleaudio as sa
from threading import Timer


root = Tk
defeat_song = sa.WaveObject.from_wave_file('./gameOver.wav')
victory_song = sa.WaveObject.from_wave_file('./victory.wav')
flip_sound = sa.WaveObject.from_wave_file('./flip.wav')


class Switch(root):
    ''' Helps in `switching` windows without keeping previous window open'''

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
    ''' Displays the startpage of the application which consist of a header and an image'''

    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.configure(self, bg='#101820')
        self.root = root
        self.root.title('Start Page')
        self.root.geometry('500x500+433+134')
        self.root.resizable(0, 0)
        # ======= Title =====================
        Label(self.master, text="Card", font='montserrat 30', fg='#f2aa4c',
              bg='#101820', justify='left').place(relx=0.32, rely=0.35, anchor=CENTER)
        Label(self.master, text="Match", font='montserrat 30', fg='#f2aa4c',
              bg='#101820', justify='left').place(relx=0.35, rely=0.45, anchor=CENTER)

        self.bg = Image.open('./static/card_1.png')
        self.bg = self.bg.resize((54, 79), Image.ANTIALIAS)
        self.back1 = ImageTk.PhotoImage(self.bg)
        self.bg = Image.open('./static/card_2.png')
        self.bg = self.bg.resize((54, 79), Image.ANTIALIAS)
        self.back2 = ImageTk.PhotoImage(self.bg)

        self.first_card = Frame(width=60, height=85,
                                relief='ridge', bg='#101820', bd=2)
        self.first_card.place(relx=0.56, rely=0.4, anchor=CENTER)
        self.second_card = Frame(
            width=60, height=85, relief='ridge', bg='#101820', bd=2)
        self.second_card.place(relx=0.71, rely=0.4, anchor=CENTER)
        Label(self.first_card, image=self.back1).place(x=0, y=0)
        Label(self.second_card, image=self.back2).place(x=0, y=0)
        # =========== Buttons ==================
        self.human = Button(self.master, text='Start', font='montserrat 16', bd=2, width=20,
                            fg='#101820', bg='#f2aa4c', command=lambda: self.master.switch_frame(MainPage))
        self.human.place(relx=0.5, rely=0.56, anchor=CENTER)


class MainPage(Frame):
    ''' Displays the main page of the application which consist of cards to memorize the hidden images beneath them'''

    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.configure(self, bg='#101820')
        self.root = root
        self.root.title('Main Page')
        self.root.geometry('900x560+233+104')
        self.root.resizable(0, 0)
        #------- VARIABLES -----------#
        self.game_over = False
        self.time_frame = 30
        self.game_info = Label(text='', font='candara 42')
        self.restart_button = Button(text='Restart', font='candara 18', width=12,
                                     fg='white', bg='#101820', command=self.restartGame)
        self.time_label = Label(text='', font='candara 42')
        self.time_label.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.images_flipped = []
        self.images_flipped_buttons = []
        self.images_to_find = [
            'Cauldron', 'Dracula', 'Eye', 'Ghost', 'Pumpkin', 'Bones'
        ] * 2
        self.images_found = []

        #------- STARTER FUNCTIONS -----------#
        self.create_cards()
        self.count_down()

    def restartGame(self):
        self.game_over = False
        self.time_frame = 30
        self.images_flipped = []
        self.images_flipped_buttons = []
        self.images_found = []
        self.game_info.place_forget()
        self.restart_button.place_forget()
        self.time_label.place(relx=0.5, rely=0.1, anchor=CENTER)
        self.create_cards()
        self.count_down()

    def create_cards(self):
        shuffle(self.images_to_find)

        self.bg = Image.open('./static/card_1.png')
        self.bg = self.bg.resize((94, 140), Image.ANTIALIAS)
        self.back = ImageTk.PhotoImage(self.bg)

        self.card1 = Button(image=self.back, bg="teal", height=138, width=90, bd=0,
                            command=lambda: self.flip_card(self.card1, self.images_to_find[0]))
        self.card1.place(x=100, y=147)
        self.card2 = Button(image=self.back, bg="teal", height=138, width=90, bd=0,
                            command=lambda: self.flip_card(self.card2, self.images_to_find[1]))
        self.card2.place(x=220, y=147)
        self.card3 = Button(image=self.back, bg="teal", height=138, width=90, bd=0,
                            command=lambda: self.flip_card(self.card3, self.images_to_find[2]))
        self.card3.place(x=340, y=147)
        self.card4 = Button(image=self.back, bg="teal", height=138, width=90, bd=0,
                            command=lambda: self.flip_card(self.card4, self.images_to_find[3]))
        self.card4.place(x=460, y=147)
        self.card5 = Button(image=self.back, bg="teal", height=138, width=90, bd=0,
                            command=lambda: self.flip_card(self.card5, self.images_to_find[4]))
        self.card5.place(x=580, y=147)
        self.card6 = Button(image=self.back, bg="teal", height=138, width=90, bd=0,
                            command=lambda: self.flip_card(self.card6, self.images_to_find[5]))
        self.card6.place(x=700, y=147)

        self.card7 = Button(image=self.back, bg="teal", height=138, width=90, bd=0,
                            command=lambda: self.flip_card(self.card7, self.images_to_find[6]))
        self.card7.place(x=100, y=320)
        self.card8 = Button(image=self.back, bg="teal", height=138, width=90, bd=0,
                            command=lambda: self.flip_card(self.card8, self.images_to_find[7]))
        self.card8.place(x=220, y=320)
        self.card9 = Button(image=self.back, bg="teal", height=138, width=90, bd=0,
                            command=lambda: self.flip_card(self.card9, self.images_to_find[8]))
        self.card9.place(x=340, y=320)
        self.card10 = Button(image=self.back, bg="teal", height=138, width=90, bd=0,
                             command=lambda: self.flip_card(self.card10, self.images_to_find[9]))
        self.card10.place(x=460, y=320)
        self.card11 = Button(image=self.back, bg="teal", height=138, width=90, bd=0,
                             command=lambda: self.flip_card(self.card11, self.images_to_find[10]))
        self.card11.place(x=580, y=320)
        self.card12 = Button(image=self.back, bg="teal", height=138, width=90, bd=0,
                             command=lambda: self.flip_card(self.card12, self.images_to_find[11]))
        self.card12.place(x=700, y=320)

    def flip_card(self, button, image_name):
        if button not in self.images_flipped_buttons and len(self.images_flipped_buttons) != 2:
            play_object = flip_sound.play()
            self.images_flipped.append(image_name)
            self.images_flipped_buttons.append(button)
            # new_the_image = PhotoImage(file=f'./static/{image_name}.png')
            # inside_image = new_the_image.subsample(1)
            bg = Image.open(f'./static/{image_name}.png')
            bg = bg.resize((75, 75), Image.ANTIALIAS)
            inside_image = ImageTk.PhotoImage(bg)
            button.configure(bg='#f2aa4c', image=inside_image)
            button.image = inside_image
            if len(self.images_flipped_buttons) == 2:
                r = Timer(0.5, self.checkIfCardsMatch)
                r.start()

    def checkIfCardsMatch(self):
        a, b = self.images_flipped[0], self.images_flipped[1]
        if a == b:
            self.images_found.append(a)
            for but in self.images_flipped_buttons:
                but.place_forget()
            self.images_flipped = []
            self.images_flipped_buttons = []
        else:
            for button in self.images_flipped_buttons:
                bg = Image.open('./static/card_1.png')
                bg = bg.resize((94, 140), Image.ANTIALIAS)
                previous = ImageTk.PhotoImage(bg)
                button.configure(bg='teal', image=previous)
                button.image = previous
                self.images_flipped = []
                self.images_flipped_buttons = []
        self.checkIfAllCardFound()

    def checkIfAllCardFound(self):
        if len(self.images_found) == 6:
            play_object = victory_song.play()
            self.game_over = True
            self.game_info.config(text=f'CONGRATULATIONS!\n It took you {29 - self.time_frame} seconds.',
                                  fg='#f2aa4c', bg='#101820')
            self.game_info.place(relx=0.5, rely=0.4, anchor=CENTER)
            self.restart_button.place(relx=0.5, rely=0.65, anchor=CENTER)
            self.time_label.place_forget()

    def count_down(self):
        if self.game_over == False:
            if self.time_frame >= 10:
                mins, secs = divmod(self.time_frame, 60)
                self.time_label.config(text='{:02d}:{:02d}'.format(
                    mins, secs), bg='#101820', fg='#f2aa4c')
                self.time_frame -= 1
                self.time_label.after(1000, self.count_down)
            elif self.time_frame < 10 and self.time_frame != 0:
                mins, secs = divmod(self.time_frame, 60)
                self.time_label.config(text='{:02d}:{:02d}'.format(
                    mins, secs), bg='#101820', fg='orangered')
                self.time_frame -= 1
                self.time_label.after(1000, self.count_down)
            else:
                self.showGameOver()

    def showGameOver(self):
        # self.time_label.config(text="GAME OVER!",bg='#101820',fg='#f2aa4c')
        for but in [self.card1, self.card2, self.card3, self.card4,
                    self.card5, self.card6, self.card7, self.card8, self.card9,
                    self.card10, self.card11, self.card12]:
            but.place_forget()
        self.game_over = True
        self.game_info.config(text=f'GAME OVER!\n Please, do try again.',
                              fg='#f2aa4c', bg='#101820')
        self.game_info.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.restart_button.place(relx=0.5, rely=0.65, anchor=CENTER)
        self.time_label.place_forget()
        play_object = defeat_song.play()


if __name__ == '__main__':
    app = Switch()
    app.mainloop()
