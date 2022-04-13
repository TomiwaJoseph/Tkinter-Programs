from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import *
import os
from PIL import ImageTk, Image


# VARIABLES
root = Tk()
choice = StringVar()
stat_bar = IntVar()
_file = None

#====== Themes ===========
color_schemes = {
    'Default': '#000-#fff',
    'Greygarious': '#83406A-#D1D4D1-#83406A',
    'Aquamarine': '#5B8340-#D1E7E0-#5B8340',
    'Bold Beige': '#4B4620-#FFF0E1-#4B4620',
    'Cobalt Blue': '#ffffBB-#3333aa-#fff',
    'Olive Green': '#D1E7E0-#5B8340-#D1E7E0',
    'Night Mode': '#fff-#000-#fff',
    "Black 'N Yellow": '#ff0-#000-#ff0'
}


class App():
    def __init__(self):
        root.geometry('650x450')
        root.title('Untitled  |  Take Note')
        root.protocol('WM_DELETE_WINDOW', self.exit_editor)
        
        #===== Shortcut Bar ============
        self.shortcut_bar = Frame(height=25)
        self.shortcut_bar.pack(expand='no', fill='x')
        
        #========== Text Area ==========
        self.text_area = Text(autoseparators=True,undo=5,font='montserrat 14')
        self.text_area.pack(expand=YES,fill=BOTH)
        self.text_area.focus()
        
        #====== Status Bar ===========
        self.status_bar = Label(self.text_area, text='Line: 1 | Column: 1')
        
        #====== Key press Bindings ===========
        self.text_area.bind('<Control-N>', self.new_file)
        self.text_area.bind('<Control-n>', self.new_file)
        self.text_area.bind('<Control-O>', self.open_file)
        self.text_area.bind('<Control-o>', self.open_file)
        self.text_area.bind('<Control-S>', self.save_file)
        self.text_area.bind('<Control-s>', self.save_file)
        self.text_area.bind('<Control-f>', self.find_text)
        self.text_area.bind('<Control-F>', self.find_text)
        self.text_area.bind('<Control-A>', self.select_all_text)
        self.text_area.bind('<Control-a>', self.select_all_text)
        self.text_area.bind('<F2>', self.about_app)
        self.text_area.bind('<Any-KeyPress>', self.update_note_stats)
        #===== MenuBars =========
        self.new_file_icon = PhotoImage(file='./static/new_file.gif')
        self.open_file_icon = PhotoImage(file='./static/open_file.gif')
        self.save_file_icon = PhotoImage(file='./static/save.gif')
        self.cut_icon = PhotoImage(file='./static/cut.gif')
        self.copy_icon = PhotoImage(file='./static/copy.gif')
        self.paste_icon =PhotoImage(file='./static/paste.gif')
        self.undo_icon = PhotoImage(file='./static/undo.gif')
        self.redo_icon = PhotoImage(file='./static/redo.gif')
        self.find_icon = PhotoImage(file='./static/find_text.gif')
        self.about_icon = PhotoImage(file='./static/about.gif')

        menubar = Menu(root)
        filemenu = Menu(menubar,tearoff=0)
        filemenu.add_command(label='New',command=self.new_file,image=self.new_file_icon,accelerator='Ctrl+N',compound='left')
        filemenu.add_command(label='Open',command=self.open_file,image=self.open_file_icon,accelerator='Ctrl+O',compound='left')
        filemenu.add_command(label='Save',command=self.save_file,image=self.save_file_icon,accelerator='Ctrl+S',compound='left')
        filemenu.add_command(label='Save As',command=self.save_file_as,accelerator='Ctrl+Shift+S')
        # Add line between Save and Exit
        filemenu.add_separator()
        filemenu.add_command(label='Exit',accelerator='Alt+F4',compound='left')
        menubar.add_cascade(label='File',menu=filemenu)
        root.config(menu=menubar)

        editmenu = Menu(menubar,tearoff=0)
        editmenu.add_command(label='Undo',command=self.undo_change,image=self.undo_icon,accelerator='Ctrl+Z',compound='left')
        editmenu.add_command(label='Redo',command=self.redo_change,image=self.redo_icon,accelerator='Ctrl+Y',compound='left')
        editmenu.add_separator()
        editmenu.add_command(label='Cut',command=self.cut_selection,image=self.cut_icon,accelerator='Ctrl+X',compound='left')
        editmenu.add_command(label='Copy',command=self.copy_selection,image=self.copy_icon,accelerator='Ctrl+C',compound='left')
        editmenu.add_command(label='Paste',command=self.paste_selection,image=self.paste_icon,accelerator='Ctrl+V',compound='left')
        editmenu.add_command(label='Delete',command=self.delete_selection,accelerator='Del',compound='left')
        editmenu.add_separator()
        editmenu.add_command(label='Select All',command=self.select_all_text,accelerator='Ctrl+A',compound='left')
        menubar.add_cascade(label='Edit',menu=editmenu)
            
        toolmenu = Menu(menubar,tearoff=0)
        toolmenu.add_command(label='Find',command=self.find_text,image=self.find_icon,accelerator='Ctrl+F',compound='left')
        toolmenu.add_separator()
        themes_menu = Menu(toolmenu,bg='orange',tearoff=0)
        toolmenu.add_cascade(label='Themes',menu=themes_menu)

        choice.set('Default')
        for keys in color_schemes:
            themes_menu.add_radiobutton(label=keys,variable=choice,command=self.change_theme)
            themes_menu.add_separator()

        toolmenu.add_command(label='Word Count',command=self.count_text)
        toolmenu.add_separator()
        toolmenu.add_checkbutton(label='Status Bar',variable=stat_bar,command=self.stat_text)
        menubar.add_cascade(label='Tools',menu=toolmenu)

        infomenu = Menu(menubar,tearoff=0)
        infomenu.add_command(label='About App',command=self.about_app,image=self.about_icon,
                             accelerator='F2',compound="left")
        infomenu.add_command(label='About Developer',command=self.about_developer)
        menubar.add_cascade(label='Help',menu=infomenu)
        # root.config(menu=menubar)
        
        #======= Icons functionality ==================
        icons = ['new_file','open_file', 'save', 'cut', 'copy', 'paste',
                'undo', 'redo', 'find_text']
        cmd = [self.new_file,self.open_file,self.save_file,self.cut_selection,
               self.copy_selection,self.paste_selection,self.undo_change,
               self.redo_change,self.find_text]
        for i, icon in enumerate(icons):
            tool_icon = PhotoImage(file='./static/{}.gif'.format(icon))
            tool_bar = Button(self.shortcut_bar, image=tool_icon, command=cmd[i])
            tool_bar.image = tool_icon
            tool_bar.pack(side='left',padx=5,pady=5)
        #========= Scrollbar ==================
        scroll = Scrollbar(self.text_area)
        scroll.pack(side=RIGHT,fill=Y)
        scroll.config(command=self.text_area.yview)
        self.text_area.config(yscrollcommand=scroll.set)
        
    def exit_editor(self):
        global _file
        if _file == None:
            if self.text_area.compare("end-1c", "==", "1.0"):
                root.destroy()
            else:
                confirm_to_quit = messagebox.askyesnocancel("Quit?", "Really quit?\nYou have unsaved note!")
                if confirm_to_quit:
                    # save then quit
                    the_note = asksaveasfilename(initialfile='Untitled.txt',
                        defaultextension='.txt',filetypes=[('Text Documents','*.txt')])
                    if the_note == '':
                        pass
                    else:
                        note_taken = open(the_note,'w')
                        note_taken.write(self.text_area.get(1.0, "end-1c"))
                        note_taken.close()
                        root.destroy()
                elif confirm_to_quit == False:
                    # don't save, just quit
                    root.destroy()
        else:
            with open(_file) as fp:
                previous_note_content = fp.read()
                fp.close()
            current_note_content = self.text_area.get("1.0", "end-1c")
            if previous_note_content == current_note_content:
                root.destroy()
            else:
                confirm_to_quit = messagebox.askyesnocancel("Quit?", "Really quit?\nYou have made unsaved changes to your note!")
                if confirm_to_quit:
                    # save then quit
                    note_taken = open(_file,'w')
                    note_taken.write(self.text_area.get(1.0, "end-1c"))
                    note_taken.close()
                    root.destroy()
                elif confirm_to_quit == False:
                    # don't save, just quit
                    root.destroy()
            
    def new_file(self, event=None):
        global _file
        if _file == None:
            if self.text_area.compare("end-1c", "==", "1.0"):
                root.title('Untitled  |  Take Note')
                self.text_area.delete(1.0, END)
            else:
                confirm_to_save = messagebox.askyesnocancel('Message',"You haven't saved your note. Do you want to save your note?")
                if confirm_to_save:
                    the_note = asksaveasfilename(initialfile='Untitled.txt',
                        defaultextension='.txt',filetypes=[('Text Documents','*.txt')])
                    if the_note == '':
                        pass
                    else:
                        note_taken = open(the_note,'w')
                        note_taken.write(self.text_area.get(1.0, "end-1c"))
                        note_taken.close()
                        root.title('Untitled  |  Take Note')
                        self.text_area.delete(1.0, END)
                elif confirm_to_save == False:
                    root.title('Untitled  |  Take Note')
                    self.text_area.delete(1.0, END)
        else:
            with open(_file) as fp:
                previous_note_content = fp.read()
                fp.close()
            current_note_content = self.text_area.get("1.0", "end-1c")
            if previous_note_content == current_note_content:
                root.title('Untitled  |  Take Note')
                self.text_area.delete(1.0, END)
                _file = None
            else:
                confirm_to_save = messagebox.askyesnocancel('Message',"You have made changes to your note. Do you want to save the changes?")
                if confirm_to_save:
                    # save the current note
                    note_taken = open(_file,'w')
                    note_taken.write(self.text_area.get(1.0, "end-1c"))
                    note_taken.close()
                    # now open new note
                    root.title('Untitled  |  Take Note')
                    self.text_area.delete(1.0, END)
                    _file = None
                elif confirm_to_save == False:
                    root.title('Untitled  |  Take Note')
                    self.text_area.delete(1.0, END)
                    _file = None
                  
    def open_file(self, event=None):
        global _file
        if _file == None:
            if self.text_area.compare("end-1c", "==", "1.0"):
                _file = askopenfilename(defaultextension='.txt',
                    filetypes=[('Text Documents','*.txt')])
                if _file == "":
                    _file = None
                else:
                    # Open text file and change note title
                    file_title = os.path.basename(_file)[:-4] + '  |  Take Note'
                    root.title(file_title)
                    self.text_area.delete(1.0, END)
                    with open(_file) as fp:
                        contents = fp.read()
                    self.text_area.insert(1.0, contents)
                    fp.close()
            else:
                confirm_to_save = messagebox.askyesnocancel('Message',"You haven't saved your note. Do you want to save your note?")
                if confirm_to_save:
                    the_note = asksaveasfilename(initialfile='Untitled.txt',
                        defaultextension='.txt',filetypes=[('Text Documents','*.txt')])
                    if the_note == '':
                        pass
                    else:
                        # save the current note
                        _file = the_note
                        note_taken = open(the_note,'w')
                        note_taken.write(self.text_area.get(1.0, "end-1c"))
                        note_taken.close()
                        file_title = os.path.basename(_file)[:-4] + '  |  Take Note'
                        root.title(file_title)
                        # now open existing note
                        the_note = askopenfilename(defaultextension='.txt',
                            filetypes=[('Text Documents','*.txt')])
                        if the_note == "":
                            pass
                        else:
                            # Open text file and change note title
                            _file = the_note
                            file_title = os.path.basename(_file)[:-4] + '  |  Take Note'
                            root.title(file_title)
                            self.text_area.delete(1.0, "end-1c")
                            with open(_file) as fp:
                                contents = fp.read()
                            self.text_area.insert(1.0, contents)
                            fp.close()
                elif confirm_to_save == False:
                    _file = askopenfilename(defaultextension='.txt',
                        filetypes=[('Text Documents','*.txt')])
                    if _file == "":
                        _file = None
                    else:
                        # Open text file and change note title
                        file_title = os.path.basename(_file)[:-4] + '  |  Take Note'
                        root.title(file_title)
                        self.text_area.delete(1.0, END)
                        with open(_file) as fp:
                            contents = fp.read()
                        self.text_area.insert(1.0, contents)
                        fp.close()
        else:
            with open(_file) as fp:
                previous_note_content = fp.read()
                fp.close()
            current_note_content = self.text_area.get("1.0", "end-1c")
            if previous_note_content == current_note_content:
                _file = askopenfilename(defaultextension='.txt',
                    filetypes=[('Text Documents','*.txt')])
                if _file == "":
                    _file = None
                else:
                    # Open text file and change note title
                    file_title = os.path.basename(_file)[:-4] + '  |  Take Note'
                    root.title(file_title)
                    self.text_area.delete(1.0, END)
                    with open(_file) as fp:
                        contents = fp.read()
                    self.text_area.insert(1.0, contents)
                    fp.close()
            else:
                confirm_to_save = messagebox.askyesnocancel('Message',"You haven't saved your note. Do you want to save your note?")
                if confirm_to_save:
                    the_note = asksaveasfilename(initialfile='Untitled.txt',
                        defaultextension='.txt',filetypes=[('Text Documents','*.txt')])
                    if the_note == '':
                        pass
                    else:
                        # save the current note
                        _file = the_note
                        note_taken = open(the_note,'w')
                        note_taken.write(self.text_area.get(1.0, "end-1c"))
                        note_taken.close()
                        file_title = os.path.basename(_file)[:-4] + '  |  Take Note'
                        root.title(file_title)
                        # now open existing note
                        the_note = askopenfilename(defaultextension='.txt',
                            filetypes=[('Text Documents','*.txt')])
                        if the_note == "":
                            pass
                        else:
                            # Open text file and change note title
                            _file = the_note
                            file_title = os.path.basename(_file)[:-4] + '  |  Take Note'
                            root.title(file_title)
                            self.text_area.delete(1.0, "end-1c")
                            with open(_file) as fp:
                                contents = fp.read()
                            self.text_area.insert(1.0, contents)
                            fp.close()
                elif confirm_to_save == False:
                    _file = askopenfilename(defaultextension='.txt',
                        filetypes=[('Text Documents','*.txt')])
                    if _file == "":
                        _file = None
                    else:
                        # Open text file and change note title
                        file_title = os.path.basename(_file)[:-4] + '  |  Take Note'
                        root.title(file_title)
                        self.text_area.delete(1.0, END)
                        with open(_file) as fp:
                            contents = fp.read()
                        self.text_area.insert(1.0, contents)
                        fp.close()
        
    def save_file_as(self):
        global _file
        # Know if current note have been saved before
        check_if_file_exist = asksaveasfilename(initialfile='Untitled.txt',
            defaultextension='.txt',filetypes=[('Text Documents','*.txt')])
        if check_if_file_exist == '':
            _file = None
            return
        _file = check_if_file_exist
        note_taken = open(_file,'w')
        note_taken.write(self.text_area.get(1.0, "end-1c"))
        note_taken.close()
        file_title = os.path.basename(_file)[:-4] + '  |  Take Note'
        root.title(file_title)
            
    def save_file(self, event=None):
        global _file
        # Know if current note have been saved before
        if _file == None:
            check_if_file_exist = asksaveasfilename(initialfile='Untitled.txt',
                defaultextension='.txt',filetypes=[('Text Documents','*.txt')])
            if check_if_file_exist == '':
                _file = None
            else:
                _file = check_if_file_exist
                note_taken = open(_file,'w')
                note_taken.write(self.text_area.get(1.0, "end-1c"))
                note_taken.close()
                file_title = os.path.basename(_file)[:-4] + '  |  Take Note'
                root.title(file_title)
        # Else, the file already exist so save on the saved file
        else:
            note_taken = open(_file,'w')
            note_taken.write(self.text_area.get(1.0, "end-1c"))
            note_taken.close()
            
    def undo_change(self):
        self.text_area.event_generate('<<Undo>>')

    def redo_change(self):
        self.text_area.event_generate('<<Redo>>')
            
    def cut_selection(self):
        self.text_area.event_generate('<<Cut>>')
            
    def copy_selection(self):
        self.text_area.event_generate('<<Copy>>')
            
    def paste_selection(self):
        self.text_area.event_generate('<<Paste>>')
            
    def delete_selection(self):
        self.text_area.delete(SEL_FIRST, SEL_LAST)
    
    def search_output(self, needle, if_ignore_case, text_area,
                    search_toplevel, search_box):
        self.text_area.tag_remove('match', '1.0', END)
        matches_found = 0
        if needle:
            start_pos = '1.0'
            while True:
                start_pos = self.text_area.search(needle, start_pos,
                                                    nocase=if_ignore_case, stopindex=END)
                if not start_pos:
                    break
                end_pos = '{}+{}c'.format(start_pos, len(needle))
                self.text_area.tag_add('match', start_pos, end_pos)
                matches_found += 1
                start_pos = end_pos
            self.text_area.tag_config(
                'match', foreground='red', background='yellow')
        search_box.focus_set()
        search_toplevel.title('{} matches found'.format(matches_found))

        def close_search_window():
            self.text_area.tag_remove('match', '1.0', END)
            search_toplevel.destroy()
        search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
        return "break"

    def find_text(self, event=None):
        search_toplevel = Toplevel()
        search_toplevel.title('Find Text')
        search_toplevel.transient()
        search_toplevel.resizable(0, 0)
        Label(search_toplevel, text="Find All:",font='candara 12').grid(row=0, column=0, sticky='e')
        search_entry_widget = Entry(
            search_toplevel, width=25,font='candara 12')
        search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
        search_entry_widget.focus_set()
        ignore_case_value = IntVar()
        Checkbutton(search_toplevel,font='candara 12', text='Ignore Case', variable=ignore_case_value).grid(
            row=1, column=1, sticky='e', padx=2, pady=2)
        Button(search_toplevel,font='candara 12', text="Find All", underline=0,
            command=lambda: self.search_output(
                search_entry_widget.get(), ignore_case_value.get(),
                self.text_area, search_toplevel, search_entry_widget)
            ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)
            
    def change_theme(self):
        selected_theme = choice.get()
        fg_bg_colors = color_schemes.get(selected_theme)
        split_them = fg_bg_colors.split('-')
        fg_color, bg_color, insertbg = split_them[0], split_them[1],split_them[2]
        self.text_area.config(background=bg_color,fg=fg_color,insertbackground=insertbg)
            
    def count_text(self):
        text = self.text_area.get(1.0, END)
        messagebox.showinfo('Word Count',f'This note has {len(text.split())} words.')
            
    def stat_text(self):
        status = stat_bar.get()
        if status:
            self.status_bar.pack(expand='no', fill=None, side='right', anchor='se')
        else:
            self.status_bar.pack_forget()
            
    def about_app(self, event=None):
        newWindow = Toplevel(root)
        newWindow.title('About App')
        newWindow.config(bg='#222')
        newWindow.geometry('300x80')
        Label(newWindow,text='The app is a basic text editor.',fg='#fff',bg='#222',font='montserrat 14').pack(pady=(20,5))

    def about_developer(self):
        newWindow = Toplevel(root)
        newWindow.title('About Developer')
        newWindow.config(bg='#222')
        newWindow.geometry('580x170')
        Label(newWindow,text='I am an experienced python desktop\n\
            application and web programmer!\
            \nFind more of my works at:',fg='#fff',bg='#222',font='montserrat 14').pack(pady=(20,5))
        the_github = Entry(newWindow,width=30, justify='center',font='montserrat 14')
        the_github.insert(0, "https://github.com/TomiwaJoseph")
        the_github.configure(fg='#fff',state="readonly",readonlybackground="#222")
        the_github.place(x=85,y=110)

    def select_all_text(self, event=None):
        self.text_area.tag_add('sel', 1.0, END)
            
    def update_note_stats(self, event=None):
        row, col = self.text_area.index(INSERT).split('.')
        line_num, col_num = str(int(row)), str(int(col) + 1)  # col starts at 0
        infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
        self.status_bar.config(text=infotext)


if __name__ == "__main__":
    app = App()
    mainloop()
