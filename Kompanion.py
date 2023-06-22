from customtkinter import *
from PIL import Image
from threading import Thread
from time import sleep
from configparser import ConfigParser
import krpc

app_name = 'Kompanion'

config = ConfigParser()
config_file = 'settings.ini'
config.read(config_file)

class App(CTk):
    def __init__(self):
        super().__init__()
        self.window_params()

        startup_screen(self)

        # run
        self.mainloop()

    def window_params(self):
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
        self.rowconfigure(0, weight=1)

class startup_screen(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color = 'transparent')

        # add logo
        self.image = CTkImage(Image.open('icons/logo.png'), size = (260,260))
        self.image_label = CTkLabel(self, image = self.image, text = '').pack(pady = (50,0))

        # add input
        self.input(self).pack()

        self.pack(expand = True, fill = 'both')
        # self.grid(row = 0, column = 0, sticky = 'nsew')

    class input(CTkFrame):
        def __init__(self, master):
            super().__init__(master)

            # add label
            CTkLabel(self, text = 'kRPC Server:').pack(pady = 5)

            # get connection settings
            self.connection = config['connection']

            # add entry boxes
            self.address_entry = self.entry('Address', self.connection['address'])
            self.rpc_port_entry = self.entry('RPC Port', self.connection['rpc_port'])
            self.stream_port_entry = self.entry('Stream Port', self.connection['stream_port'])

            # add connect button
            def connect_button():
                ksp_address = self.address_entry.get()
                ksp_rpc_port = self.rpc_port_entry.get()
                ksp_stream_port = self.stream_port_entry.get()

                def handle_error():
                    self.error_label.configure(text = 'ERROR: Connection refused')
                    self.error_label.pack()

                def save_connection():
                    conn = config['connection']
                    conn['address'] = ksp_address
                    conn['rpc_port'] = ksp_rpc_port
                    conn['stream_port'] = ksp_stream_port

                    with open(config_file, 'w') as configfile:
                        config.write(configfile)

                    print('Settings saved')

                try:
                    ksp = krpc.connect(
                        name=app_name,
                        address=ksp_address,
                        rpc_port=int(ksp_rpc_port),
                        stream_port=int(ksp_stream_port)
                    )
                except ConnectionRefusedError:
                    handle_error()
                else:
                    save_connection()

            self.button = CTkButton(self,
                text = 'Connect',
                text_color='black',
                fg_color='#84bd08',
                hover_color='#425e04',
                command = connect_button).pack(pady = (5,20))
            
            # add error label            
            self.error_label = CTkLabel(self, text_color = 'red', text = '')

        def entry(self, placeholder, value):
            entry = CTkEntry(self, width = 250, placeholder_text = placeholder, justify = 'center')
            entry.pack(padx = 20, pady = (0,5))
            entry.insert(0, value)
            return entry

class main_screen(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color = 'green')

        CTkLabel(self, text='Main Screen').pack()

        self.pack(expand = True, fill = 'both')
        # self.grid(row = 0, column = 0, sticky = 'nsew')

App()