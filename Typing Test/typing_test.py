from tkinter import Tk, Frame, Label, Label, Canvas, Button, Text
import time
from random import choices, shuffle
from threading import Timer


root = Tk


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
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.configure(self, bg='#1a1a1a')
        self.root = root
        self.root.resizable(0, 0)
        self.root.geometry('500x200+433+284')
        self.root.title('Welcome Page')
        # ======= Title =====================
        Label(self.master, text='Typing Test', font=('Fira Code', 42),
              fg='#505050', bg='#f2aa4c').place(relx=0.5, rely=0.399, anchor='center')
        Label(self.master, text='Typing Test', font=('Fira Code', 42),
              fg='#fff', bg='#1a1a1a').place(relx=0.5, rely=0.39, anchor='center')
        startpage_timer = Timer(
            3, lambda: self.master.switch_frame(InstructionPage))
        startpage_timer.start()


class InstructionPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.configure(self, bg='#1a1a1a')
        self.root = root
        self.root.resizable(0, 0)
        self.root.geometry('700x400+333+184')
        self.root.title('Instruction Page')
        # ======= Instruction =====================
        Label(text='Hello typist!\nType all the words with spaces in-between them.\nWishing you good luck!', font=(
            'Fira Code', 18), fg='#fff', bg='#1a1a1a').place(relx=0.5, rely=0.4, anchor='center')
        Button(text='S T A R T', bg='#f2aa4c', fg='#fff', font=('dosis', 14), width=18, bd=0,
               command=lambda: self.master.switch_frame(MainPage)).place(relx=0.5, rely=0.65, anchor='center')


class MainPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.configure(self, bg='#1a1a1a')
        self.root = root
        self.root.geometry('1200x620+83+74')
        self.root.resizable(0, 0)
        self.root.config(cursor='none')
        self.root.title('Typing Test')
        # =============== Variables ============#
        self.TEXT_TO_TYPE = ""
        self.cursor = 0
        self.current_text = []
        self.actual_type = ''
        self.time_when_typing_started = 0.0
        # =============== UI ============#
        self.canvas = Canvas(bg='#1a1a1a', width=1200, height=620)
        self.canvas.place(relx=0.5, rely=0, anchor='n')
        self.canvas.create_line(20, 520, 1180, 520, fill='#fff', width=3)
        self.canvas.create_line(20, 590, 1180, 590, fill='#fff', width=3)

        self.the_text = Label(justify='left', text=self.TEXT_TO_TYPE, font=(
            'dosis', 24), name='main_text', fg='#fff', wraplength=550, bg='#1a1a1a')
        self.the_text.place(x=40, y=40)

        self.wpm_label = Label(text="WPM:", font=(
            'dosis', 24), fg='#fff', bg='#1a1a1a')
        self.wpm_label.place(relx=0.1, rely=0.89, anchor='center')
        self.wpm = Label(text="0", font=(
            'dosis', 24), fg='yellow', bg='#1a1a1a')
        self.wpm.place(relx=0.165, rely=0.89, anchor='center')

        self.accuracy_label = Label(text="Acurracy:", font=(
            'dosis', 24), fg='#fff', bg='#1a1a1a')
        self.accuracy_label.place(relx=0.45, rely=0.89, anchor='center')
        self.accuracy = Label(text="100%", font=(
            'dosis', 24), fg='yellow', bg='#1a1a1a')
        self.accuracy.place(relx=0.56, rely=0.89, anchor='center')

        self.awpm_label = Label(text="AWPM:", font=(
            'dosis', 24), fg='#fff', bg='#1a1a1a')
        self.awpm_label.place(relx=0.85, rely=0.89, anchor='center')
        self.awpm = Label(text="0", font=(
            'dosis', 24), fg='yellow', bg='#1a1a1a')
        self.awpm.place(relx=0.92, rely=0.89, anchor='center')

        # =============== TEXTAREA UI ============#
        self.text_area = Text(width=32, height=10, wrap='word',
                              border=3, relief='groove', bg='#fff', font=('dosis', 24))
        self.text_area.place(relx=0.74, rely=0.428, anchor='center')
        self.text_area.focus()
        self.text_area.tag_config('correct', foreground='green')
        self.text_area.tag_config('incorrect', foreground='red')

        self.generate_words()
        self.bind_keys()

    def bind_keys(self):
        self.text_area.bind('<KeyRelease>', self.know_key)
        self.text_area.bind('<BackSpace>', self.clean_text)
        self.text_area.bind('<Control-a>', lambda event: 'break')
        self.text_area.bind('<Control-A>', lambda event: 'break')
        self.text_area.bind('<Double-1>', lambda event: 'break')
        self.text_area.bind('<ButtonPress-1>', lambda event: 'break')
        self.text_area.bind('<Up>', lambda event: 'break')
        self.text_area.bind('<Down>', lambda event: 'break')
        self.text_area.bind('<Left>', lambda event: 'break')
        self.text_area.bind('<Right>', lambda event: 'break')
        self.text_area.bind('<Tab>', lambda event: 'break')
        # Disable all Mouse Events
        self.text_area.bind('<Button-1>', lambda event: 'break')
        self.text_area.bind('<B1-Motion>', lambda event: 'break')
        self.text_area.bind('<Button-2>', lambda event: 'break')
        self.text_area.bind('<Button-3>', lambda event: 'break')
        self.text_area.bind('<B2-Motion>', lambda event: 'break')
        self.text_area.bind('<B3-Motion>', lambda event: 'break')
        self.text_area.bind('<Enter>', lambda event: 'break')
        self.text_area.bind('<Leave>', lambda event: 'break')

    def clean_text(self, event):
        if self.cursor != 0:
            self.cursor -= 1
            self.actual_type = self.actual_type[:-1]
            self.current_text.pop()

    def end_session(self):
        self.text_area.config(state='disabled')
        self.root.unbind("all")
        self.the_text.place_forget()
        self.text_area.place_forget()
        self.restart_button = Button(text='Restart', font=(
            'dosis', 18), width=15, bd=0, command=self.restart_test)
        self.restart_button.place(relx=0.5, rely=0.5, anchor='center')

    def restart_test(self):
        self.restart_button.place_forget()
        self.text_area.config(state='normal')
        self.text_area.delete(1.0, 'end')
        self.text_area.focus()
        self.wpm.config(text='0')
        self.accuracy.config(text='100%')
        self.awpm.config(text='0')

        self.generate_words()
        self.bind_keys()
        self.the_text.place(x=40, y=40)
        self.text_area.place(relx=0.74, rely=0.428, anchor='center')
        self.cursor = 0
        self.current_text = []
        self.actual_type = ''
        self.time_when_typing_started = 0.0

    def generate_words(self):
        with open('dictionary.txt') as fp:
            content = fp.readlines()
            words = [word.strip() for word in content]

        three_letter_choices = [i for i in words if len(i) == 3]
        four_letter_choices = [i for i in words if len(i) == 4]
        five_letter_choices = [i for i in words if len(i) == 5]
        six_letter_choices = [i for i in words if len(i) == 6]
        seven_letter_choices = [i for i in words if len(i) == 7]
        eight_letter_choices = [i for i in words if len(i) == 8]

        final_words = []
        all_choices = [three_letter_choices, four_letter_choices,
                       five_letter_choices, six_letter_choices,
                       seven_letter_choices, eight_letter_choices]
        random_count = {0: 18, 1: 14, 2: 19, 3: 17, 4: 20, 5: 17}
        new_dictionary = {}
        for ind in range(6):
            shuffle(all_choices[ind])
            new_dictionary[ind] = choices(
                all_choices[ind], k=random_count[ind])
            final_words.extend(choices(all_choices[ind], k=random_count[ind]))

        final_words = []
        number_to_choose = {0: 10, 1: 12, 2: 11, 3: 9, 4: 11, 5: 9}
        for key, value in new_dictionary.items():
            final_words.extend(value[:number_to_choose[key]])

        shuffle(final_words)
        self.the_text.config(text=' '.join(final_words))
        self.TEXT_TO_TYPE = " ".join(final_words)

    def know_key(self, event):
        modifiers = ['Caps_Lock', 'Shift_L', 'Shift_R', 'BackSpace',
                     'Up', 'Down', 'Left', 'Right', 'Alt_L', 'Alt_R', 'Tab']

        if self.cursor == len(self.TEXT_TO_TYPE):
            return

        if self.time_when_typing_started == 0.0:
            self.time_when_typing_started = time.time()

        row = self.text_area.index('insert').split('.')[0]
        new_row = row + '.' + str(self.cursor)
        new_col = row + '.' + str(self.cursor + 1)

        if event.keysym == 'space' and self.TEXT_TO_TYPE[self.cursor] == ' ':
            self.actual_type += " "
            self.current_text.append(self.TEXT_TO_TYPE[self.cursor])
            self.cursor += 1
        elif event.keysym == self.TEXT_TO_TYPE[self.cursor] and event.keysym not in modifiers:
            self.actual_type += event.keysym
            self.current_text.append(self.TEXT_TO_TYPE[self.cursor])
            self.text_area.tag_add('correct', new_row, new_col)
            self.cursor += 1
            self.show_results()
        elif event.keysym != self.TEXT_TO_TYPE[self.cursor] and event.keysym not in modifiers:
            self.actual_type += event.keysym
            self.current_text.append(self.TEXT_TO_TYPE[self.cursor])
            self.text_area.tag_add('incorrect', new_row, new_col)
            self.cursor += 1
            self.show_results()

    def show_results(self):
        if self.cursor == len(self.TEXT_TO_TYPE):
            self.end_session()

        time_elapsed = max(time.time() - self.time_when_typing_started, 1)
        wpm = round((len(self.current_text) / (time_elapsed / 60)) / 5)
        correct_letters = [1 for i in range(
            self.cursor) if self.actual_type[i] == self.TEXT_TO_TYPE[i]]
        accuracy = round((len(correct_letters) / len(self.current_text)) * 100)
        adjusted_wpm = round(wpm * (accuracy/100))

        self.wpm.config(text=wpm)
        self.accuracy.config(text=str(accuracy) + '%')
        self.awpm.config(text=adjusted_wpm)


if __name__ == '__main__':
    app = Switch()
    app.mainloop()
