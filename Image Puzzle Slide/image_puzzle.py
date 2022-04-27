import random 
from tkinter import *
from tkinter import messagebox as tkMessageBox 
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename

root = Tk
MAX_BOARD_SIZE = 550
image_selected = r''
board_grid_input = 3


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
        self._frame.place(x=0,y=0,relheight=1,relwidth=1)
        
        
class StartPage(Frame):
    ''' Displays the startpage of the application which consist of a puzzle image, a `Image Puzle`\
        label and a button that leads to the settings page'''
    def __init__(self,root):
        Frame.__init__(self,root)
        Frame.configure(self,bg='#143d59')
        self.root = root
        self.root.title('Start Page')
        self.root.resizable(0,0)
        #======= Background Image =====================
        self.bg = Image.open('./static/landing_page.png')
        self.bg = self.bg.resize((485,485), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.picture_frame = Frame(self.master,width=500,height=500,relief='ridge',bg='#143d59',bd=5)
        self.picture_frame.place(anchor=CENTER,relx=0.35,rely=0.5)
        Label(self.picture_frame,image=self.bg).place(x=0,y=0)
        #======= Title =====================
        Label(self.master,text="Image Puzzle",font='montserrat 40',fg='#fff',
              bg='#143d59').place(relx=0.7,rely=0.46,anchor=CENTER)
        #=========== Buttons ==================
        self.setting = Button(self.master,text='Start',font='montserrat 16',bd=2,width=24,
            fg='#143d59',bg='#f4b41a',command=lambda:self.master.switch_frame(SettingsPage))
        self.setting.place(relx=0.7,rely=0.55,anchor=CENTER)


class SettingsPage(Frame):
    ''' Displays the settings page of the application which allows the player to select an `image file`\
        and the `dimension` of the puzzle grid'''
    def __init__(self,root):
        Frame.__init__(self,root)
        Frame.configure(self,bg='#143d59')
        self.root = root
        self.root.title('Settings Page')
        self.root.resizable(0,0)
        #========= Info about Game ==============
        self.menubar = Menu()
        self.filemenu = Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='Help',command=self.about_game)
        self.menubar.add_cascade(label='About Developer',command=self.about_developer)
        self.root.config(menu=self.menubar)
        # =========== UI ===============
        self.settings_frame = Frame(self.master,width=600,height=230,relief='ridge',bg='#143d59',bd=5)
        self.settings_frame.place(anchor=CENTER,relx=0.5,rely=0.5)
        self.dimension = Entry(self.settings_frame,font='montserrat 18',bg='#dadada',
            justify=CENTER,width=20,fg='#222')
        self.dimension.insert(0, 'Enter 3 to get a 3x3 grid')
        self.dimension.place(anchor=CENTER,relx=0.5,rely=0.18)
        self.dimension.bind('<FocusIn>', self.entry_click)
        self.dimension.bind('<FocusOut>', self.out_click)
        self.input_status = Label(self.master,text='Incorrect input or no image selected 🤨',
            fg='#f00',bg='#fff',font='montserrat 14')
        #=========== Buttons ==================
        self.select_image = Button(self.settings_frame,text='Select Image',font='montserrat 16',bd=2,width=24,
            fg='#143d59',bg='#f4b41a',command=self.openfile_name)
        self.select_image.place(relx=0.5,rely=0.46,anchor=CENTER)
        self.start_game = Button(self.settings_frame,text='Start',font='montserrat 16',bd=2,width=24,
            fg='#143d59',bg='#f4b41a',command=self.verify_inputs)
        self.start_game.place(relx=0.5,rely=0.75,anchor=CENTER)
        
    def about_game(self):
        newWindow = Toplevel(self.root)
        newWindow.attributes('-topmost', 'true')
        newWindow.title('About Game')
        newWindow.config(bg='#222')
        newWindow.geometry('530x410')
        newWindow.resizable(0,0)
        the_text = '''\nWelcome player!\n\nSETTINGS\nEnter the number of tiles per row and column\nEg. Enter 3 to get a 3x3 image tiles\nEg. Enter 4 to get a 4x4 image tiles\nSelect your image and press start
        \nGAMEPLAY\nArrange tiles of your selected picture\nEnjoy😎!
        '''
        Label(newWindow,text=the_text,fg='#fff',bg='#222',
              font='montserrat 14').pack(pady=(20,5))
    
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
    
    def openfile_name(self):
        global image_selected
        filename = askopenfilename(filetypes=[('image files', '*.png *.jpg')])
        image_selected = filename
    
    def entry_click(self, event):
        if self.dimension.get() == 'Enter 3 to get a 3x3 grid':
            self.dimension.delete(0, END)
    
    def out_click(self, event):
        if self.dimension.get() == '':
            self.dimension.insert(0, 'Enter 3 to get a 3x3 grid')
                
    def verify_inputs(self):
        global image_selected, board_grid_input
        try:
            integer_test = int(self.dimension.get())
            if not image_selected:
                raise ValueError
            
            board_grid_input = integer_test
            self.master.switch_frame(MainPage)
        except ValueError:
            self.input_status.place(relx=0.5,rely=0.3,anchor=CENTER)
        
        
class MainPage(Frame):
    ''' Displays the main page of the application which allows the player to `arrange` the selected image file\
        and `enjoy` the game'''
    def __init__(self,root):
        Frame.__init__(self,root)
        Frame.configure(self,bg='#143d59')
        self.root = root
        self.root.title('Image Puzzle')
        self.root.resizable(0,0)
        #========= Info about Game ==============
        self.menubar = Menu()
        self.filemenu = Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='About Game',command=self.about_game)
        self.root.config(menu=self.menubar)
        #======== Back Button ============
        self.the_image = PhotoImage(file='./static/back_arrow.png')
        self.back = self.the_image.subsample(1,1)
        Button(image=self.back,bg="#fff",width=50,command=self.go_back_to_settings).place(x=60,y=20)
        # =========== Game Area ================
        self.picture_frame = Frame(self.master,width=600,height=600,relief='ridge',bg='#143d59',bd=5)
        self.picture_frame.place(anchor=CENTER,relx=0.5,rely=0.46)
        self.show_or_hide = Button(text='Show Arranged Image',font='montserrat 14',width=25,
            fg='#143d59',bg='#f4b41a',command=self.help)
        self.show_or_hide.place(anchor=CENTER,relx=0.5,rely=0.93)
        self.board_grid = board_grid_input
        self.load_image(image_selected) 
        self.steps = 0 
        self.create_widgets() 
        self.create_events() 
        self.create_board() 
        self.show()
        
    def about_game(self):
        newWindow = Toplevel(self.root)
        newWindow.attributes('-topmost', 'true')
        newWindow.title('About Game')
        newWindow.config(bg='#222')
        newWindow.geometry('430x260')
        newWindow.resizable(0,0)
        the_text = '''\nWelcome player!\n\nGAMEPLAY\nUse UP⬆, DOWN⬇,\nLEFT⬅ and RIGHT➡ to move tiles \nEnjoy😎!'''
        Label(newWindow,text=the_text,fg='#fff',bg='#222',
              font='montserrat 14').pack(pady=(20,5))
        
    def load_image(self, image): 
        image = Image.open(image) 
        board_size = min(image.size) 
        if image.size[0] != image.size[1]: 
            image = image.crop((0, 0, board_size, board_size)) 
        if board_size > MAX_BOARD_SIZE: 
            board_size = MAX_BOARD_SIZE 
            image = image.resize((board_size, board_size), Image.ANTIALIAS) 
        self.image = image 
        self.board_size = board_size 
        self.piece_size = self.board_size / self.board_grid 
        
    def create_widgets(self): 
        args = dict(width=self.board_size, height=self.board_size) 
        self.canvas = Canvas(self.picture_frame, **args) 
        # self.canvas.grid()
        self.canvas.place(anchor=CENTER,relx=0.5,rely=0.5)
        
    def create_events(self): 
        self.canvas.bind_all('<KeyPress-Up>', self.slide) 
        self.canvas.bind_all('<KeyPress-Down>', self.slide) 
        self.canvas.bind_all('<KeyPress-Left>', self.slide) 
        self.canvas.bind_all('<KeyPress-Right>', self.slide) 
        
    def switch_btn_text(self):
        if self.show_or_hide['text'] == 'Show Arranged Image':
            self.show_or_hide.config(text='Hide Arranged Image')
        else:
            self.show_or_hide.config(text='Show Arranged Image')
        
    def help(self):
        self.switch_btn_text()
        if getattr(self, '_img_help_id', None) is None:
            self._img_help = ImageTk.PhotoImage(self.image) 
            self._img_help_id = self.canvas.create_image(0, 0, image=self._img_help, anchor=NW) 
        else: 
            state = self.canvas.itemcget(self._img_help_id, 'state') 
            state = 'hidden' if state == '' else '' 
            self.canvas.itemconfigure(self._img_help_id, state=state) 
            
    def slide(self, event):
        pieces = self.get_pieces_around()
        if event.keysym in ('Up', 'k') and pieces['bottom']: 
            self._slide(pieces['bottom'], pieces['center'], (0, -self.piece_size)) 
        if event.keysym in ('Down', 'j') and pieces['top']: 
            self._slide(pieces['top'], pieces['center'], (0, self.piece_size)) 
        if event.keysym in ('Left', 'h') and pieces['right']: 
            self._slide(pieces['right'], pieces['center'], (-self.piece_size, 0)) 
        if event.keysym in ('Right', 'l') and pieces['left']: 
            self._slide(pieces['left'], pieces['center'], (self.piece_size, 0)) 
        self.check_status() 
        
    def _slide(self, from_, to, coord):
        self.canvas.move(from_['id'], *coord)
        to['pos_a'], from_['pos_a'] = from_['pos_a'], to['pos_a'] 
        self.steps += 1 
        
    def get_pieces_around(self):
        pieces = {
            'center': None, 
            'right' : None, 
            'left' : None, 
            'top' : None, 
            'bottom': None
            } 
        for piece in self.board: 
            if not piece['visible']: 
                pieces['center'] = piece 
                break 
        x0, y0 = pieces['center']['pos_a'] 
        for piece in self.board: 
            x1, y1 = piece['pos_a'] 
            if y0 == y1 and x1 == x0 + 1: pieces['right'] = piece 
            if y0 == y1 and x1 == x0 - 1: pieces['left'] = piece 
            if x0 == x1 and y1 == y0 - 1: pieces['top'] = piece 
            if x0 == x1 and y1 == y0 + 1: pieces['bottom'] = piece
        return pieces 
    
    def create_board(self): 
        self.board = [] 
        for x in range(self.board_grid): 
            for y in range(self.board_grid): 
                x0 = x * self.piece_size 
                y0 = y * self.piece_size 
                x1 = x0 + self.piece_size 
                y1 = y0 + self.piece_size 
                image = ImageTk.PhotoImage( self.image.crop((x0, y0, x1, y1))) 
                piece = {
                    'id' : None, 'image' : image, 'pos_o' : (x, y), 'pos_a' : None, 'visible': True
                    }
                self.board.append(piece) 
        self.board[-1]['visible'] = False 
        
    def check_status(self): 
        for piece in self.board: 
            if piece['pos_a'] != piece['pos_o']: 
                return 
        title = 'Congratulations!' 
        message = f'You solved it in {self.steps} moves!'
        tkMessageBox.showinfo(title, message) 
        
    def show(self): 
        random.shuffle(self.board) 
        index = 0 
        for x in range(self.board_grid): 
            for y in range(self.board_grid): 
                self.board[index]['pos_a'] = (x, y) 
                if self.board[index]['visible']: 
                    x1 = x * self.piece_size 
                    y1 = y * self.piece_size 
                    image = self.board[index]['image'] 
                    id = self.canvas.create_image( x1, y1, image=image, anchor=NW) 
                    self.board[index]['id'] = id 
                index += 1 
        
    def go_back_to_settings(self):
        global image_selected, board_grid_input
        image_selected = ''
        board_grid_input = 0
        self.master.switch_frame(SettingsPage)
                           
        
if __name__ == '__main__':
    app = Switch()
    # app.state('zoomed') # Fullscreen with minimize and maximize button
    app.attributes('-fullscreen', True) # Fullscreen without minimize and maximize button
    app.mainloop()