# from tkinter import *
import customtkinter as ctk
from PIL import Image
import krpc

class connect_ksp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Kompanion - Connect')
        self.resizable(False, False)
        self.columnconfigure(0, minsize=300)
        self.eval('tk::PlaceWindow . center')

        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
        frame.columnconfigure(0, weight=1)

        host_frame = ctk.CTkFrame(frame, fg_color='transparent')
        host_frame.grid(row=0, column=0, padx=10, pady=(10,0), sticky='ew')
        host_frame.columnconfigure(0, weight=1)

        host_input_frame = ctk.CTkFrame(host_frame, fg_color='transparent')

        def host_dropdown_callback(choice):
            if choice == 'Localhost':
                host = '127.0.0.1'
                host_input_frame.grid_remove()
            elif choice == 'LAN/WAN':
                host_input_frame.grid(row=1, column=0, padx=5, sticky='ew')
                host_input_frame.columnconfigure(0, weight=1)

                host_entry = ctk.CTkEntry(host_input_frame, placeholder_text='Address', justify='center')
                host_entry.grid(row=0, column=0, pady=(0,5), sticky='ew')

                subnet_entry = ctk.CTkEntry(host_input_frame, placeholder_text='Subnet', justify='center')
                subnet_entry.grid(row=1, column=0, pady=(0,5), sticky='ew')

        host_dropdown = ctk.CTkOptionMenu(host_frame, values=['Localhost', 'LAN/WAN'], anchor='center', command=host_dropdown_callback)
        host_dropdown.grid(row=0, column=0, pady=(0,5), sticky='ew')

        port_frame = ctk.CTkFrame(frame, fg_color='transparent')
        port_frame.grid(row=1, column=0, padx=10, pady=(0,5), sticky='ew')
        port_frame.columnconfigure(0, weight=1)

        port_input_frame = ctk.CTkFrame(port_frame, fg_color='transparent')

        def port_dropdown_callback(choice):
            if choice == 'Default Ports':
                rpc_port = 50000
                stream_port = 50001
                port_input_frame.grid_remove()
            elif choice == 'Custom Ports':
                port_input_frame.grid(row=1, column=0, padx=5, sticky='ew')
                port_input_frame.columnconfigure(0, weight=1)

                rpc_port_entry = ctk.CTkEntry(port_input_frame, placeholder_text='RPC Port', justify='center')
                rpc_port_entry.grid(row=0, column=0, pady=(0,5), sticky='ew')

                ent_port_stream = ctk.CTkEntry(port_input_frame, placeholder_text='Stream Port', justify='center')
                ent_port_stream.grid(row=1, column=0, pady=(0,5), sticky='ew')

        ports_dropdown = ctk.CTkOptionMenu(port_frame, values=['Default Ports', 'Custom Ports'], anchor='center', command=port_dropdown_callback)
        ports_dropdown.grid(row=0, column=0, pady=(0,5), sticky='ew')

        btn_connect = ctk.CTkButton(frame, text='Connect')
        btn_connect.grid(row=2, column=0, pady=(0,10))

        # # connection
        # ksp = krpc.connect(
        #     name='Kompanion',
        #     address=host,
        #     rpc_port=50000,
        #     stream_port=50001,
        # )

# # game mode
# gm = str(ksp.space_center.game_mode)

# run
connection = connect_ksp()
connection.mainloop()
# app = app()
# app.mainloop()