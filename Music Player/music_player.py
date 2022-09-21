from tkinter import *
from tkinter.filedialog import *
from pygame import mixer
from io import BytesIO
import stagger
import pygame
from mutagen.mp3 import MP3
from tkinter import ttk
import _thread
import time
from PIL import ImageTk, Image
from threading import Timer
from random import shuffle, choice
from threading import Thread

root = Tk
pygame.init()


class Switch(root):
    def __init__(self):
        root.__init__(self)
        self._frame = None
        self.switch_frame(MusicPage)

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
        self.root.geometry('630x350')
        self.root.resizable(0, 0)
        self.root.iconbitmap(r'./static/icon.ico')
        # ======= UI =====================
        self.bg = Image.open('./static/icon.ico')
        self.bg = self.bg.resize((55, 55), Image.ANTIALIAS)
        self.the_logo = ImageTk.PhotoImage(self.bg)
        self.first_card = Frame(width=60, height=60,
                                relief='ridge', bg='#101820', bd=2)
        self.first_card.place(relx=0.5, rely=0.36, anchor=CENTER)
        Label(self.first_card, image=self.the_logo).place(x=0, y=0)
        # ======= Title =====================
        Label(self.master, text="MusicPlay", font='montserrat 30', fg='#f2aa4c',
              bg='#101820', justify='left').place(relx=0.5, rely=0.56, anchor=CENTER)

        # ======= SHOW STARTPAGE FOR 3 ONLY SECONDS =====================
        r = Timer(3.0, lambda: self.master.switch_frame(MusicPage))
        r.start()


class MusicPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.configure(self, bg='#101820')
        self.root = root
        self.root.geometry('630x350')
        self.root.resizable(0, 0)
        self.root.iconbitmap(r'./static/icon.ico')
        # ========= MENUBAR ==============
        self.create_menubar()
        # ============ USER INTERFACE ====================
        self.create_ui()
        # ============ VARIABLES ====================
        self.original_playlist = {
            #    0: 'C:/Users/dretech/Music/1/v09BloodFlagInFdismantlingThe.ogg',
            #    1: 'C:/Users/dretech/Music/1/for-player.wav',
            #    2: "C:/Users/dretech/Music/1/04 Don't You Remember.mp3",
            #    3: 'C:/Users/dretech/Music/1/for_player.wav',

            0: 'C:/Users/dretech/Music/1/for_player.wav',
            1: 'C:/Users/dretech/Music/1/04 - You Have Been Loved - (Musicfire.in).mp3',
            2: 'C:/Users/dretech/Music/1/for-player.wav',
            3: 'C:/Users/dretech/Music/1/bbbsecond-song.mp3',
            4: "C:/Users/dretech/Music/1/04 Don't You Remember.mp3",
            5: 'C:/Users/dretech/Music/1/v09BloodFlagInFdismantlingThe.ogg',
        }
        self.shuffled_playlist = []
        self.playlist_in_use = self.original_playlist
        self.current_song_index_in_playlist = 0
        self.paused = False
        self.music_details = []
        self.mute = False
        self.playing = False
        self.to_break = False
        self.current_time = 0
        self.current_song = ''
        self.song = ''
        self.single_song_duration = 0
        self.repeat_one = False
        self.repeat_all = False
        self.shuffle = False
        self.auto_next_button_press = False
        self.paused_before_next = False
        self.last_dict_key = 0
        self.pas = False
        # ============ KeyBinds ====================
        self.create_keybinds()
        # ============ Utility Frames ====================
        self.back_image = PhotoImage(file='./static/back_arrow.png')
        self.back = self.back_image.subsample(1, 1)
        self.playlist_frame = Frame(
            width=630, height=350, relief='ridge', bg='#101820')
        self.about_app_frame = Frame(
            width=630, height=350, relief='ridge', bg='#101820')
        self.about_developer_frame = Frame(
            width=630, height=350, relief='ridge', bg='#101820')
        self.quitting_frame = Frame(
            width=630, height=350, relief='ridge', bg='#101820')

    def create_keybinds(self):
        ''' Create shortcuts eg. CTRL + Z, CTRL + X '''
        self.root.bind('<Control-A>', self.add_songs_to_playlist)
        self.root.bind('<Control-a>', self.add_songs_to_playlist)
        self.root.bind('<Control-Q>', self.show_quit_frame)
        self.root.bind('<Control-q>', self.show_quit_frame)
        self.root.bind('<Control-L>', self.view_playlist)
        self.root.bind('<Control-l>', self.view_playlist)
        self.root.bind('<space>', lambda t: self.play_song(
            'button press') if self.original_playlist else print('Empty playlist'))

    def create_ui(self):
        ''' Create the user interface which include buttons and stuff '''
        # ============ Album Art ====================
        self.cover = Image.open('./static/icon.ico')
        self.cover = self.cover.resize((170, 170), Image.ANTIALIAS)
        self.cover = ImageTk.PhotoImage(self.cover)
        self.album_art = Label(
            image=self.cover, relief='ridge', width=180, height=180)
        self.album_art.place(relx=0.312, rely=0.35, anchor=CENTER)
        # ============ Progress Bar ====================
        # self.progress = ttk.Progressbar(length=420)
        # self.progress.place(relx=0.5,rely=0.72,anchor=CENTER)
        self.progress = ttk.Scale(from_=0, to=100, orient=HORIZONTAL, length=430,
                                  command=self.forwards_or_backwards)
        self.progress.place(relx=0.5, rely=0.72, anchor=CENTER)
        self.progress_start = Label(
            font='candara 14', fg='#f2aa4c', bg='#101820', text='5:00:00')
        self.progress_start.place(relx=0.09, rely=0.72, anchor=CENTER)
        self.progress_end = Label(
            font='candara 14', fg='#f2aa4c', bg='#101820', text='5:00:00')
        self.progress_end.place(relx=0.91, rely=0.72, anchor=CENTER)
        self.current_display = Label(fg='#101820', bg='#f2aa4c', font='candara 14', text="Welcome to Tommy's Music Player",
                                     relief='ridge', width=57, height=1)
        self.current_display.place(relx=0.5, rely=0.85, anchor=CENTER)
        # ============ Prev Button ====================
        self.bg = Image.open('./static/_previous.png')
        self.bg = self.bg.resize((50, 50), Image.ANTIALIAS)
        self.prev_img = ImageTk.PhotoImage(self.bg)  # ,bg='#101820'
        self.previous_btn = Button(
            image=self.prev_img, bd=0, command=self.previous_song, bg='#101820')
        self.previous_btn.place(relx=0.55, rely=0.23, anchor=CENTER)
        # ============ Play Button ====================
        self.bg = Image.open('./static/_play.png')
        self.bg = self.bg.resize((50, 50), Image.ANTIALIAS)
        self.play_img = ImageTk.PhotoImage(self.bg)
        self.bg = Image.open('./static/_pause.png')
        self.bg = self.bg.resize((50, 50), Image.ANTIALIAS)
        self.pause_img = ImageTk.PhotoImage(self.bg)
        self.play_btn = Button(image=self.play_img, bd=0, command=lambda: self.play_song(
            'button press'), bg='#101820')
        self.play_btn.place(relx=0.675, rely=0.23, anchor=CENTER)
        # ============ Next Button ====================
        self.bg = Image.open('./static/_next.png')
        self.bg = self.bg.resize((50, 50), Image.ANTIALIAS)
        self.next_img = ImageTk.PhotoImage(self.bg)
        self.next_btn = Button(image=self.next_img, bd=0, command=lambda: self.next_song(
            'from button'), bg='#101820')
        self.next_btn.place(relx=0.8, rely=0.23, anchor=CENTER)
        # ============ View Playlist Button ====================
        self.bg = Image.open('./static/_playlist.png')
        self.bg = self.bg.resize((20, 20), Image.ANTIALIAS)
        self.view_playlist_img = ImageTk.PhotoImage(self.bg)
        self.repeat_all_btn = Button(
            image=self.view_playlist_img, bd=0, command=self.view_playlist, bg='#101820')
        self.repeat_all_btn.place(relx=0.55, rely=0.41, anchor=CENTER)
        # ============ Repeat All Button ====================
        self.bg = Image.open('./static/_repeat_all_yes.png')
        self.bg = self.bg.resize((20, 20), Image.ANTIALIAS)
        self.repeat_all_yes_img = ImageTk.PhotoImage(self.bg)
        self.bg = Image.open('./static/_repeat_all_icon.png')
        self.bg = self.bg.resize((20, 20), Image.ANTIALIAS)
        self.repeat_all_img = ImageTk.PhotoImage(self.bg)
        self.repeat_all_btn = Button(
            image=self.repeat_all_img, bd=0, command=self.repeat_all_playlist, bg='#101820')
        self.repeat_all_btn.place(relx=0.64, rely=0.41, anchor=CENTER)
        # ============ Repeat One Button ====================
        self.bg = Image.open('./static/_repeat_one_yes.png')
        self.bg = self.bg.resize((20, 20), Image.ANTIALIAS)
        self.repeat_one_yes_img = ImageTk.PhotoImage(self.bg)
        self.bg = Image.open('./static/_repeat_one_icon.png')
        self.bg = self.bg.resize((20, 20), Image.ANTIALIAS)
        self.repeat_one_img = ImageTk.PhotoImage(self.bg)
        self.repeat_one_btn = Button(
            image=self.repeat_one_img, bd=0, command=self.repeat_current_song, bg='#101820')
        self.repeat_one_btn.place(relx=0.72, rely=0.41, anchor=CENTER)
        # ============ Shuffle Button ====================
        self.bg = Image.open('./static/_shuffle_yes.png')
        self.bg = self.bg.resize((20, 20), Image.ANTIALIAS)
        self.shuffle_yes_img = ImageTk.PhotoImage(self.bg)
        self.bg = Image.open('./static/_shuffle_icon.png')
        self.bg = self.bg.resize((20, 20), Image.ANTIALIAS)
        self.shuffle_img = ImageTk.PhotoImage(self.bg)
        self.shuffle_btn = Button(
            image=self.shuffle_img, bd=0, command=self.shuffle_playlist, bg='#101820')
        self.shuffle_btn.place(relx=0.8, rely=0.41, anchor=CENTER)
        # ============ Mute and Volume ====================
        self.bg = Image.open('./static/_mute_icon.png')
        self.bg = self.bg.resize((20, 20), Image.ANTIALIAS)
        self.mute_img = ImageTk.PhotoImage(self.bg)
        self.bg = Image.open('./static/_volume_icon.png')
        self.bg = self.bg.resize((20, 20), Image.ANTIALIAS)
        self.speaker_img = ImageTk.PhotoImage(self.bg)
        self.speaker_btn = Button(
            image=self.speaker_img, bd=0, command=self.mute_and_unmute_song, bg='#101820')
        self.speaker_btn.place(relx=0.55, rely=0.54, anchor=CENTER)
        style = ttk.Style(self.root)
        style.theme_use('clam')
        self.volume = ttk.Scale(from_=0, to=100, orient=HORIZONTAL, length=150,
                                command=self.set_volume)
        self.volume.set(30)
        self.volume.place(relx=0.711, rely=0.54, anchor=CENTER)

    def create_menubar(self):
        ''' Create the menubar where thing like File, About etc. reside '''
        self.bg = Image.open('./static/_add_icon.png')
        self.bg = self.bg.resize((12, 12), Image.ANTIALIAS)
        self.add_icon = ImageTk.PhotoImage(self.bg)

        self.bg = Image.open('./static/_exit_icon.png')
        self.bg = self.bg.resize((12, 12), Image.ANTIALIAS)
        self.exit_icon = ImageTk.PhotoImage(self.bg)

        self.bg = Image.open('./static/_playlist_icon.png')
        self.bg = self.bg.resize((12, 12), Image.ANTIALIAS)
        self.playlist_view_icon = ImageTk.PhotoImage(self.bg)

        self.bg = Image.open('./static/_play_icon.png')
        self.bg = self.bg.resize((12, 12), Image.ANTIALIAS)
        self.play_icon = ImageTk.PhotoImage(self.bg)

        self.bg = Image.open('./static/_previous_icon.png')
        self.bg = self.bg.resize((12, 12), Image.ANTIALIAS)
        self.prev_icon = ImageTk.PhotoImage(self.bg)

        self.bg = Image.open('./static/_next_icon.png')
        self.bg = self.bg.resize((12, 12), Image.ANTIALIAS)
        self.next_icon = ImageTk.PhotoImage(self.bg)

        self.bg = Image.open('./static/_repeat_all_icon.png')
        self.bg = self.bg.resize((15, 15), Image.ANTIALIAS)
        self.repeat_icon = ImageTk.PhotoImage(self.bg)

        self.bg = Image.open('./static/_repeat_one_icon.png')
        self.bg = self.bg.resize((15, 15), Image.ANTIALIAS)
        self.repeat_one_icon = ImageTk.PhotoImage(self.bg)

        self.bg = Image.open('./static/_shuffle_icon.png')
        self.bg = self.bg.resize((15, 15), Image.ANTIALIAS)
        self.shuffle_icon = ImageTk.PhotoImage(self.bg)

        self.bg = Image.open('./static/_about_icon.png')
        self.bg = self.bg.resize((15, 15), Image.ANTIALIAS)
        self.about_icon = ImageTk.PhotoImage(self.bg)

        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        self.mediamenu = Menu(self.menubar, tearoff=0)
        self.playbackmenu = Menu(self.menubar, tearoff=0)
        self.viewmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu = Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label='Media', menu=self.mediamenu)
        self.menubar.add_cascade(label='Playback', menu=self.playbackmenu)
        self.menubar.add_cascade(label='View', menu=self.viewmenu)
        self.menubar.add_cascade(label='Help', menu=self.helpmenu)

        self.mediamenu.add_command(label='Add Songs', image=self.add_icon,
                                   command=self.add_songs_to_playlist, accelerator='Ctrl+A', compound='left')
        self.mediamenu.add_command(label='Exit', image=self.exit_icon,
                                   command=self.show_quit_frame, accelerator='Ctrl+Q', compound='left')

        self.playbackmenu.add_command(label='Play', image=self.play_icon,
                                      command=lambda: self.play_song('button press'), compound='left')
        # self.playbackmenu.add_command(label='Stop',image=self.stop_icon,
        #     command=self.stop_song,compound='left')
        self.playbackmenu.add_command(label='Previous', image=self.prev_icon,
                                      command=self.previous_song, compound='left')
        self.playbackmenu.add_command(label='Next', image=self.next_icon,
                                      command=lambda: self.next_song('from button'), compound='left')
        self.playbackmenu.add_command(label='Repeat All', image=self.repeat_icon,
                                      command=self.repeat_all_playlist, compound='left')
        self.playbackmenu.add_command(label='Repeat One', image=self.repeat_one_icon,
                                      command=self.repeat_current_song, compound='left')
        self.playbackmenu.add_command(label='Shuffle', image=self.shuffle_icon,
                                      command=self.shuffle_playlist, compound='left')

        self.viewmenu.add_command(label='View Playlist', image=self.playlist_view_icon,
                                  command=self.view_playlist, accelerator='Ctrl+L', compound='left')

        self.helpmenu.add_command(label='About App', image=self.about_icon,
                                  command=self.about_app, compound='left')
        self.helpmenu.add_command(
            label='About Developer', command=self.about_developer, compound='left')

    def forwards_or_backwards(self, value):
        new_position = int(self.progress.get())
        self.current_time = new_position
        pygame.mixer.music.load(
            self.playlist_in_use[self.current_song_index_in_playlist])
        pygame.mixer.music.play(loops=0, start=new_position)

    def rerun_single_song_in_playlist(self):
        ''' Play current song again after it ends '''
        self.current_time = 0
        self.current_song_index_in_playlist = self.current_song_index_in_playlist
        self.to_break = True
        directory = self.original_playlist[self.current_song_index_in_playlist]
        mixer.music.load(directory)
        mixer.music.play()
        self.current_song = directory
        directory_split = directory.split('/')
        song_title = directory_split[-1][:-4]
        self.current_display['text'] = 'Playing:   ♫ ' + song_title + ' ♫'
        self.add_song(directory)
        self.show_progress(directory)

    def rerun_all_songs_in_playlist(self):
        ''' Replay all songs in the playlist once it ends '''
        self.current_time = 0
        self.current_song_index_in_playlist = 0
        self.to_break = True
        directory = self.original_playlist[self.current_song_index_in_playlist]
        mixer.music.load(directory)
        mixer.music.play()
        self.current_song = directory
        directory_split = directory.split('/')
        song_title = directory_split[-1][:-4]
        self.current_display['text'] = 'Playing:   ♫ ' + song_title + ' ♫'
        self.add_song(directory)
        self.show_progress(directory)

    def shuffle_playlist(self):
        ''' Randomize all songs in the playlist '''
        self.repeat_one = False
        self.repeat_all = False

        if self.shuffle:
            self.shuffle = False
            self.playlist_in_use = self.original_playlist
            self.shuffle_btn['image'] = self.shuffle_img
            shuffle_false_index = [k for k, v in self.original_playlist.items(
            ) if v == self.shuffled_playlist[self.current_song_index_in_playlist]][0]
            self.current_song_index_in_playlist = shuffle_false_index
        else:
            # if you press the shuffle button, shuffle the original playlist and use
            # a new playlist instead
            try:
                self.shuffled_playlist = [self.original_playlist.get(
                    i) for i in self.original_playlist.keys()]
                self.new_first_song = self.shuffled_playlist[self.current_song_index_in_playlist]
                del self.shuffled_playlist[self.current_song_index_in_playlist]
                shuffle(self.shuffled_playlist)
                self.shuffled_playlist.insert(0, self.new_first_song)
                self.playlist_in_use = self.shuffled_playlist
                self.current_song_index_in_playlist = 0
                self.shuffle = True
                self.shuffle_btn['image'] = self.shuffle_yes_img
                self.repeat_one_btn['image'] = self.repeat_one_img
                self.repeat_all_btn['image'] = self.repeat_all_img
            except IndexError:
                print('No songs to shuffle')

    def repeat_all_playlist(self):
        ''' Changes the image on the repeat all button to indicate on or off '''
        self.repeat_one = False
        self.shuffle = False
        if self.repeat_all:
            self.repeat_all = False
            self.repeat_all_btn['image'] = self.repeat_all_img
        else:
            self.repeat_all = True
            self.repeat_all_btn['image'] = self.repeat_all_yes_img
            self.repeat_one_btn['image'] = self.repeat_one_img
            self.shuffle_btn['image'] = self.shuffle_img

    def repeat_current_song(self):
        ''' Changes the image on the repeat one button to indicate on or off '''
        self.repeat_all = False
        self.shuffle = False
        if self.repeat_one:
            self.repeat_one = False
            self.repeat_one_btn['image'] = self.repeat_one_img
        else:
            self.repeat_one = True
            self.repeat_one_btn['image'] = self.repeat_one_yes_img
            self.repeat_all_btn['image'] = self.repeat_all_img
            self.shuffle_btn['image'] = self.shuffle_img

    def add_song(self, song):
        ''' Add song to global variable and passes it to other function '''
        self.song = song
        self.get_album_art()
        self.change_album_art()

    def get_album_art(self):
        ''' Get song image if available in the APIC data '''
        self.art = ''
        self.no_art = ''
        try:
            mp3 = stagger.read_tag(self.song)
            by_data = mp3[stagger.id3.APIC][0].data
            image_stream = BytesIO(by_data)
            self.art = Image.open(image_stream)
            self.art = self.art.resize((175, 175), Image.ANTIALIAS)
            self.art = ImageTk.PhotoImage(self.art)
        except:
            random_image = choice([str(i) for i in range(1, 11)])
            self.alt_art = f'./static/{random_image}.jpg'
            self.no_art = Image.open(self.alt_art)
            self.no_art = self.no_art.resize((175, 175), Image.ANTIALIAS)
            self.no_art = ImageTk.PhotoImage(self.no_art)

    def change_album_art(self):
        ''' Add image to it if available else use a default image '''
        if type(self.art) == str:
            self.album_art['image'] = self.no_art
        else:
            self.album_art['image'] = self.art

    def show_progress(self, playing_song):
        ''' Show the progress of the music playing '''
        file_details = playing_song
        details = file_details.split('.')

        if details[-1] == 'mp3':
            audio = MP3(playing_song)
            total_duration = audio.info.length
        else:
            audio = mixer.Sound(playing_song)
            total_duration = audio.get_length()

        total_duration = int(total_duration)
        self.progress['to'] = total_duration
        mins, secs = divmod(total_duration, 60)
        mins = round(mins)
        secs = round(secs)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        self.progress_end['text'] = timeformat
        self.single_song_duration = total_duration

        def time_counter():
            if self.current_time == self.single_song_duration:
                print('song ended')
                # self.current_time = 0
                self.next_song('auto next')
            elif self.paused:
                pass
            # elif self.to_break:
            #     pass
            else:
                mins, secs = divmod(self.current_time, 60)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                self.progress_start['text'] = timeformat
                self.progress['value'] = self.current_time
                self.current_time += 1
                # self.progress.update()

            self.progress.after(1000, time_counter)
        if self.pas == False:
            time_counter()
            self.pas = True
        else:
            pass

    def previous_song(self):
        ''' Play the previous song if any '''
        if self.playing == False and self.current_song_index_in_playlist == 0:
            self.current_time = 0
            self.play_btn['image'] = self.pause_img
            directory = self.playlist_in_use[self.current_song_index_in_playlist]
            mixer.music.load(directory)
            mixer.music.play()
            self.current_song = directory
            directory_split = directory.split('/')
            song_title = directory_split[-1][:-4]
            self.current_display['text'] = 'Playing:   ♫ ' + song_title + ' ♫'
            self.playing = True
            self.add_song(directory)
            self.show_progress(directory)
        else:
            try:
                self.current_time = 0
                self.to_break = True
                if self.current_song_index_in_playlist != 0:
                    self.current_song_index_in_playlist -= 1
                if self.shuffle:
                    directory = self.shuffled_playlist[self.current_song_index_in_playlist]
                else:
                    directory = self.original_playlist[self.current_song_index_in_playlist]
                mixer.music.load(directory)
                mixer.music.play()
                self.current_song = directory
                directory_split = directory.split('/')
                song_title = directory_split[-1][:-4]
                self.current_display['text'] = 'Playing:   ♫ ' + \
                    song_title + ' ♫'
                self.add_song(directory)
                self.show_progress(directory)
                self.play_song('next press')
            except KeyError:
                print('Empty playlist')

    def next_song(self, the_type):
        ''' Play the next song if any '''
        if self.current_song_index_in_playlist != len(self.original_playlist) - 1:
            try:
                self.current_time = 0
                if the_type == 'auto next' and self.repeat_one:
                    self.current_song_index_in_playlist = self.current_song_index_in_playlist
                else:
                    self.current_song_index_in_playlist += 1

                self.to_break = True
                if self.shuffle:
                    directory = self.shuffled_playlist[self.current_song_index_in_playlist]
                else:
                    directory = self.original_playlist[self.current_song_index_in_playlist]
                mixer.music.load(directory)
                mixer.music.play()
                self.current_song = directory
                directory_split = directory.split('/')
                song_title = directory_split[-1][:-4]
                self.current_display['text'] = 'Playing:   ♫ ' + \
                    song_title + ' ♫'
                self.add_song(directory)
                self.show_progress(directory)
                self.play_song('next press')
            except KeyError:
                print('Empty playlist')
            except pygame.error as e:
                print(e)
                self.next_song('auto next')
        else:
            if self.repeat_all:
                self.rerun_all_songs_in_playlist()
            elif self.repeat_one:
                self.rerun_single_song_in_playlist()
            else:
                self.to_break = False
                if not mixer.music.get_busy():
                    self.play_btn['image'] = self.play_img
                    self.playing = False

    def play_song(self, the_type, event=None):
        ''' Play the selected song if any '''
        if self.playing == False:
            try:
                self.current_time = 0
                self.play_btn['image'] = self.pause_img
                directory = self.original_playlist[self.current_song_index_in_playlist]
                mixer.music.load(directory)
                mixer.music.play()
                self.current_song = directory
                directory_split = directory.split('/')
                song_title = directory_split[-1][:-4]
                self.current_display['text'] = 'Playing:   ♫ ' + \
                    song_title + ' ♫'
                self.playing = True
                self.add_song(directory)
                self.show_progress(directory)
            except:
                self.play_btn['image'] = self.play_img
        else:
            if self.paused == True and the_type == 'next press':
                self.play_btn['image'] = self.pause_img
                self.paused = False
            elif self.paused == False and the_type == 'next press':
                self.paused == False
            elif self.paused == True:
                mixer.music.unpause()
                self.play_btn['image'] = self.pause_img
                self.paused = False
            else:
                mixer.music.pause()
                self.play_btn['image'] = self.play_img
                self.paused = True

    def remove_all_previous_frames(self):
        ''' Remove all information frames '''
        self.about_app_frame.place_forget()
        self.playlist_frame.place_forget()
        self.about_developer_frame.place_forget()

    def remove_frame(self, window):
        ''' Remove a particular frame '''
        if window == 'view_playlist':
            self.playlist_frame.place_forget()
        if window == 'about_app':
            self.about_app_frame.place_forget()
        if window == 'about_developer':
            self.about_developer_frame.place_forget()

    def about_app(self):
        ''' Display information about the app '''
        self.remove_all_previous_frames()
        self.about_app_frame.place(x=0, y=0)

        back_button = Button(self.about_app_frame, image=self.back, bg="#fff",
                             width=50, command=lambda: self.remove_frame('about_app'))
        back_button.place(x=20, y=15)
        about_text = '''\nWelcome music lover!\n\nSHORTCUTS\nCtrl+A -> Add songs\nCtrl+Q -> Quit app\nCtrl+L -> View playlist\nSpace -> Play or pause music
        \nEnjoy😎!
        '''
        the_label = Label(self.about_app_frame, text=about_text,
                          fg='#f2aa4c', bg='#101820', font='montserrat 14')
        the_label.place(anchor=CENTER, relx=0.5, rely=0.5)

    def view_playlist(self, event=None):
        ''' Display the playlist in use '''
        self.remove_all_previous_frames()
        self.playlist_frame.place(x=0, y=0)
        back_button = Button(self.playlist_frame, image=self.back, bg="#fff",
                             width=50, command=lambda: self.remove_frame('view_playlist'))
        back_button.place(x=20, y=15)
        lists = Listbox(self.playlist_frame, fg='#fff', bg='#252525', font='candara 12',
                        width=65, height=12)
        lists.place(x=20, y=50)
        if self.playlist_in_use == self.original_playlist:
            for values in self.original_playlist.values():
                song_title = values.split('/')
                song_title = song_title[-1][:-4]
                lists.insert(END, '-> ' + song_title)
        else:
            for title in self.shuffled_playlist:
                song_title = title.split('/')
                song_title = song_title[-1][:-4]
                lists.insert(END, '-> ' + song_title)
        try:
            song_currently_playing = self.current_song_index_in_playlist
            if self.playlist_in_use == self.shuffled_playlist:
                currently_playing_index = self.shuffled_playlist.index(
                    self.current_song)
            else:
                currently_playing_index = [
                    k for k, v in self.original_playlist.items() if v == self.current_song][0]
            lists.itemconfig(currently_playing_index, {
                             'bg': '#101820', 'fg': 'white'})
        except IndexError:
            print("No song in playlist")
        except ValueError:
            print("No song is playing or paused")

    def add_songs_to_playlist(self, event=None):
        ''' Add song from pc to app playlist '''
        filenames = askopenfilenames(
            filetypes=[('audio files', '*.mp3 *.wav *.ogg')])
        for _file in filenames:
            if _file not in self.original_playlist.values():
                file_name = _file
                self.original_playlist[self.last_dict_key] = file_name
                song_details = file_name.split('/')
                song_details = song_details[-1][:-4]
                self.music_details.append(song_details)
                self.last_dict_key += 1

    def show_quit_frame(self, event=None):
        ''' Show some text for 3 seconds before quiting the app '''
        self.remove_all_previous_frames()
        self.quitting_frame.place(x=0, y=0)
        about_text = '''\nThanks for using my app!\n\nPlease contact me for any questions, comments,\ncollaborations or critique even.\nAlways ready to talk.
        \n Thank you.
        '''
        the_label = Label(self.quitting_frame, text=about_text,
                          fg='#f2aa4c', bg='#101820', font='montserrat 14')
        the_label.place(anchor=CENTER, relx=0.5, rely=0.47)

        r = Timer(5.0, lambda: self.quit_app())
        r.start()

    def quit_app(self, event=None):
        ''' Quit the app '''
        self.root.quit()

    def about_developer(self):
        ''' Display information about the app developer '''
        self.remove_all_previous_frames()
        self.about_developer_frame.place(x=0, y=0)

        back_button = Button(self.about_developer_frame, image=self.back, bg="#fff",
                             width=50, command=lambda: self.remove_frame('about_developer'))
        back_button.place(x=20, y=15)
        the_label = Label(self.about_developer_frame, text='I am an experienced python desktop\n\
            application and web programmer!\
            \nFind more of my works at:', fg='#f2aa4c', bg='#101820', font='montserrat 14')
        the_label.place(anchor=CENTER, relx=0.5, rely=0.4)
        the_github = Entry(self.about_developer_frame, width=30,
                           justify='center', font='montserrat 14')
        the_github.insert(0, "https://github.com/TomiwaJoseph")
        the_github.configure(fg='#f2aa4c', state="readonly",
                             readonlybackground="#101820")
        the_github.place(anchor=CENTER, relx=0.5, rely=0.6)

    def mute_and_unmute_song(self):
        ''' Mute and unmute the song according to button press '''
        if self.mute == False:
            self.speaker_btn['image'] = self.mute_img
            mixer.music.set_volume(0.0)
            self.mute = True
        else:
            self.speaker_btn['image'] = self.speaker_img
            value = self.volume.get()
            mixer.music.set_volume(float(value)/100)
            self.mute = False

    def set_volume(self, value):
        ''' Adjust music volume '''
        new = self.volume.get()
        if new == float(0):
            self.speaker_btn['image'] = self.mute_img
            mixer.music.set_volume(0.0)
        else:
            self.speaker_btn['image'] = self.speaker_img
            volume = float(new) / 100
            mixer.music.set_volume(volume)


if __name__ == '__main__':
    app = Switch()
    app.title('Music Player')
    ico = Image.open('./static/icon.ico')
    photo = ImageTk.PhotoImage(ico)
    app.wm_iconphoto(False, photo)
    app.mainloop()
