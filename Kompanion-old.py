import customtkinter as ctk
from PIL import Image
import threading
from time import sleep
import krpc
from configparser import ConfigParser

app_name = 'Kompanion'

config = ConfigParser()
config_file = 'settings.ini'
config.read(config_file)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(app_name)
        self.iconbitmap('icons/favicon.ico')

        self.width = 450
        self.height = 600
        self.minsize(width=self.width, height=self.height)

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.maxsize(width=self.screen_width, height=self.screen_height)

        self.start_x = (self.screen_width/2) - (self.width/2)
        self.start_y = (self.screen_height/2) - (self.height/2)

        self.geometry(f'{self.width}x{self.height}+{int(self.start_x)}+{int(self.start_y)}')

        self.columnconfigure(0, weight=1)

        self.connection_screen = ctk.CTkFrame(self, fg_color='transparent')
        self.connection_screen.columnconfigure(0, weight=1)
        self.connection_screen.grid(row=0, column=0, sticky='nsew')

        self.image = ctk.CTkImage(Image.open('icons/logo.png'), size=(260,260))
        self.image_label = ctk.CTkLabel(self.connection_screen, image=self.image, text='')
        self.image_label.grid(row=0, column=0, pady=(50,0))

        self.connection_frame = ctk.CTkFrame(self.connection_screen)
        self.connection_frame.grid(row=1, column=0, padx=20, pady=20)

        self.label = ctk.CTkLabel(self.connection_frame, text='Connect to KSP:')
        self.label.grid(row=0, column=0, padx=5, pady=5)

        self.input = ctk.CTkFrame(self.connection_frame, fg_color='transparent')
        self.input.columnconfigure(0, minsize=200, weight=1)
        self.input.grid(row=1, column=0, padx=20, pady=(0,10), sticky='nsew')

        self.address_entry = ctk.CTkEntry(self.input, placeholder_text='Address', justify='center')
        self.address_entry.grid(row=0, column=0, pady=(0,5), sticky='ew')
        self.address_entry.insert(0, config['connection']['address']) # localhost as default

        self.rpc_port_entry = ctk.CTkEntry(self.input, placeholder_text='RPC Port', justify='center')
        self.rpc_port_entry.grid(row=1, column=0, pady=(0,5), sticky='ew')
        self.rpc_port_entry.insert(0, config['connection']['rpc_port']) # default port

        self.stream_port_entry = ctk.CTkEntry(self.input, placeholder_text='Stream Port', justify='center')
        self.stream_port_entry.grid(row=2, column=0, sticky='ew')
        self.stream_port_entry.insert(0, config['connection']['stream_port']) # default port

        def connect():
            ksp_host = self.address_entry.get()
            ksp_rpc_port = self.rpc_port_entry.get()
            ksp_stream_port = self.stream_port_entry.get()

            try:
                ksp = krpc.connect(
                    name=app_name,
                    address=ksp_host,
                    rpc_port=int(ksp_rpc_port),
                    stream_port=int(ksp_stream_port)
                )

            except:
                self.error_label.grid(row=4, column=0)

            else:
                def save_connection():
                    conn = config['connection']
                    conn['address'] = ksp_host
                    conn['rpc_port'] = ksp_rpc_port
                    conn['stream_port'] = ksp_stream_port

                    with open(config_file, 'w') as configfile:
                        config.write(configfile)

                save_connection()

                self.state('zoomed')
                self.update()

                game_mode = str(ksp.space_center.game_mode)

                self.connection_screen.grid_remove()

                main_app = ctk.CTkFrame(self, fg_color='transparent')
                main_app.columnconfigure(0, weight=1)
                main_app.grid(row=0, column=0, sticky='nsew')

                top_bar = ctk.CTkFrame(main_app)
                top_bar.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

                ########## --- ASSETS WIDGET --- ##########
                asset_widget = ctk.CTkFrame(top_bar, fg_color='transparent')
                asset_widget.pack(pady=5)

                def asset(asset_type):
                    size = 24
                    font_size = ctk.CTkFont(size=size)
                    icon_size = (size,size)

                    stream = ksp.add_stream(getattr, ksp.space_center, asset_type)

                    if asset_type == 'funds':
                        asset_text = "{:,}".format(round(stream()))
                    elif asset_type == 'reputation':
                        asset_text = round(stream(),2)
                    elif asset_type == 'science':
                        asset_text = "{:,}".format(stream())

                    asset_icon = ctk.CTkImage(Image.open('icons/icon_' + asset_type + '.png'), size=icon_size)

                    label = ctk.CTkLabel(
                        asset_widget,
                        text=asset_text,
                        image=asset_icon,
                        compound='left',
                        font=font_size,
                        padx=5,
                        pady=5
                    )

                    label.pack(side='left', padx=10)

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
                            label.configure(text=round(stream(),2))
                            check_negative()
                        elif asset_type == 'science':
                            label.configure(text="{:,}".format(stream()))
                            check_negative()

                    stream.add_callback(check_asset)

                if game_mode == 'GameMode.career':
                    career_assets = ['funds', 'reputation', 'science']
                    for i in career_assets:
                        asset(i)
                elif game_mode == 'GameMode.science_sandbox':
                    asset('science')
                ##########

                def check_connection():
                    while True:
                        try:
                            ksp.krpc.get_status().version
                            sleep(5)

                        except:
                            main_app.grid_remove()
                            self.connection_screen.grid(row=0, column=0, sticky='nsew')
                            self.error_label.configure(text='Lost connection to server')
                            sleep(5)
                            self.error_label.grid_remove()
                            break

                con = threading.Thread(name='check_connection', target=check_connection)
                con.daemon = True
                con.start()

        self.connect_button = ctk.CTkButton(self.input, text='Connect', command=connect)
        self.connect_button.grid(row=3, column=0, padx=10, pady=(10,5))

        self.error_label = ctk.CTkLabel(self.input, text="Can't connect to server", text_color='red')

App().mainloop()