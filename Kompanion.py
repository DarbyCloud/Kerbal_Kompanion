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
            entry = CTkEntry(frame, width=250, placeholder_text=placeholder, justify='center')
            entry.pack(padx=20, pady=(0, 5))
            entry.insert(0, value)
            return entry
        
        # add frame
        frame = CTkFrame(self)
        frame.pack()

        # add label
        label = CTkLabel(frame, text='kRPC Server:')
        label.pack(pady=5)

        # add entry boxes
        global address_entry, rpc_port_entry, stream_port_entry
        address_entry = entry('Address', connection['address'])
        rpc_port_entry = entry('RPC Port', connection['rpc_port'])
        stream_port_entry = entry('Stream Port', connection['stream_port'])

        # add connect button
        connect_button = CTkButton(
            frame,
            text = 'Connect',
            text_color = 'black',
            fg_color = '#84bd08',
            hover_color = '#425e04',
            command = Connection.connect)
        connect_button.pack(pady=(5, 15))

        return frame

    def connect():
        # get entry values
        ksp_address = address_entry.get()
        ksp_rpc_port = rpc_port_entry.get()
        ksp_stream_port = stream_port_entry.get()

        # save entry values to settings.ini
        def save_connection():
            connection['address'] = ksp_address
            connection['rpc_port'] = ksp_rpc_port
            connection['stream_port'] = ksp_stream_port

            with open(config_file, 'w') as configfile:
                config.write(configfile)

            print('Settings saved')

        # monitor connection to kRPC server (runs in new thread)
        def connection_monitor():
            while True:
                try:
                    ksp.krpc.get_status().version
                    sleep(5)
                except ConnectionAbortedError:
                    app.connect.pack(expand=True, fill='both')
                    handler = AbortedErrorHandler(app.connect)
                    handler.update()
                    sleep(5)
                    handler.destroy()
                    break

        # start connection monitor in new thread
        def start_connection_monitor():
            Thread(name='connection_monitor', target=connection_monitor, daemon=True).start()

        # def get_current_scene():
        #     current_scene = str(ksp.krpc.current_game_scene)
        #     return current_scene

        # returns current game mode
        def get_game_mode():
            game_mode = str(ksp.space_center.game_mode)
            return game_mode

        ########## DEFINE WIDGETS ##########
        class AssetWidget(CTkFrame):
            def __init__(self, master):
                super().__init__(master)
                self.configure(fg_color='transparent')

                mode = get_game_mode()
                print(mode)

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

                stream = ksp.add_stream(getattr, ksp.space_center, asset_type)

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


        try:
            # establish connection to kRPC server
            ksp = krpc.connect(
                name = app_name,
                address = ksp_address,
                rpc_port = int(ksp_rpc_port),
                stream_port = int(ksp_stream_port)
            )
        except ConnectionRefusedError:
            handler = RefusedErrorHandler(app.connect)
            handler.update()
            sleep(5)
            handler.destroy()
        else:
            # save and monitor server connection
            save_connection()
            start_connection_monitor()

            # hide connection screen
            app.connect.pack_forget()

            # maximize window
            app.state('zoomed')
            app.update()

            # create main app frame where all widgets are added
            global main_frame
            main_frame = MainApp(app)
            main_frame.pack(expand=True, fill=BOTH)

            ########## ADD WIDGETS ##########

            assets = AssetWidget(main_frame.top_bar)
            assets.pack()


class RefusedErrorHandler(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(border_color='red', border_width=2)

        self.label = CTkLabel(self, text='ERROR: Connection Refused').pack(padx=10, pady=5)

        self.pack(pady=10)


class AbortedErrorHandler(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(border_color='red', border_width=2)

        self.label = CTkLabel(self, text='ERROR: Connection Aborted').pack(padx=10, pady=5)

        main_frame.destroy()
        self.pack(pady=10)

# define frame to contain widgets
class MainApp(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='transparent')

        self.top_bar = CTkFrame(self)
        self.top_bar.pack(padx=10, pady=10, fill=X)

        self.main = CTkFrame(self, fg_color='transparent')
        self.main.pack(expand=True, fill=BOTH)


# main app window
class App(CTk):
    def __init__(self):
        super().__init__()
        self.window_params()

        # connection screen
        self.connect = Connection(self)
        self.connect.pack(expand=True, fill='both')

    def window_params(self):
        self.title(app_name)
        self.iconbitmap('icons/favicon.ico')

        self.width = 450
        self.height = 600
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