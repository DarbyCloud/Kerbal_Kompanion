from customtkinter import *
from PIL import Image
from threading import Thread
from time import sleep
from configparser import ConfigParser
import krpc

app_name = 'Kerbal Kompanion'

config = ConfigParser()
config_file = 'settings.ini'
config.read(config_file)
connection = config['connection']

class ConnectWidget(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color = 'transparent')

        # add logo
        self.image = CTkImage(Image.open('icons/logo.png'), size = (260, 260))
        self.image_label = CTkLabel(self, image = self.image, text = '').pack(pady = (50, 0))

        # add input
        self.input()

    # construct and return frame with entries and button
    def input(self):
        def entry(placeholder, value):
            entry = CTkEntry(frame, width = 250, placeholder_text = placeholder, justify = 'center')
            entry.pack(padx = 20, pady = (0, 5))
            entry.insert(0, value)
            return entry
        
        # add frame
        frame = CTkFrame(self)
        frame.pack()

        # add label
        label = CTkLabel(frame, text = 'kRPC Server:')
        label.pack(pady = 5)

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
            command = ConnectWidget.connect)
        connect_button.pack(pady = (5, 15))

        return frame

    def connect():
        # get entry values
        ksp_address = address_entry.get()
        ksp_rpc_port =  rpc_port_entry.get()
        ksp_stream_port =  stream_port_entry.get()

        # save entry values to setting file
        def save_connection():
            # connection['address'] = ksp_address
            connection['address'] = ksp_address
            connection['rpc_port'] = ksp_rpc_port
            connection['stream_port'] = ksp_stream_port

            with open(config_file, 'w') as configfile:
                config.write(configfile)

            print('Settings saved')

        # monitor connection to kRPC server
        def connection_monitor():
            while True:
                try:
                    ksp.krpc.get_status().version
                    sleep(5)
                except ConnectionAbortedError:
                    connect.pack(expand = True, fill = 'both')
                    eh = ErrorHandler(connect)
                    eh.pack(pady = 5)
                    break

        # create new thread and run connection monitor
        def connection_monitor_thread():
            connection = Thread(name='connection_monitor', target=connection_monitor)
            connection.daemon = True
            connection.start()

        try:
            ksp = krpc.connect(
                name = app_name,
                address = ksp_address,
                rpc_port = int(ksp_rpc_port),
                stream_port = int(ksp_stream_port)
            )
        except ConnectionRefusedError:
            global refused_error
            refused_error = ErrorHandler(connect)
            refused_error.pack(pady = 5)
        else:
            save_connection()
            connection_monitor_thread()
            connect.pack_forget()


class ErrorHandler(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(border_color = 'red', border_width = 2)
        self.label = CTkLabel(self, text = 'ERROR: Connection Refused').pack(padx = 10, pady = 5)


class App(CTk):
    def __init__(self):
        super().__init__()
        self.window_params()

        # connection screen
        global connect
        connect = ConnectWidget(self)
        connect.pack(expand = True, fill = 'both')

        # run
        self.mainloop()

    def window_params(self):
        self.title(app_name)
        self.iconbitmap('icons/favicon.ico')

        self.width = 450
        self.height = 600
        self.minsize(width = self.width, height = self.height)

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.maxsize(width = self.screen_width, height = self.screen_height)

        self.start_x = (self.screen_width/2) - (self.width/2)
        self.start_y = (self.screen_height/2) - (self.height/2)

        self.geometry(f'{self.width}x{self.height}+{int(self.start_x)}+{int(self.start_y)}')

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)


App()