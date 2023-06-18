import customtkinter as ctk
from PIL import Image
import krpc

app_name = 'Kompanion'

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(app_name)
        self.iconbitmap('icons/favicon.ico')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()-80
        self.geometry(f'{screen_width}x{screen_height}+0+0')
        self.minsize(width=screen_width, height=screen_height)
        self.maxsize(width=screen_width, height=screen_height+80)
        self.state('zoomed')
        self.update()

        # self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.image = ctk.CTkImage(Image.open('icons/Kompanion_logo.png'), size=(260,260))
        self.image_label = ctk.CTkLabel(self, image=self.image, text='')
        self.image_label.grid(row=0, column=0, pady=(100,0))

        self.connection_frame = ctk.CTkFrame(self)
        self.connection_frame.grid(row=1, column=0, padx=20, pady=20)

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

            except:
                self.error_label.grid(row=4, column=0)

            else:
                game_mode = str(ksp.space_center.game_mode)

                self.connection_frame.grid_remove()

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

        self.connect_button = ctk.CTkButton(self.input, text='Connect', command=connect)
        self.connect_button.grid(row=3, column=0, padx=10, pady=(10,5))

        self.error_label = ctk.CTkLabel(self.input, text="Can't connect to server", text_color='red')

App().mainloop()