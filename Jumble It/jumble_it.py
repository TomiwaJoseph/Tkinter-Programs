from tkinter import *
from tkinter import messagebox
from random import choice, shuffle
from string import ascii_letters


root = Tk
all_text_files = [
    './static/programming terms.txt','./static/occupations.txt','./static/countries.txt',
    './static/animals.txt','./static/musicians.txt','./static/12 letter words.txt','./static/football teams.txt'
]

#category word count
programming_count, occupation_count, country_count, = 0,0,0
animal_count, musician_count, long_letters_count, football_count = 0,0,0,0

#category words
programming_category_words, occupation_category_words  = [], []
country_category_words, animal_category_words = [], []
musician_category_words, long_letters_category_words = [], []
football_category_words = []

# all done words in each category
done_programming_words, done_occupation_words = [], []
done_country_words, done_animal_words = [], []
done_musician_words, done_long_letters_words = [], []
done_football_words = []

def set_all_variables():
    global programming_category_words, occupation_category_words,\
        country_category_words, animal_category_words, musician_category_words,\
        long_letters_category_words, football_category_words, programming_count,\
        occupation_count, country_count, animal_count, musician_count,\
            long_letters_count, football_count
    for text_file in all_text_files:
        with open(text_file) as file_:
            if 'programming' in text_file:
                contents = file_.readlines()
                programming_category_words = [word.strip() for word in contents]
                programming_count = len(programming_category_words)
            elif 'occupation' in text_file:
                contents = file_.readlines()
                occupation_category_words = [word.strip() for word in contents]
                occupation_count = len(occupation_category_words)
            elif 'countr' in text_file:
                contents = file_.readlines()
                country_category_words = [word.strip() for word in contents]
                country_count = len(country_category_words)
            elif 'animal' in text_file:
                contents = file_.readlines()
                animal_category_words = [word.strip() for word in contents]
                animal_count = len(animal_category_words)
            elif 'music' in text_file:
                contents = file_.readlines()
                musician_category_words = [word.strip() for word in contents]
                musician_count = len(musician_category_words)
            elif 'letter' in text_file:
                contents = file_.readlines()
                long_letters_category_words = [word.strip() for word in contents]
                long_letters_count = len(long_letters_category_words)
            elif 'football' in text_file:
                contents = file_.readlines()
                football_category_words = [word.strip() for word in contents]
                football_count = len(football_category_words)
            
set_all_variables()

game_category = 15
overall_score = 0
game_total_words = programming_count + occupation_count + country_count\
    + animal_count + musician_count + long_letters_count + football_count
finished_category = {5: 0, 10: 0, 15: 0, 20: 0, 25: 0, 30: 0, 35: 0}
done_correct_answers = []

    
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
        self._frame.place(x=0,y=0,relheight=1,relwidth=1)


class StartPage(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        Frame.configure(self,bg='#143d59')
        self.root = root
        self.root.title('Intro Page')
        self.root.geometry('600x420')
        self.root.resizable(0,0)
        #======= Title =====================
        Label(self.master,text='Jumbled Words',font='poppins 40',fg='#505050',bg='#fff').place(x=80,y=133)
        Label(self.master,text='Jumbled Words',font='poppins 40',fg='#fff',bg='#143d59').place(x=80,y=130)
        #=========== Buttons ==================
        Button(self.master,text='  Start  ',font='poppins 18',bd=0,fg='#fff',bg='#143d59',command=lambda:self.master.switch_frame(GameSettings)).place(x=240,y=200)


class GameSettings(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        Frame.configure(self,bg='#143d59')
        self.root = root
        self.root.title('Settings')
        self.root.geometry('600x420')
        self.root.resizable(0,0)
        Label(text='Select a category',bg='#143d59',fg='#fff',font='poppins 30').place(x=120,y=40)
        # ========== Checkboxes ====================
        self.programmingcheck = Button(text='Programming Terms',width=18,font='poppins 14',bg='#f4b41a',fg='#143d59',
                command=lambda:self.set_category(self.programmingcheck))
        self.programmingcheck.place(x=85,y=120)
        self.professcheck = Button(text='Occupations',width=15,font='poppins 14',bg='#f4b41a',fg='#143d59',
                command=lambda:self.set_category(self.professcheck))
        self.professcheck.place(x=320,y=120)
        self.countrycheck = Button(text='Countries',width=13,font='poppins 14',bg='#f4b41a',fg='#143d59',
                command=lambda:self.set_category(self.countrycheck))
        self.countrycheck.place(x=40,y=200)
        self.animalcheck = Button(text='Animals',width=13,font='poppins 14',bg='#f4b41a',fg='#143d59',
                command=lambda:self.set_category(self.animalcheck))
        self.animalcheck.place(x=215,y=200)
        self.musiciancheck = Button(text='Musicians',width=13,font='poppins 14',bg='#f4b41a',fg='#143d59',
                command=lambda:self.set_category(self.musiciancheck))
        self.musiciancheck.place(x=390,y=200)
        self.letterwords = Button(text='12 Letters Words',width=15,font='poppins 14',bg='#f4b41a',fg='#143d59',
                command=lambda:self.set_category(self.letterwords))
        self.letterwords.place(x=95,y=280)
        self.footballcheck = Button(text='Football Teams',width=15,font='poppins 14',bg='#f4b41a',fg='#143d59',
                command=lambda:self.set_category(self.footballcheck))
        self.footballcheck.place(x=295,y=280)
        self.check_game_done()
        
    def check_game_done(self):
        global game_category
        game_category = 0
        for key, value in finished_category.items():
            if value:
                if key == 5:
                    self.programmingcheck.config(state=DISABLED,fg='#fff',bg='#222')
                if key == 10:
                    self.professcheck.config(state=DISABLED,fg='#fff',bg='#222')
                if key == 15:
                    self.countrycheck.config(state=DISABLED,fg='#fff',bg='#222')
                if key == 20:
                    self.animalcheck.config(state=DISABLED,fg='#fff',bg='#222')
                if key == 25:
                    self.musiciancheck.config(state=DISABLED,fg='#fff',bg='#222')
                if key == 30:
                    self.letterwords.config(state=DISABLED,fg='#fff',bg='#222')
                if key == 35:
                    self.footballcheck.config(state=DISABLED,fg='#fff',bg='#222')
            
    def set_category(self, button):
        global game_category
        if button['text'] == 'Programming Terms': game_category += 5
        if button['text'] == 'Occupations': game_category += 10
        if button['text'] == 'Countries': game_category += 15
        if button['text'] == 'Animals': game_category += 20
        if button['text'] == 'Musicians': game_category += 25
        if button['text'] == '12 Letters Words': game_category += 30
        if button['text'] == 'Football Teams': game_category += 35
        
        self.master.switch_frame(Jumble)


class Jumble(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        Frame.configure(self,bg='#143d59')
        self.root = root
        self.root.title('Jumble It')
        self.root.geometry('600x420')
        self.root.resizable(0,0)
        #========= Info about Game ==============
        self.menubar = Menu()
        self.filemenu = Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='About Game',command=self.about_game)
        self.menubar.add_cascade(label='About Developer',command=self.about_developer)
        self.root.config(menu=self.menubar)
        #======== Back Button ============
        self.the_image = PhotoImage(file='./static/back_arrow.png')
        self.back = self.the_image.subsample(1,1)
        Button(image=self.back,bg="#fff",width=50,command=self.go_back).place(x=20,y=20)
        #======== Variables ========
        self.hint_count = 1
        self.rearrange = ''
        self.current_word = ''
        self.entryWord = StringVar()
        #======= UI ================
        self.showscore = Label(text='Score : '+str(overall_score),width=10,font='poppins 14',bg='#143d59',fg='#fff')
        self.showscore.place(x=445,y=15)
        self.jumbled = Label(text='',font='poppins 32',fg='#fff',bg='#143d59')
        self.jumbled.place(anchor=CENTER,relx=0.5,rely=0.24)
        self.user_entry = Entry(bg='cornsilk',textvariable=self.entryWord,font='poppins 16',
            width=30,justify='center',relief=SUNKEN,bd=5)
        self.user_entry.bind('<Return>', lambda dummy=0: self.check_if_correct())
        self.user_entry.place(x=100,y=130)
        self.hint = Button(text='Hint',width=12,font='poppins 13',bg='#f4b41a',fg='#143d59',command=self.show_letter)
        self.hint.place(x=85,y=193)
        self.submit = Button(text='Submit',width=12,font='poppins 13',bg='#f4b41a',fg='#143d59',command=self.check_if_correct)
        self.submit.place(x=238,y=193)
        self.nextWord = Button(text='Next Word',width=12,font='poppins 13',bg='#f4b41a',fg='#143d59',command=self.show_next_word)
        self.nextWord.place(x=390,y=193)
        self.show_it = Button(text='Show Word',width=20,font='poppins 13',bg='#f4b41a',fg='#143d59',command=self.show_whole_word)
        self.show_it.place(x=197,y=255)
        self.correct_or_not = Label()
        self.jumble_and_show_it()
        
    def jumble_and_show_it(self):
        self.entryWord.set('')
        self.rearrange = ''
        all_categories = {
            5:programming_category_words, 10:occupation_category_words,
            15:country_category_words, 20:animal_category_words, 25:musician_category_words,
            30:long_letters_category_words, 35:football_category_words
        }

        while len(done_correct_answers) != game_total_words:
            word = choice(all_categories.get(game_category))
            allowed_chars = [chr(i) for i in list(range(65, 91)) + list(range(97, 123))]
            word = ''.join(letter for letter in word if letter in allowed_chars + [" ",".","!"])
            splitted = []
            shuffled = []
            if word not in done_correct_answers:
                self.current_word = word
                if ' ' in word:
                    splitted += word.split()
                    for letter in splitted:
                        break_apart = list(letter)
                        shuffle(break_apart)
                        form = ''.join(break_apart)
                        shuffled.append(form)
                    self.rearrange = ' '.join(shuffled)
                    break
                else:
                    break_apart = list(word)
                    shuffle(break_apart)
                    form = ''.join(break_apart)
                    shuffled.append(form)
                    self.rearrange = ''.join(shuffled)
                    break
        print(self.current_word)
        self.jumbled.config(text=self.rearrange)
        self.user_entry.focus()

    def check_category_or_game_done(self):
        global finished_category
        
        if len(done_correct_answers) == game_total_words:
            self.master.switch_frame(FinishPage)
            return
        if game_category == 5 and len(done_programming_words) == programming_count:
            messagebox.showinfo('Complete','Congratulations, you have completed this category. Please continue.')
            finished_category[game_category] = True
            self.master.switch_frame(GameSettings)
        elif game_category == 10 and len(done_occupation_words) == occupation_count:
            messagebox.showinfo('Complete','Congratulations, you have completed this category. Please continue.')
            finished_category[game_category] = True
            self.master.switch_frame(GameSettings)
        elif game_category == 15 and len(done_country_words) == country_count:
            messagebox.showinfo('Complete','Congratulations, you have completed this category. Please continue.')
            finished_category[game_category] = True
            self.master.switch_frame(GameSettings)
        elif game_category == 20 and len(done_animal_words) == animal_count:
            messagebox.showinfo('Complete','Congratulations, you have completed this category. Please continue.')
            finished_category[game_category] = True
            self.master.switch_frame(GameSettings)
        elif game_category == 25 and len(done_musician_words) == musician_count:
            messagebox.showinfo('Complete','Congratulations, you have completed this category. Please continue.')
            finished_category[game_category] = True
            self.master.switch_frame(GameSettings)
        elif game_category == 30 and len(done_long_letters_words) == long_letters_count:
            messagebox.showinfo('Complete','Congratulations, you have completed this category. Please continue.')
            finished_category[game_category] = True
            self.master.switch_frame(GameSettings)
        elif game_category == 35 and len(done_football_words) == football_count:
            messagebox.showinfo('Complete','Congratulations, you have completed this category. Please continue.')
            finished_category[game_category] = True
            self.master.switch_frame(GameSettings)
        else:
            messagebox.showinfo('Congratulations',"You did it!\nPlease continue.")
            self.jumble_and_show_it()
    
    def check_if_correct(self):
        global overall_score,done_correct_answers,done_programming_words,\
            done_occupation_words,done_country_words,done_animal_words,\
            done_musician_words,done_long_letters_words,done_football_words
        entry = self.entryWord.get().lower()
        if entry == self.current_word.lower():
            done_correct_answers.append(self.current_word)
            overall_score += 5
            self.showscore.config(text='Score : '+str(overall_score),width=10,font='poppins 14',bg='#143d59',fg='#f4b41a')
            self.correct_or_not.place_forget()
            self.hint_count = 1
            if game_category == 5:
                done_programming_words.append(self.current_word)
            elif game_category == 10:
                done_occupation_words.append(self.current_word)
            elif game_category == 15:
                done_country_words.append(self.current_word)
            elif game_category == 20:
                done_animal_words.append(self.current_word)
            elif game_category == 25:
                done_musician_words.append(self.current_word)
            elif game_category == 30:
                done_long_letters_words.append(self.current_word)
            elif game_category == 35:
                done_football_words.append(self.current_word)
            self.check_category_or_game_done()
        else:
            self.correct_or_not.place(anchor=CENTER,relx=0.5,rely=0.85)
            self.correct_or_not.config(text='Your input is incorrect',font='poppins 18',fg='#ff6a6a',bg='#143d59')
        
    def show_letter(self):
        global overall_score
        if overall_score >= 1:
            confirm = messagebox.askyesno('Hint?','Are you sure?\nThis will reduce your score by 1point!')
            if confirm:
                overall_score -= 1
                self.hint_count += 1
                self.showscore.config(text='Score : '+str(overall_score),width=10,font='poppins 14',bg='#143d59',fg='#f4b41a')
                self.correct_or_not.place(anchor=CENTER,relx=0.5,rely=0.85)
                self.correct_or_not.config(text='Hint: '+ self.current_word[:self.hint_count],
                    font='poppins 18',fg='light green',bg='#143d59')
        else:
            self.correct_or_not.place(anchor=CENTER,relx=0.5,rely=0.85)
            self.correct_or_not.config(text="You don't have enough score points to show letter.",
                                       font='poppins 14',fg='#f4b41a',bg='#143d59')
        
    def show_next_word(self):
        self.correct_or_not.place_forget()
        self.hint_count = 1
        self.jumble_and_show_it()
    
    def show_whole_word(self):
        global overall_score
        if overall_score >= 5:
            show_or_not = messagebox.askyesno('Show?','Are you sure?\nThis will reduce your score by 5points!')
            if show_or_not:
                overall_score -= 5
                self.hint_count = 1
                self.showscore.config(text='Score : '+str(overall_score),width=10,font='poppins 14',bg='#143d59',fg='#f4b41a')
                self.correct_or_not.place(anchor=CENTER,relx=0.5,rely=0.85)
                self.correct_or_not.config(text='The Word is '+self.current_word,
                    font='poppins 18',fg='light green',bg='#143d59')
        else:
            self.correct_or_not.place(anchor=CENTER,relx=0.5,rely=0.85)
            self.correct_or_not.config(text="You don't have enough score points to show word.",
                                       font='poppins 14',fg='#f4b41a',bg='#143d59')
                  
    def go_back(self):
        global game_category
        game_category = 0
        self.master.switch_frame(GameSettings)

    def about_game(self):
        newWindow = Toplevel(self.root)
        newWindow.attributes('-topmost', 'true')
        newWindow.title('About Game')
        newWindow.config(bg='#222')
        newWindow.geometry('530x210')
        newWindow.resizable(0,0)
        Label(newWindow,text="Welcome player!\n This game scatters (jumbles) the letters of a word.\n Enter what you think the arranged word is.\n Use hints and show whole word.\n It will cost you though😎 \nEnjoy!",
              fg='#fff',bg='#222',font='montserrat 14').pack(pady=(20,5))
        
    def about_developer(self):
        newWindow = Toplevel()
        newWindow.attributes('-topmost', 'true')
        newWindow.title('About Developer')
        newWindow.config(bg='#222')
        newWindow.geometry('550x170')
        newWindow.resizable(0,0)
        Label(newWindow,text='I am an experienced python desktop\n\
            application and web programmer!\
            \nFind more of my works at:',fg='#fff',bg='#222',font='montserrat 14').pack(pady=(20,5))
        the_github = Entry(newWindow,width=30, justify='center',font='montserrat 14')
        the_github.insert(0, "https://github.com/TomiwaJoseph")
        the_github.configure(fg='#fff',state="readonly",readonlybackground="#222")
        the_github.place(x=85,y=110)
        
        

class FinishPage(Frame):
    def __init__(self,root):
        Frame.__init__(self,root) # #143d59  #f4b41a 
        Frame.configure(self,bg='#143d59')
        self.root = root
        self.root.title('Game Completed')
        self.root.geometry('600x420')
        self.root.resizable(0,0)
        #====== UI ===========
        Label(text='Congratulations!',font='poppins 34',fg='#f4b41a',bg='#143d59').place(anchor=CENTER,relx=0.5,rely=0.25)
        Label(text='You have finished the game.\nYou solved it all.',font='poppins 24',fg='white',bg='#143d59').place(anchor=CENTER,relx=0.5,rely=0.48)
        Button(text='Reset progress',width=15,command=self.reset_it,font='poppins 14',fg='#143d59',bg='#f4b41a').place(anchor=CENTER,relx=0.5,rely=0.7)   

    def reset_it(self):
        global overall_score,game_category,finished_category,done_correct_answers,\
            done_programming_words,done_occupation_words,done_country_words,done_animal_words,\
            done_musician_words,done_long_letters_words,done_football_words
        
        game_category = 0
        overall_score = 0
        finished_category = {5: 0, 10: 0, 15: 0, 20: 0, 25: 0, 30: 0, 35: 0}
        done_correct_answers = []
        done_programming_words, done_occupation_words = [], []
        done_country_words, done_animal_words = [], []
        done_musician_words, done_long_letters_words = [], []
        done_football_words = []
        self.master.switch_frame(GameSettings)
     

if __name__ == '__main__':
    app = Switch()
    app.mainloop()