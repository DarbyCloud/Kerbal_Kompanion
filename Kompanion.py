from configparser import ConfigParser
from threading import Thread
from time import sleep

from PIL import Image

from customtkinter import *
import krpc

app_name = 'Kerbal Kompanion'

config = ConfigParser()
config_file = 'settings.ini'
config.read(config_file)
connection = config['connection']

class Connection(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='transparent')

        # add logo
        self.image = CTkImage(Image.open('icons/logo.png'), size=(260, 260))
        self.image_label = CTkLabel(self, image=self.image, text='').pack(pady=(50, 0))

        # add input
        self.input()

    # construct and return frame with entries and button
    def input(self):
        # construct entry box
        def entry(placeholder, value):
            entry = CTkEntry(self.frame, width=250, placeholder_text=placeholder, justify='center')
            entry.pack(padx=20, pady=(0, 5))
            entry.insert(0, value)
            return entry
        
        # add frame
        self.frame = CTkFrame(self)
        self.frame.pack()

        # add label
        self.label = CTkLabel(self.frame, text='kRPC Server:')
        self.label.pack(pady=5)

        # add entry boxes
        self.address_entry = entry('Address', connection['address'])
        self.rpc_port_entry = entry('RPC Port', connection['rpc_port'])
        self.stream_port_entry = entry('Stream Port', connection['stream_port'])

        # add connect button
        self.connect_button = CTkButton(
            self.frame,
            text = 'Connect',
            text_color = 'black',
            fg_color = '#84bd08',
            hover_color = '#425e04',
            command = self.connect)
        self.connect_button.pack(pady=(5, 15))

        return self.frame

    # returns current game mode
    def get_game_mode(self):
        game_mode = str(self.ksp.space_center.game_mode)
        print(game_mode)
        return game_mode

    # returns current scene
    def get_scene(self):
        current_scene = str(self.ksp.krpc.current_game_scene)
        return current_scene

    # monitor connection to kRPC server (runs in new thread)
    def start_connection_monitor(self):
        def monitor():
            while True:
                try:
                    self.ksp.krpc.get_status().version
                    sleep(5)
                except ConnectionAbortedError:
                    ErrorHandler(app.connect).aborted()
                    break

        Thread(name='connection_monitor', target=monitor, daemon=True).start()

    # monitor the current game scene (runs in new thread)
    def start_scene_monitor(self):
        def monitor():
            while True:
                try:
                    scene = self.get_scene()
                    if scene == 'GameScene.space_center':
                        print('Space Center')
                    elif scene == 'GameScene.editor_vab':
                        print('VAB')
                    sleep(5)
                except:
                    print('Something went wrong here!')
                    break
        
        Thread(name='scene_monitor', target=monitor, daemon=True).start()

    # save entry values to settings.ini
    def save_connection(self):
        connection['address'] = self.address_entry.get()
        connection['rpc_port'] = self.rpc_port_entry.get()
        connection['stream_port'] = self.stream_port_entry.get()

        with open(config_file, 'w') as configfile:
            config.write(configfile)

        print('Settings saved')

    # establish connection to kRPC server
    def connect(self):
        try:
            self.ksp = krpc.connect(
                name=app_name,
                address=self.address_entry.get(),
                rpc_port=int(self.rpc_port_entry.get()),
                stream_port=int(self.stream_port_entry.get())
            )
        except ConnectionRefusedError:
            ErrorHandler(app.connect).refused()
        else:
            # save and monitor server connection
            self.save_connection()
            self.start_connection_monitor()

            # hide connection screen
            app.connect.pack_forget()

            # create main app frame where all widgets are added
            self.content = Content(app)
            self.content.pack(expand=True, fill=BOTH)
            # start_scene_monitor()

            ########## ADD WIDGETS ##########
            assets = Assets(self.content.top_bar)
            assets.pack(pady=4)


# define frame to contain widgets
class Content(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='transparent')

        self.top_bar = CTkFrame(self, border_width=2)
        self.top_bar.pack(padx=10, pady=10, fill=X)

        self.main = CTkFrame(self, fg_color='transparent')
        self.main.pack(expand=True, fill=BOTH)


# define asset widget
class Assets(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='transparent')

        mode = app.connect.get_game_mode()

        if mode == 'GameMode.career':
            career_assets = ['funds', 'reputation', 'science']
            for i in career_assets:
                self.asset(i)
        elif mode == 'GameMode.science_sandbox':
            self.asset('science')

    def asset(self, asset_type):
        size = 24
        font_size = CTkFont(size=size)
        icon_size = (size, size)

        stream = app.connect.ksp.add_stream(getattr, app.connect.ksp.space_center, asset_type)

        if asset_type == 'funds':
            asset_text = "{:,}".format(round(stream()))
        elif asset_type == 'reputation':
            asset_text = round(stream(), 2)
        elif asset_type == 'science':
            asset_text = "{:,}".format(stream())

        asset_icon = CTkImage(Image.open('icons/icon_' + asset_type + '.png'), size=icon_size)

        label = CTkLabel(
            self,
            text=asset_text,
            image=asset_icon,
            compound='left',
            font=font_size,
            padx=5,
            pady=5
        )
        label.pack(side='left', padx=10, pady=5)

        def check_asset(x):
            def check_negative():
                if x < 0:
                    label.configure(text_color='red')
                else:
                    label.configure(text_color='white')

            if asset_type == 'funds':
                label.configure(text="{:,}".format(round(stream())))
                check_negative()
            elif asset_type == 'reputation':
                label.configure(text=round(stream(), 2))
                check_negative()
            elif asset_type == 'science':
                label.configure(text="{:,}".format(stream()))
                check_negative()

        stream.add_callback(check_asset)


# handle connection errors
class ErrorHandler(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(border_color='red', border_width=2)

        self.label = CTkLabel(self, text='')
        self.label.pack(padx=10, pady=5)

        self.text = 'ERROR: Connection '

        self.pack(pady=10)

    def refused(self):
        self.label.configure(text=self.text + 'Refused')
        self.cycle(3)

    def aborted(self):
        app.connect.content.destroy()
        app.connect.pack(expand=True, fill='both')
        self.label.configure(text=self.text + 'Aborted')
        self.cycle(5)

    def cycle(self, time):
        self.update()
        sleep(time)
        self.destroy()


# main app window
class App(CTk):
    def __init__(self):
        super().__init__()
        self.window_params(800, 600)

        # create connection screen
        self.connect = Connection(self)
        self.connect.pack(expand=True, fill='both')

    def window_params(self, width, height):
        self.title(app_name)
        self.iconbitmap('icons/favicon.ico')

        self.width = width
        self.height = height
        self.minsize(width=self.width, height=self.height)

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.maxsize(width=self.screen_width, height=self.screen_height)

        self.start_x = (self.screen_width / 2) - (self.width / 2)
        self.start_y = (self.screen_height / 2) - (self.height / 2)

        self.geometry(f'{self.width}x{self.height}+{int(self.start_x)}+{int(self.start_y)}')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


app = App()
app.mainloop()