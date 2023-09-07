from tkinter import *
from tkinter import messagebox
from random import choice

root = Tk

# Getting game words here

with open('dont_hang_words.txt') as fp:
    contents = fp.readlines()
    contents = [i.rstrip().upper() for i in contents]

all_game_words = contents


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
        Frame.configure(self, bg='cadetblue')
        self.root = root
        self.root.title('Intro Page')
        self.root.geometry('400x300')
        self.root.resizable(0, 0)
        # ======= Title =====================
        Label(self.master, text="Don't Han", font='candara 40',
              fg='#505050', bg='#fff').place(x=65, y=83)
        Label(self.master, text="Don't Hang", font='candara 40',
              fg='white', bg='cadetblue').place(x=65, y=80)
        # =========== Buttons ==================
        self.human = Button(self.master, text='Start', font='candara 18', bd=0, fg='cornsilk',
                            bg='cadetblue', command=lambda: self.master.switch_frame(MainPage))
        self.human.place(x=160, y=140)


class MainPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.configure(self, bg='cadet blue')
        self.root = root
        self.root.title("Don't Hang")
        self.root.geometry('710x540')
        self.root.resizable(0, 0)
        # ========= Info about Game ==============
        self.menubar = Menu()
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='About Game', command=self.about_game)
        self.menubar.add_cascade(
            label='About Developer', command=self.about_developer)
        self.root.config(menu=self.menubar)
        # ======= Guess buttons =================
        self.l1 = Button(text='', font='candara 32', bd=0,
                         width=2, fg='green', bg='white')
        self.l1.place(x=120, y=40)
        self.l2 = Button(text='', font='candara 32', bd=0,
                         width=2, fg='green', bg='white')
        self.l2.place(x=180, y=40)
        self.l3 = Button(text='', font='candara 32', bd=0,
                         width=2, fg='green', bg='white')
        self.l3.place(x=240, y=40)
        self.l4 = Button(text='', font='candara 32', bd=0,
                         width=2, fg='green', bg='white')
        self.l4.place(x=300, y=40)
        self.l5 = Button(text='', font='candara 32', bd=0,
                         width=2, fg='green', bg='white')
        self.l5.place(x=360, y=40)
        self.l6 = Button(text='', font='candara 32', bd=0,
                         width=2, fg='green', bg='white')
        self.l6.place(x=420, y=40)
        self.l7 = Button(text='', font='candara 32', bd=0,
                         width=2, fg='green', bg='white')
        self.l7.place(x=480, y=40)
        self.l8 = Button(text='', font='candara 32', bd=0,
                         width=2, fg='green', bg='white')
        self.l8.place(x=540, y=40)
        # ======= Game play buttons ============
        self.show = Button(text='Show Letter', font='candara 18', width=10,
                           bd=0, fg='white', bg='cadetblue', command=self.hint_them)
        self.show.place(x=60, y=145)
        self.showScore = Label(
            font='candara 18', text='Your score -> 0', bg='cadetblue', fg='white')
        self.showScore.place(x=480, y=145)
        # ======== Keyboard ==============
        self.show_keyboard()
        # ========= Other Variables ===============
        self.score = 0
        self.done_correct_words = []
        self.current_done_letters = ''
        self.current_word = ''
        self.pick_word()

    def show_keyboard(self):
        self.q = Button(text='Q', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('Q'))
        self.q.place(x=60, y=200)
        self.w = Button(text='W', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('W'))
        self.w.place(x=120, y=200)
        self.e = Button(text='E', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('E'))
        self.e.place(x=180, y=200)
        self.r = Button(text='R', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('R'))
        self.r.place(x=240, y=200)
        self.t = Button(text='T', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('T'))
        self.t.place(x=300, y=200)
        self.y = Button(text='Y', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('Y'))
        self.y.place(x=360, y=200)
        self.u = Button(text='U', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('U'))
        self.u.place(x=420, y=200)
        self.i = Button(text='I', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('I'))
        self.i.place(x=480, y=200)
        self.o = Button(text='O', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('O'))
        self.o.place(x=540, y=200)
        self.p = Button(text='P', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('P'))
        self.p.place(x=600, y=200)

        self.a = Button(text='A', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('A'))
        self.a.place(x=80, y=300)
        self.s = Button(text='S', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('S'))
        self.s.place(x=140, y=300)
        self.d = Button(text='D', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('D'))
        self.d.place(x=200, y=300)
        self.f = Button(text='F', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('F'))
        self.f.place(x=260, y=300)
        self.g = Button(text='G', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('G'))
        self.g.place(x=320, y=300)
        self.h = Button(text='H', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('H'))
        self.h.place(x=380, y=300)
        self.j = Button(text='J', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('J'))
        self.j.place(x=440, y=300)
        self.k = Button(text='K', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('K'))
        self.k.place(x=500, y=300)
        self.l = Button(text='L', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('L'))
        self.l.place(x=560, y=300)

        self.z = Button(text='Z', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('Z'))
        self.z.place(x=140, y=400)
        self.x = Button(text='X', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('X'))
        self.x.place(x=200, y=400)
        self.c = Button(text='C', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('C'))
        self.c.place(x=260, y=400)
        self.v = Button(text='V', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('V'))
        self.v.place(x=320, y=400)
        self.b = Button(text='B', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('B'))
        self.b.place(x=380, y=400)
        self.n = Button(text='N', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('N'))
        self.n.place(x=440, y=400)
        self.m = Button(text='M', font='candara 32', bd=0, width=2, activebackground='black',
                        activeforeground='white', fg='white', bg='#222', command=lambda: self.main_logic('M'))
        self.m.place(x=500, y=400)

    def check_game_done(self):
        if len(all_game_words) == len(self.done_correct_words):
            newWindow = Toplevel()
            newWindow.attributes('-topmost', 'true')
            newWindow.title('Game Completed')
            newWindow.config(bg='#222')
            newWindow.geometry('450x170')
            newWindow.resizable(0, 0)
            Label(newWindow, text='Congratulations!\n\
                You have finished the game.\
                \nYou solved it all.', fg='#fff', bg='#222',
                  font='montserrat 14').pack(pady=(30, 5))
            for i in (self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h, self.i, self.j, self.k, self.l, self.m, self.n,
                      self.o, self.p, self.q, self.r, self.s, self.t, self.u, self.v, self.w, self.x, self.y, self.z, self.show):
                i.config(state=DISABLED)
            self.l1.config(text='C')
            self.l2.config(text='O')
            self.l3.config(text='N')
            self.l4.config(text='G')
            self.l5.config(text='R')
            self.l6.config(text='A')
            self.l7.config(text='T')
            self.l8.config(text='S')
        else:
            messagebox.showinfo('Congratulations',
                                "You did it!\nPlease continue.")
            self.pick_word()

    def check_for_word(self):
        reword = ''
        for i in (self.l1, self.l2, self.l3, self.l4, self.l5, self.l6, self.l7, self.l8):
            reword += i['text']
        if reword == self.current_word:
            self.done_correct_words.append(self.current_word)
            self.check_game_done()

    def pick_word(self):
        self.current_word = ''
        self.current_done_letters = ''
        for i in (self.l1, self.l2, self.l3, self.l4, self.l5, self.l6, self.l7, self.l8):
            i['text'] = ''
        while len(all_game_words) != len(self.done_correct_words):
            pick = choice(all_game_words)
            if pick not in self.done_correct_words:
                self.current_word = pick
                break

    def hint_them(self):
        agree_to_hint = messagebox.askyesno(
            'Show?', f'Are you sure?\nThis will cost you 5 score points')
        if agree_to_hint:
            for i in range(1):
                if self.l1['text'] == '':
                    self.score -= 5
                    newWindow = Toplevel()
                    newWindow.attributes('-topmost', 'true')
                    newWindow.title('First letter')
                    newWindow.config(bg='#222')
                    newWindow.geometry('420x190')
                    newWindow.resizable(0, 0)
                    Label(newWindow, text=f'{self.current_word[0]}', fg='#fff',
                          bg='#222', font='montserrat 72').place(anchor=CENTER, relx=0.5, rely=0.55)
                    Label(newWindow, text='The first letter is:', fg='#fff', bg='#222',
                          font='montserrat 14').pack(pady=(25, 0))
                    self.showScore.config(
                        text='Your score -> ' + str(self.score))
                    break
                if self.l2['text'] == '':
                    self.score -= 5
                    newWindow = Toplevel()
                    newWindow.attributes('-topmost', 'true')
                    newWindow.title('Second letter')
                    newWindow.config(bg='#222')
                    newWindow.geometry('420x190')
                    newWindow.resizable(0, 0)
                    Label(newWindow, text=f'{self.current_word[1]}', fg='#fff',
                          bg='#222', font='montserrat 72').place(anchor=CENTER, relx=0.5, rely=0.55)
                    Label(newWindow, text='The second letter is:', fg='#fff', bg='#222',
                          font='montserrat 14').pack(pady=(25, 0))
                    self.showScore.config(
                        text='Your score -> ' + str(self.score))
                    break
                if self.l3['text'] == '':
                    self.score -= 5
                    newWindow = Toplevel()
                    newWindow.attributes('-topmost', 'true')
                    newWindow.title('Third letter')
                    newWindow.config(bg='#222')
                    newWindow.geometry('420x190')
                    newWindow.resizable(0, 0)
                    Label(newWindow, text=f'{self.current_word[2]}', fg='#fff',
                          bg='#222', font='montserrat 72').place(anchor=CENTER, relx=0.5, rely=0.55)
                    Label(newWindow, text='The third letter is:', fg='#fff', bg='#222',
                          font='montserrat 14').pack(pady=(25, 0))
                    self.showScore.config(
                        text='Your score -> ' + str(self.score))
                    break
                if self.l4['text'] == '':
                    self.score -= 5
                    newWindow = Toplevel()
                    newWindow.attributes('-topmost', 'true')
                    newWindow.title('Fourth letter')
                    newWindow.config(bg='#222')
                    newWindow.geometry('420x190')
                    newWindow.resizable(0, 0)
                    Label(newWindow, text=f'{self.current_word[3]}', fg='#fff',
                          bg='#222', font='montserrat 72').place(anchor=CENTER, relx=0.5, rely=0.55)
                    Label(newWindow, text='The fourth letter is:', fg='#fff', bg='#222',
                          font='montserrat 14').pack(pady=(25, 0))
                    self.showScore.config(
                        text='Your score -> ' + str(self.score))
                    break
                if self.l5['text'] == '':
                    self.score -= 5
                    newWindow = Toplevel()
                    newWindow.attributes('-topmost', 'true')
                    newWindow.title('Fifth letter')
                    newWindow.config(bg='#222')
                    newWindow.geometry('420x190')
                    newWindow.resizable(0, 0)
                    Label(newWindow, text=f'{self.current_word[4]}', fg='#fff',
                          bg='#222', font='montserrat 72').place(anchor=CENTER, relx=0.5, rely=0.55)
                    Label(newWindow, text='The fifth letter is:', fg='#fff', bg='#222',
                          font='montserrat 14').pack(pady=(25, 0))
                    self.showScore.config(
                        text='Your score -> ' + str(self.score))
                    break
                if self.l6['text'] == '':
                    self.score -= 5
                    newWindow = Toplevel()
                    newWindow.attributes('-topmost', 'true')
                    newWindow.title('Sixth letter')
                    newWindow.config(bg='#222')
                    newWindow.geometry('420x190')
                    newWindow.resizable(0, 0)
                    Label(newWindow, text=f'{self.current_word[5]}', fg='#fff',
                          bg='#222', font='montserrat 72').place(anchor=CENTER, relx=0.5, rely=0.55)
                    Label(newWindow, text='The sixth letter is:', fg='#fff', bg='#222',
                          font='montserrat 14').pack(pady=(25, 0))
                    self.showScore.config(
                        text='Your score -> ' + str(self.score))
                    break
                if self.l7['text'] == '':
                    self.score -= 5
                    newWindow = Toplevel()
                    newWindow.attributes('-topmost', 'true')
                    newWindow.title('Seventh letter')
                    newWindow.config(bg='#222')
                    newWindow.geometry('420x190')
                    newWindow.resizable(0, 0)
                    Label(newWindow, text=f'{self.current_word[6]}', fg='#fff',
                          bg='#222', font='montserrat 72').place(anchor=CENTER, relx=0.5, rely=0.55)
                    Label(newWindow, text='The seventh letter is:', fg='#fff', bg='#222',
                          font='montserrat 14').pack(pady=(25, 0))
                    self.showScore.config(
                        text='Your score -> ' + str(self.score))
                    break
                if self.l8['text'] == '':
                    self.score -= 5
                    newWindow = Toplevel()
                    newWindow.attributes('-topmost', 'true')
                    newWindow.title('Eighth letter')
                    newWindow.config(bg='#222')
                    newWindow.geometry('420x190')
                    newWindow.resizable(0, 0)
                    Label(newWindow, text=f'{self.current_word[7]}', fg='#fff',
                          bg='#222', font='montserrat 72').place(anchor=CENTER, relx=0.5, rely=0.55)
                    Label(newWindow, text='The eighth letter is:', fg='#fff', bg='#222',
                          font='montserrat 14').pack(pady=(25, 0))
                    self.showScore.config(
                        text='Your score -> ' + str(self.score))
                    break

    def main_logic(self, letter):
        if letter in self.current_word:
            self.current_done_letters += letter
            if letter == self.current_word[0]:
                self.l1.config(text=self.current_word[0])
                if self.current_done_letters.count(letter) == 1:
                    self.score += 5
                    self.showScore.config(
                        text='Your score -> ' + str(self.score))
            if letter == self.current_word[1]:
                self.l2.config(text=self.current_word[1])
                if self.current_done_letters.count(letter) == 1:
                    self.score += 5
                    self.showScore.config(
                        text='Your score -> ' + str(self.score))
            if letter == self.current_word[2]:
                self.l3.config(text=self.current_word[2])
                if self.current_done_letters.count(letter) == 1:
                    self.score += 5
                    self.showScore.config(
                        text='Your score -> ' + str(self.score))
            if letter == self.current_word[3]:
                self.l4.config(text=self.current_word[3])
                if self.current_done_letters.count(letter) == 1:
                    self.score += 5
                    self.showScore.config(
                        text='Your score -> ' + str(self.score))
            if letter == self.current_word[4]:
                self.l5.config(text=self.current_word[4])
                if self.current_done_letters.count(letter) == 1:
                    self.score += 5
                    self.showScore.config(
                        text='Your score -> ' + str(self.score))
            if letter == self.current_word[5]:
                self.l6.config(text=self.current_word[5])
                if self.current_done_letters.count(letter) == 1:
                    self.score += 5
                    self.showScore.config(
                        text='Your score -> ' + str(self.score))
            if letter == self.current_word[6]:
                self.l7.config(text=self.current_word[6])
                if self.current_done_letters.count(letter) == 1:
                    self.score += 5
                    self.showScore.config(
                        text='Your score -> ' + str(self.score))
            if letter == self.current_word[7]:
                self.l8.config(text=self.current_word[7])
                if self.current_done_letters.count(letter) == 1:
                    self.score += 5
                    self.showScore.config(
                        text='Your score -> ' + str(self.score))
        else:
            self.score -= 2
            self.showScore.config(text='Your score -> ' + str(self.score))

        self.check_for_word()

    def about_game(self):
        newWindow = Toplevel(self.root)
        newWindow.attributes('-topmost', 'true')
        newWindow.title('About Game')
        newWindow.config(bg='#222')
        newWindow.geometry('530x220')
        newWindow.resizable(0, 0)
        Label(newWindow, text="This is a variant of the Hangman Game.\n In this variation you won't hang.\n Wrong letter you press is -2 points\n Right letter you press is +5 points\n Show letter is -5 points\nEnjoy!",
              fg='#fff', bg='#222', font='montserrat 14').pack(pady=(20, 5))

    def about_developer(self):
        newWindow = Toplevel()
        newWindow.attributes('-topmost', 'true')
        newWindow.title('About Developer')
        newWindow.config(bg='#222')
        newWindow.geometry('550x170')
        newWindow.resizable(0, 0)
        Label(newWindow, text='I am an experienced python desktop\n\
            application and web programmer!\
            \nFind more of my works at:', fg='#fff', bg='#222', font='montserrat 14').pack(pady=(20, 5))
        the_github = Entry(newWindow, width=30,
                           justify='center', font='montserrat 14')
        the_github.insert(0, "https://github.com/TomiwaJoseph")
        the_github.configure(fg='#fff', state="readonly",
                             readonlybackground="#222")
        the_github.place(x=85, y=110)


if __name__ == '__main__':
    app = Switch()
    app.mainloop()
