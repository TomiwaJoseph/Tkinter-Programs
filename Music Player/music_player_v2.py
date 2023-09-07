from tkinter import *
from tkinter.filedialog import *
from pygame import mixer
from io import BytesIO
import pygame
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from tkinter import ttk
from PIL import ImageTk, Image
from threading import Timer
from random import shuffle, choice
from eyed3 import id3 as eye
import webbrowser
import pyperclip


root = Tk
pygame.init()


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
        self.root.geometry('1000x500+183+134')
        self.root.resizable(0, 0)
        # ======= UI =====================
        self.bg = Image.open('./static/icon.ico')
        self.bg = self.bg.resize((54, 54), Image.LANCZOS)
        self.the_logo = ImageTk.PhotoImage(self.bg)
        self.app_logo = Frame(width=62, height=60,
                              relief='ridge', bg='#101820', bd=2)
        self.app_logo.place(relx=0.4, rely=0.5, anchor=CENTER)
        Label(self.app_logo, image=self.the_logo).place(x=0, y=0)
        # ======= Title =====================
        Label(self.master, text="PlayIt", font=('AdobeClean-Bold', 40), fg='#f2aa4c',
              bg='#101820', justify='left').place(relx=0.51, rely=0.5, anchor=CENTER)

        # ======= SHOW STARTPAGE FOR 3 ONLY SECONDS =====================
        r = Timer(3.0, lambda: self.master.switch_frame(MusicPage))
        r.start()


class MusicPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.configure(self, bg='#101820')
        self.root = root
        self.root.geometry('1000x500+183+134')
        self.root.resizable(0, 0)
        # ============ VARIABLES ====================
        self.original_playlist = {}
        self.shuffled_playlist = []
        self.playlist_in_use = self.original_playlist
        self.current_song_index_in_playlist = 0
        self.paused = False
        self.mute = False
        self.playing = False
        self.to_break = False
        self.current_play_time = 0
        self.current_song = ''
        self.song = ''
        self.single_song_duration = 0
        self.repeat_one = False
        self.repeat_all = False
        self.shuffle = False
        self.auto_next_button_press = False
        self.last_dict_key = 0
        self.breaking = False
        self.playlist_window_is_open = False
        self.about_window_is_open = False
        # ============ KeyBinds ====================
        self.create_keybinds()
        # ========= MENUBAR ==============
        self.create_menubar()
        # ============ USER INTERFACE ====================
        self.create_ui()
        # ============ Utility Frames ====================
        self.quitting_frame = Frame(
            width=1000, height=500, relief='ridge', bg='#101820')

    def create_keybinds(self):
        ''' Create shortcuts eg. CTRL + Z, CTRL + X '''
        self.root.bind('<Control-A>', self.add_songs_to_playlist)
        self.root.bind('<Control-a>', self.add_songs_to_playlist)
        self.root.bind('<Control-Q>', self.show_quit_frame)
        self.root.bind('<Control-q>', self.show_quit_frame)
        self.root.bind('<Control-L>', self.view_playlist)
        self.root.bind('<Control-l>', self.view_playlist)
        self.root.bind('<M>', self.mute_and_unmute_song)
        self.root.bind('<m>', self.mute_and_unmute_song)
        self.root.bind('<P>', self.previous_song)
        self.root.bind('<p>', self.previous_song)
        self.root.bind('<N>', self.next_song)
        self.root.bind('<n>', self.next_song)
        self.root.bind('<S>', self.shuffle_playlist)
        self.root.bind('<s>', self.shuffle_playlist)
        self.root.bind('<E>', self.repeat_all_songs)
        self.root.bind('<e>', self.repeat_all_songs)
        self.root.bind('<R>', self.repeat_current_song)
        self.root.bind('<r>', self.repeat_current_song)
        self.root.bind('<space>', lambda t: self.play_song(
            'button press') if self.original_playlist else print('Empty playlist'))

    def create_ui(self):
        ''' Create the user interface which include buttons and stuff '''
        # ============ Album Art ====================
        self.cover = Image.open('./static/icon.ico')
        self.cover = self.cover.resize((300, 300), Image.LANCZOS)
        self.cover = ImageTk.PhotoImage(self.cover)
        self.album_art = Label(
            image=self.cover, relief='ridge', width=230, height=230)
        self.album_art.place(relx=0.5, rely=0.31, anchor=CENTER)
        # ============ CONTROL FRAME ====================
        self.control_frame = Frame(
            width=850, height=80, relief='ridge', bg='#101820', bd=3)
        self.control_frame.place(relx=0.5, rely=0.85, anchor=CENTER)
        # ============ Prev Button ====================
        self.prev_bg = Image.open('./static/_previous.png')
        self.prev_bg = self.prev_bg.resize((50, 50), Image.LANCZOS)
        self.prev_img = ImageTk.PhotoImage(self.prev_bg)
        self.previous_btn = Button(
            self.control_frame, image=self.prev_img, bd=0, command=self.previous_song, bg='#101820')
        self.previous_btn.place(relx=0.1, rely=0.5, anchor=CENTER)
        # ============ Play Button ====================
        self.play_bg = Image.open('./static/_play.png')
        self.play_bg = self.play_bg.resize((50, 50), Image.LANCZOS)
        self.play_img = ImageTk.PhotoImage(self.play_bg)
        self.pause_bg = Image.open('./static/_pause.png')
        self.pause_bg = self.pause_bg.resize((50, 50), Image.LANCZOS)
        self.pause_img = ImageTk.PhotoImage(self.pause_bg)
        self.play_btn = Button(self.control_frame, image=self.play_img, bd=0,
                               command=lambda: self.play_song('button press'), bg='#101820')
        self.play_btn.place(relx=0.199, rely=0.5, anchor=CENTER)
        # ============ Next Button ====================
        self.bg = Image.open('./static/_next.png')
        self.bg = self.bg.resize((50, 50), Image.LANCZOS)
        self.next_img = ImageTk.PhotoImage(self.bg)
        self.next_btn = Button(self.control_frame, image=self.next_img,
                               bd=0, command=lambda: self.next_song('from button'), bg='#101820')
        self.next_btn.place(relx=0.3, rely=0.5, anchor=CENTER)
        # ============ View Playlist Button ====================
        self.bg = Image.open('./static/_playlist.png')
        self.bg = self.bg.resize((20, 20), Image.LANCZOS)
        self.view_playlist_img = ImageTk.PhotoImage(self.bg)
        self.repeat_all_btn = Button(
            self.control_frame, image=self.view_playlist_img, bd=0, command=self.view_playlist, bg='#101820')
        self.repeat_all_btn.place(relx=0.4, rely=0.5, anchor=CENTER)
        # ============ Repeat All Button ====================
        self.bg = Image.open('./static/_repeat_all_yes.png')
        self.bg = self.bg.resize((20, 20), Image.LANCZOS)
        self.repeat_all_yes_img = ImageTk.PhotoImage(self.bg)
        self.bg = Image.open('./static/_repeat_all_icon.png')
        self.bg = self.bg.resize((20, 20), Image.LANCZOS)
        self.repeat_all_img = ImageTk.PhotoImage(self.bg)
        self.repeat_all_btn = Button(
            self.control_frame, image=self.repeat_all_img, bd=0, command=self.repeat_all_songs, bg='#101820')
        self.repeat_all_btn.place(relx=0.48, rely=0.5, anchor=CENTER)
        # ============ Repeat One Button ====================
        self.bg = Image.open('./static/_repeat_one_yes.png')
        self.bg = self.bg.resize((20, 20), Image.LANCZOS)
        self.repeat_one_yes_img = ImageTk.PhotoImage(self.bg)
        self.bg = Image.open('./static/_repeat_one_icon.png')
        self.bg = self.bg.resize((20, 20), Image.LANCZOS)
        self.repeat_one_img = ImageTk.PhotoImage(self.bg)
        self.repeat_one_btn = Button(
            self.control_frame, image=self.repeat_one_img, bd=0, command=self.repeat_current_song, bg='#101820')
        self.repeat_one_btn.place(relx=0.55, rely=0.5, anchor=CENTER)
        # ============ Shuffle Button ====================
        self.bg = Image.open('./static/_shuffle_yes.png')
        self.bg = self.bg.resize((20, 20), Image.LANCZOS)
        self.shuffle_yes_img = ImageTk.PhotoImage(self.bg)
        self.bg = Image.open('./static/_shuffle_icon.png')
        self.bg = self.bg.resize((20, 20), Image.LANCZOS)
        self.shuffle_img = ImageTk.PhotoImage(self.bg)
        self.shuffle_btn = Button(self.control_frame, image=self.shuffle_img,
                                  bd=0, command=self.shuffle_playlist, bg='#101820')
        self.shuffle_btn.place(relx=0.63, rely=0.5, anchor=CENTER)
        # ============ Progress Bar ====================
        self.progress = ttk.Scale(from_=0, to=100, orient=HORIZONTAL, length=700,
                                  command=self.forwards_or_backwards)
        self.progress.place(relx=0.5, rely=0.72, anchor=CENTER)
        self.progress_start = Label(
            font=('AdobeClean-Bold', 13), fg='#f2aa4c', bg='#101820', text='5:00:00')
        self.progress_start.place(relx=0.11, rely=0.72, anchor=CENTER)
        self.progress_end = Label(
            font=('AdobeClean-Bold', 13), fg='#f2aa4c', bg='#101820', text='5:00:00')
        self.progress_end.place(relx=0.89, rely=0.72, anchor=CENTER)

        self.song_artist_and_title = Text(width=70, height=1, font=(
            'AdobeClean-REGULAR', 14), fg='#101820', bg='#f2aa4c')
        self.song_artist_and_title.tag_configure('center', justify='center')
        self.song_artist_and_title.tag_configure(
            'bold', font=('AdobeClean-Bold', 14), justify='center')
        self.song_artist_and_title.place(relx=0.5, rely=0.64, anchor=CENTER)
        self.song_artist_and_title.insert('end', '♫   ', 'center')
        self.song_artist_and_title.insert('end', 'No Song title / ', 'bold')
        self.song_artist_and_title.insert('end', 'No Artist   ♫')
        self.song_artist_and_title.configure(state=DISABLED)
        # ============ Mute and Volume ====================
        self.bg = Image.open('./static/_mute_icon.png')
        self.bg = self.bg.resize((20, 20), Image.LANCZOS)
        self.mute_img = ImageTk.PhotoImage(self.bg)
        self.bg = Image.open('./static/_volume_icon.png')
        self.bg = self.bg.resize((20, 20), Image.LANCZOS)
        self.speaker_img = ImageTk.PhotoImage(self.bg)
        self.speaker_btn = Button(self.control_frame, image=self.speaker_img,
                                  bd=0, command=self.mute_and_unmute_song, bg='#101820')
        self.speaker_btn.place(relx=0.72, rely=0.5, anchor=CENTER)
        style = ttk.Style(self.root)
        style.theme_use('clam')
        self.volume = ttk.Scale(self.control_frame, from_=0, to=100, orient=HORIZONTAL, length=150,
                                command=self.set_volume)
        self.volume.set(40)
        self.volume.place(relx=0.84, rely=0.5, anchor=CENTER)

    def create_menubar(self):
        ''' Create the menubar where thing like File, About etc. reside '''
        self.bg = Image.open('./static/_add_icon.png')
        self.bg = self.bg.resize((12, 12), Image.LANCZOS)
        self.add_icon = ImageTk.PhotoImage(self.bg)

        self.bg = Image.open('./static/_exit_icon.png')
        self.bg = self.bg.resize((12, 12), Image.LANCZOS)
        self.exit_icon = ImageTk.PhotoImage(self.bg)

        self.bg = Image.open('./static/_playlist_icon.png')
        self.bg = self.bg.resize((12, 12), Image.LANCZOS)
        self.playlist_view_icon = ImageTk.PhotoImage(self.bg)

        self.bg = Image.open('./static/_play_icon.png')
        self.bg = self.bg.resize((12, 12), Image.LANCZOS)
        self.play_icon = ImageTk.PhotoImage(self.bg)

        self.bg = Image.open('./static/_previous_icon.png')
        self.bg = self.bg.resize((12, 12), Image.LANCZOS)
        self.prev_icon = ImageTk.PhotoImage(self.bg)

        self.bg = Image.open('./static/_next_icon.png')
        self.bg = self.bg.resize((12, 12), Image.LANCZOS)
        self.next_icon = ImageTk.PhotoImage(self.bg)

        self.bg = Image.open('./static/_repeat_all_icon.png')
        self.bg = self.bg.resize((15, 15), Image.LANCZOS)
        self.repeat_icon = ImageTk.PhotoImage(self.bg)

        self.bg = Image.open('./static/_repeat_one_icon.png')
        self.bg = self.bg.resize((15, 15), Image.LANCZOS)
        self.repeat_one_icon = ImageTk.PhotoImage(self.bg)

        self.bg = Image.open('./static/_shuffle_icon.png')
        self.bg = self.bg.resize((15, 15), Image.LANCZOS)
        self.shuffle_icon = ImageTk.PhotoImage(self.bg)

        self.bg = Image.open('./static/_about_icon.png')
        self.bg = self.bg.resize((15, 15), Image.LANCZOS)
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
                                      command=lambda: self.play_song('button press'), accelerator='Space', compound='left')
        self.playbackmenu.add_command(label='Previous', image=self.prev_icon,
                                      command=self.previous_song, accelerator='P', compound='left')
        self.playbackmenu.add_command(label='Next', image=self.next_icon,
                                      command=lambda: self.next_song('from button'), accelerator='N', compound='left')
        self.playbackmenu.add_command(label='Repeat All', image=self.repeat_icon,
                                      command=self.repeat_all_songs, accelerator='E', compound='left')
        self.playbackmenu.add_command(label='Repeat One', image=self.repeat_one_icon,
                                      command=self.repeat_current_song, accelerator='R', compound='left')
        self.playbackmenu.add_command(label='Shuffle', image=self.shuffle_icon,
                                      command=self.shuffle_playlist, accelerator='S', compound='left')

        self.viewmenu.add_command(label='View Playlist', image=self.playlist_view_icon,
                                  command=self.view_playlist, accelerator='Ctrl+L', compound='left')

        self.helpmenu.add_command(label='About', image=self.about_icon,
                                  command=self.about_app, compound='left')

    def change_root_title(self):
        song_title = self.current_song.split('/')
        song_title = song_title[-1][:-4]
        self.root.title(f"{song_title} - PlayIt")

    def forwards_or_backwards(self, value):
        ''' Fast forward or rewind playing music '''
        new_position = int(self.progress.get())
        self.current_playing_time = new_position
        if self.paused:
            self.play_btn['image'] = self.pause_img
            self.paused = False
        try:
            mixer.music.load(
                self.playlist_in_use[self.current_song_index_in_playlist])
            mixer.music.play(loops=0, start=new_position)
        except KeyError:
            print("No song is currently playing...")

    def rerun_single_song_in_playlist(self):
        ''' Play current song again after it ends '''
        self.current_playing_time = 0
        self.current_song_index_in_playlist = self.current_song_index_in_playlist
        self.to_break = True
        directory = self.original_playlist[self.current_song_index_in_playlist]
        mixer.music.load(directory)
        mixer.music.play()
        self.current_song = directory
        self.add_song(directory)
        self.show_progress(directory)
        self.get_and_set_music_title_artist(directory)
        self.change_root_title()

    def rerun_all_songs_in_playlist(self):
        ''' Replay all songs in the playlist once it ends '''
        self.current_playing_time = 0
        self.current_song_index_in_playlist = 0
        self.to_break = True
        directory = self.original_playlist[self.current_song_index_in_playlist]
        mixer.music.load(directory)
        mixer.music.play()
        self.add_song(directory)
        self.show_progress(directory)
        self.get_and_set_music_title_artist(directory)
        self.change_root_title()

    def shuffle_playlist(self, event=None):
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

    def repeat_all_songs(self, event=None):
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

    def repeat_current_song(self, event=None):
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

    def get_and_set_music_title_artist(self, the_song):
        try:
            tag = eye.Tag()
            tag.parse(the_song)
            song_artist = tag.artist
            song_title = tag.title
            self.song_artist_and_title.configure(state=NORMAL)
            self.song_artist_and_title.delete('1.0', 'end')
            self.song_artist_and_title.insert('end', '♫   ', 'center')
            if song_title == None:
                self.song_artist_and_title.insert(
                    'end', 'Unknown Title / ', 'bold')
            else:
                self.song_artist_and_title.insert(
                    'end', song_title + ' / ', 'bold')

            if song_artist == None:
                self.song_artist_and_title.insert('end', 'Unknown Artist ♫')
            else:
                self.song_artist_and_title.insert('end', song_artist+'   ♫')
        except:
            self.song_artist_and_title.delete('1.0', 'end')
            self.song_artist_and_title.insert('end', '♫   ', 'center')
            self.song_artist_and_title.insert(
                'end', 'Unknown Title / ', 'bold')
            self.song_artist_and_title.insert('end', 'Unknown Artist ♫')

        self.song_artist_and_title.configure(state=DISABLED)

    def play_selected_playlist_item(self):
        try:
            selection = self.musicList.curselection()[0]
            self.current_playing_time = 0
            self.current_song_index_in_playlist = selection
            self.play_btn['image'] = self.pause_img
            directory = self.playlist_in_use[self.current_song_index_in_playlist]
            mixer.music.load(directory)
            mixer.music.play()
            self.current_song = directory
            self.playing = True
            self.add_song(directory)
            self.show_progress(directory)
            self.get_and_set_music_title_artist(directory)
            self.change_root_title()
        except IndexError:
            print('No item selected')

    def delete_selected_playlist_item(self):
        try:
            selection = self.musicList.curselection()[0]
            if selection == self.current_song_index_in_playlist:
                # since the deleted song is playing stop music
                self.current_playing_time = 0
                self.current_song_index_in_playlist = 0
                self.paused = True
                self.play_btn['image'] = self.play_img
                self.current_song = ""
                self.progress['value'] = 0
                self.progress_end['text'] = '5:00:00'
                self.progress_start['text'] = '5:00:00'
                self.playing = False
                self.song_artist_and_title.configure(state=NORMAL)
                self.song_artist_and_title.delete('1.0', 'end')
                self.song_artist_and_title.insert('end', '♫   ', 'center')
                self.song_artist_and_title.insert(
                    'end', 'Unknown Title / ', 'bold')
                self.song_artist_and_title.insert('end', 'Unknown Artist ♫')
                self.song_artist_and_title.configure(state=DISABLED)
                mixer.music.stop()
                self.root.title('PlayIt')
                # self.root.update()
                # change the picture to default
                self.album_art['image'] = self.cover
                # delete the song in both playlist
                if self.playlist_in_use == self.original_playlist:
                    song_to_delete = self.original_playlist[selection]
                else:
                    song_to_delete = self.shuffled_playlist[selection]
                original_playlist_key = [
                    key for key, value in self.original_playlist.items() if value == song_to_delete][0]
                del self.original_playlist[original_playlist_key]
                # if the shuffled list has been created
                if self.shuffled_playlist != []:
                    shuffled_playlist_index = self.shuffled_playlist.index(
                        song_to_delete)
                    del self.shuffled_playlist[shuffled_playlist_index]

                # make the keys in original_playlist be in numerical order
                old_keys = list(self.original_playlist.keys())
                for i in range(len(old_keys)):
                    self.original_playlist[i] = self.original_playlist.pop(
                        old_keys[i])
                if old_keys:
                    self.last_dict_key = i + 1
                else:
                    self.last_dict_key = 0
            else:
                # delete the song in both playlist and keep playing song
                if self.playlist_in_use == self.original_playlist:
                    song_to_delete = self.original_playlist[selection]
                else:
                    song_to_delete = self.shuffled_playlist[selection]
                original_playlist_key = [
                    key for key, value in self.original_playlist.items() if value == song_to_delete][0]
                del self.original_playlist[original_playlist_key]

                if self.shuffled_playlist != []:
                    shuffled_playlist_index = self.shuffled_playlist.index(
                        song_to_delete)
                    del self.shuffled_playlist[shuffled_playlist_index]

                # make the keys in original_playlist be in numerical order
                old_keys = list(self.original_playlist.keys())
                for i in range(len(old_keys)):
                    self.original_playlist[i] = self.original_playlist.pop(
                        old_keys[i])
                self.last_dict_key = i + 1
            # close window and open it again to display changes made
            self.playlistWindow.destroy()
            self.view_playlist()
        except IndexError:
            print('No item selected')

    def view_playlist(self, event=None):
        ''' Display the playlist in use '''
        if self.playlist_window_is_open == True:
            self.playlistWindow.destroy()
        if self.about_window_is_open == True:
            self.aboutWindow.destroy()

        self.playlistWindow = Toplevel(self.root)
        self.playlistWindow.config(bg='#101820')
        self.playlistWindow.geometry("500x520+433+124")
        self.playlistWindow.title('PlayIt - Playlist')
        self.playlistWindow.resizable(0, 0)
        self.playlistWindow.iconbitmap(r'./static/icon.ico')
        self.playlist_window_is_open = True

        # ========= PLAYLIST FRAME ==================
        music_list_frame = Frame(self.playlistWindow, width=400, height=300)
        music_list_frame.place(anchor=CENTER, relx=0.5, rely=0.42)
        self.musicList = Listbox(music_list_frame, height=13, width=42,
                                 fg='#fff', bg='#222222', font=('AdobeClean-REGULAR', 13))
        self.musicList.pack(side='left', fill='y')
        # ========= Scrollbar =========
        scroll = Scrollbar(music_list_frame, orient='vertical', bg='red')
        scroll.pack(side='right', fill='y')
        scroll.config(command=self.musicList.yview)
        self.musicList.config(yscrollcommand=scroll.set)

        # ========= UTILITY TOOLS FRAME ==================
        utility_tools_frame = Frame(
            self.playlistWindow, width=400, bd=2, height=53, relief='ridge', bg='#101820')
        utility_tools_frame.place(anchor=CENTER, relx=0.5, rely=0.8)
        self.playlist_play_btn = Button(utility_tools_frame, fg='#101820', bg='#f2aa4c', text='Play',
                                        font=('AdobeClean-REGULAR', 13), width=17, command=self.play_selected_playlist_item)
        self.playlist_play_btn.place(anchor=CENTER, relx=0.25, rely=0.5)
        self.playlist_delete_btn = Button(utility_tools_frame, fg='#101820', bg='#f2aa4c', text='Delete',
                                          font=('AdobeClean-REGULAR', 13), width=17, command=self.delete_selected_playlist_item)
        self.playlist_delete_btn.place(anchor=CENTER, relx=0.75, rely=0.5)

        if self.playlist_in_use == self.original_playlist:
            for values in self.original_playlist.values():
                song_title = values.split('/')
                song_title = song_title[-1][:-4]
                self.musicList.insert(END, '-> ' + song_title)
        else:
            for title in self.shuffled_playlist:
                song_title = title.split('/')
                song_title = song_title[-1][:-4]
                self.musicList.insert(END, '-> ' + song_title)

        try:
            if self.playlist_in_use == self.shuffled_playlist:
                currently_playing_index = self.shuffled_playlist.index(
                    self.current_song)
            else:
                currently_playing_index = [
                    k for k, v in self.original_playlist.items() if v == self.current_song][0]
            self.musicList.itemconfig(currently_playing_index, {
                                      'bg': '#f2aa4c', 'fg': '#101820'})
            self.musicList.see(currently_playing_index)
        except:
            print("No song in playlist or no song is playing or paused")

    def about_app(self):
        ''' Display information about the app '''
        if self.about_window_is_open == True:
            self.aboutWindow.destroy()
        if self.playlist_window_is_open == True:
            self.playlistWindow.destroy()

        self.aboutWindow = Toplevel(self.root)
        self.aboutWindow.config(bg='#101820')
        self.aboutWindow.geometry("500x520+433+124")
        self.aboutWindow.title('PlayIt - About')
        self.aboutWindow.resizable(0, 0)
        self.aboutWindow.iconbitmap(r'./static/icon.ico')
        self.about_window_is_open = True

        about_text = 'Welcome music lover! \n'\
            'PlayIt is a powerful and fast music player with elegant \n'\
            'design. This audio player supports music in mp3, wav and \n'\
            'ogg audio formats. Enjoy😎!'
        shortcuts_text = 'All features work! Here are some shortcuts: \n'\
            'Space -> Play or pause music, Ctrl+L -> View playlist, \n'\
            'Ctrl+A -> Add songs, Ctrl+Q -> Quit app , M -> Mute, \n'\
            'N -> Next, P -> Previous, S -> Shuffle, R -> Repeat One, \n'\
            'E -> Repeat All \n'\

        app_name = Label(self.aboutWindow, text='PlayIt - Music Player', font=('AdobeClean-Bold', 15),
                         fg='#f2aa4c', bg='#101820')
        app_name.place(anchor=CENTER, relx=0.5, rely=0.12)
        app_version = Label(self.aboutWindow, text='Version 1.1', font=('AdobeClean-REGULAR', 10),
                            fg='#fff', bg='#101820')
        app_version.place(anchor=CENTER, relx=0.5, rely=0.16)
        demarcation = Frame(self.aboutWindow, height=1, width=390,
                            highlightthickness=1, highlightbackground='#f2aa4c')
        demarcation.place(anchor=CENTER, relx=0.5, rely=0.21)

        about_app = Label(self.aboutWindow, text=about_text, font=('AdobeClean-REGULAR', 12),
                          fg='#fff', bg='#101820', justify=LEFT)
        about_app.place(anchor=CENTER, relx=0.5, rely=0.31)
        demarcation2 = Frame(self.aboutWindow, height=1, width=390,
                             highlightthickness=1, highlightbackground='#f2aa4c')
        demarcation2.place(anchor=CENTER, relx=0.5, rely=0.42)

        shortcut_header = Label(self.aboutWindow, text='Shortcuts', font=('AdobeClean-Bold', 13),
                                fg='#f2aa4c', bg='#101820')
        shortcut_header.place(anchor=CENTER, relx=0.18, rely=0.46)
        shorcuts = Label(self.aboutWindow, text=shortcuts_text, font=('AdobeClean-REGULAR', 12),
                         fg='#fff', bg='#101820', justify=LEFT)
        shorcuts.place(anchor=CENTER, relx=0.48, rely=0.62)
        demarcation3 = Frame(self.aboutWindow, height=1, width=390,
                             highlightthickness=1, highlightbackground='#f2aa4c')
        demarcation3.place(anchor=CENTER, relx=0.5, rely=0.72)

        contact_me = Label(self.aboutWindow, text='Contact Me', font=('AdobeClean-Bold', 13),
                           fg='#f2aa4c', bg='#101820')
        contact_me.place(anchor=CENTER, relx=0.19, rely=0.76)
        github_contact = Button(self.aboutWindow, text='Go to my GitHub', font=('AdobeClean-Bold', 13),
                                fg='#101820', bg='#f2aa4c', command=self.open_github, width=18)
        github_contact.place(anchor=CENTER, relx=0.29, rely=0.83)
        copy_email = Button(self.aboutWindow, text='Copy my email address', font=('AdobeClean-Bold', 13),
                            fg='#101820', bg='#f2aa4c', command=self.copy_email_address, width=18)
        copy_email.place(anchor=CENTER, relx=0.7, rely=0.83)

    def copy_email_address(self):
        pyperclip.copy('tomiwajoseph88@gmail.com')

    def open_github(self):
        webbrowser.open_new('https://github.com/TomiwaJoseph')

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
            music = ID3(self.song)
            artwork = music.getall("APIC")[0].data            
            image_stream = BytesIO(artwork)
            self.art = Image.open(image_stream)
            self.art = self.art.resize((225, 225), Image.LANCZOS)
            self.art = ImageTk.PhotoImage(self.art)
        except Exception as e:
            random_image = choice([str(i) for i in range(1, 11)])
            self.alt_art = f'./static/{random_image}.jpg'
            self.no_art = Image.open(self.alt_art)
            self.no_art = self.no_art.resize((225, 225), Image.LANCZOS)
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
            if self.current_playing_time == self.single_song_duration:
                self.next_song('auto next')
            elif self.paused:
                pass
            else:
                mins, secs = divmod(self.current_playing_time, 60)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                self.progress_start['text'] = timeformat
                self.progress['value'] = self.current_playing_time
                self.current_playing_time += 1

            self.progress.after(1000, time_counter)
        if self.breaking == False:
            time_counter()
            self.breaking = True
        else:
            pass

    def previous_song(self, event=None):
        ''' Play the previous song if any '''
        if self.playing == False and self.current_song_index_in_playlist == 0:
            self.current_playing_time = 0
            self.play_btn['image'] = self.pause_img
            directory = self.playlist_in_use[self.current_song_index_in_playlist]
            mixer.music.load(directory)
            mixer.music.play()
            self.current_song = directory
            self.playing = True
            self.add_song(directory)
            self.show_progress(directory)
            self.get_and_set_music_title_artist(directory)
            self.change_root_title()
        else:
            try:
                self.current_playing_time = 0
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
                self.add_song(directory)
                self.show_progress(directory)
                self.get_and_set_music_title_artist(directory)
                self.change_root_title()
                self.play_song('next press')
            except KeyError:
                print('Empty playlist')

    def next_song(self, the_type, event=None):
        ''' Play the next song if any '''
        if self.current_song_index_in_playlist != len(self.original_playlist) - 1:
            try:
                self.current_playing_time = 0
                if the_type == 'auto next' and self.repeat_one:
                    self.current_song_index_in_playlist = self.current_song_index_in_playlist
                else:
                    self.current_song_index_in_playlist += 1

                self.to_break = True
                directory = self.playlist_in_use[self.current_song_index_in_playlist]
                mixer.music.load(directory)
                mixer.music.play()
                self.current_song = directory
                self.add_song(directory)
                self.show_progress(directory)
                self.get_and_set_music_title_artist(directory)
                self.change_root_title()
                self.play_song('next press')
            except KeyError:
                print('Empty playlist or last song')
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
                self.current_playing_time = 0
                self.play_btn['image'] = self.pause_img
                directory = self.original_playlist[self.current_song_index_in_playlist]
                mixer.music.load(directory)
                mixer.music.play()
                self.current_song = directory
                self.playing = True
                self.paused = False
                self.add_song(directory)
                self.show_progress(directory)
                self.get_and_set_music_title_artist(directory)
                self.change_root_title()
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
                self.last_dict_key += 1

    def show_quit_frame(self, event=None):
        ''' Show some text for 3 seconds before quiting the app '''
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

    def mute_and_unmute_song(self, event=None):
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
    app.title('PlayIt')
    app.iconbitmap(r'./static/icon.ico')
    app.mainloop()
