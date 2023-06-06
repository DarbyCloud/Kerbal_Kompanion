import customtkinter as ctk
from PIL import Image
import krpc

app_name = 'Kompanion'

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(app_name)
        self.iconbitmap('icons/favicon.ico')
        # self.minsize(width=280, height=220)
        # self.geometry('280x220')
        self.eval('tk::PlaceWindow . center')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.connection_frame = ctk.CTkFrame(self)
        self.connection_frame.grid(row=0, column=0, padx=20, pady=20)

        self.label = ctk.CTkLabel(self.connection_frame, text='Connect to KSP:')
        self.label.grid(row=0, column=0, padx=5, pady=5)

        self.input = ctk.CTkFrame(self.connection_frame, fg_color='transparent')
        self.input.columnconfigure(0, minsize=200, weight=1)
        self.input.grid(row=1, column=0, padx=20, pady=(0,10), sticky='nsew')

        self.address_entry = ctk.CTkEntry(self.input, placeholder_text='Address', justify='center')
        self.address_entry.grid(row=0, column=0, pady=(0,5), sticky='ew')
        self.address_entry.insert(0, '127.0.0.1') # localhost as default

        self.rpc_port_entry = ctk.CTkEntry(self.input, placeholder_text='RPC Port', justify='center')
        self.rpc_port_entry.grid(row=1, column=0, pady=(0,5), sticky='ew')
        self.rpc_port_entry.insert(0, '50000') # default port

        self.stream_port_entry = ctk.CTkEntry(self.input, placeholder_text='Stream Port', justify='center')
        self.stream_port_entry.grid(row=2, column=0, sticky='ew')
        self.stream_port_entry.insert(0, '50001') # default port

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

                game_mode = str(ksp.space_center.game_mode)

                self.connection_frame.grid_remove()
                self.state('zoomed')
                self.update()

                main_app = ctk.CTkFrame(self, fg_color='transparent')
                main_app.columnconfigure(0, weight=1)
                main_app.grid(row=0, column=0, sticky='nsew')
                print(game_mode)

                top_bar = ctk.CTkFrame(main_app)
                top_bar.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

                # class Main_app(ctk.CTkFrame):
                #     def __init__(self, master):
                #         super().__init__(master)

                #         self.rowconfigure(0, weight=1)
                #         self.columnconfigure(0, weight=1)
                #         self.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

                #         print(game_mode)

                # Main_app(main_app)

            except:
                self.error_label.grid(row=4, column=0)
            
        self.connect_button = ctk.CTkButton(self.input, text='Connect', command=connect)
        self.connect_button.grid(row=3, column=0, padx=10, pady=(10,5))

        self.error_label = ctk.CTkLabel(self.input, text="Can't connect to server", text_color='red')

App().mainloop()