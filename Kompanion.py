import customtkinter as ctk
from PIL import Image
import krpc

app_name = 'Kompanion'

class Connect_KSP(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label = ctk.CTkLabel(self, text='Connect to KSP:')
        self.label.grid(row=0, column=0, padx=5, pady=5)
        
        self.input = ctk.CTkFrame(self, fg_color='transparent')
        self.input.columnconfigure(0, minsize=200, weight=1)
        self.input.grid(row=1, column=0, padx=20, pady=(0,10), sticky='nsew')

        self.host_entry = ctk.CTkEntry(self.input, placeholder_text='Address', justify='center')
        self.host_entry.grid(row=0, column=0, pady=(0,5), sticky='ew')
        self.host_entry.insert(0, '127.0.0.1') # localhost as default

        self.rpc_port_entry = ctk.CTkEntry(self.input, placeholder_text='RPC Port', justify='center')
        self.rpc_port_entry.grid(row=1, column=0, pady=(0,5), sticky='ew')
        self.rpc_port_entry.insert(0, '50000') # default port

        self.stream_port_entry = ctk.CTkEntry(self.input, placeholder_text='Stream Port', justify='center')
        self.stream_port_entry.grid(row=2, column=0, sticky='ew')
        self.stream_port_entry.insert(0, '50001') # default port

        def connect():
            ksp_host = self.host_entry.get()
            ksp_rpc_port = self.rpc_port_entry.get()
            ksp_stream_port = self.stream_port_entry.get()

            try:
                global ksp
                ksp = krpc.connect(
                    name=app_name,
                    address=ksp_host,
                    rpc_port=int(ksp_rpc_port),
                    stream_port=int(ksp_stream_port)
                )
                
                app.connect_ksp.grid_remove()
                app.main.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
                app.state('zoomed')
                app.update()

            except:
                self.error_label.grid(row=4, column=0)
            
        self.connect_button = ctk.CTkButton(self.input, text='Connect', command=connect)
        self.connect_button.grid(row=3, column=0, padx=10, pady=(10,5))

        self.error_label = ctk.CTkLabel(self.input, text="Can't connect to server", text_color='red')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(app_name)
        self.iconbitmap('icons/favicon.ico')
        self.eval('tk::PlaceWindow . center')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.connect_ksp = Connect_KSP(self)
        self.connect_ksp.grid(row=0, column=0, padx=20, pady=20)

        self.main = ctk.CTkFrame(self)
        self.main.rowconfigure(0, weight=1)
        self.main.columnconfigure(0, weight=1)

app = App()
app.mainloop()