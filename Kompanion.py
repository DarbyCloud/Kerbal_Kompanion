import customtkinter as ctk
from PIL import Image
import krpc

# connection
ksp = krpc.connect(
    name='Kompanion',
    address='127.0.0.1',
    rpc_port=50000,
    stream_port=50001,
)

# game mode
gm = str(ksp.space_center.game_mode)

# colors
clr_window = '#191919'

# window
window = ctk.CTk()
window.title('Kompanion')
window_width = 500
window_height = 350
window.geometry('%dx%d+1970+-400' % (window_width, window_height))
window.configure(fg_color = (clr_window))
window.columnconfigure(0, weight=1)
window.rowconfigure(1, weight=1)

######################################## --- TOPBAR --- ########################################

frm_topbar = ctk.CTkFrame(window)
frm_topbar.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
frm_topbar.columnconfigure(0, weight=1)

### --- ASSETS WIDGET --- ###

wgt_assets = ctk.CTkFrame(frm_topbar,
    # fg_color='transparent'
    fg_color=clr_window
)

wgt_assets.grid(row=0, column=0, padx=5, pady=5, sticky='ns')
wgt_assets.columnconfigure(0, weight=1)

class asset_widget:
    def __init__(self, asset, pos):
        self.asset = asset
        self.pos = pos

        stream = ksp.add_stream(getattr, ksp.space_center, asset)
    
        if asset == 'funds':
            asset_txt = "{:,}".format(round(stream()))
        elif asset == 'reputation':
            asset_txt = round(stream(),1)
        elif asset == 'science':
            asset_txt = "{:,}".format(stream())

        asset_icn = ctk.CTkImage(Image.open('icons/icn_' + asset + '.png'), size=(18,18))

        label = ctk.CTkLabel(
            wgt_assets,
            text=asset_txt,
            image=asset_icn,
            compound='left',
            # font=18,
            padx=5,
            pady=5
        )

        label.grid(row=0, column=pos, padx=5)

        def check_asset(x):
            if asset == 'funds':
                label.configure(text="{:,}".format(round(stream())))
            elif asset == 'reputation':
                label.configure(text=round(stream(),1))
            elif asset == 'science':
                label.configure(text="{:,}".format(stream()))

        stream.add_callback(check_asset)

# set relevant game mode widgets
asset_widget('funds', 0)
asset_widget('reputation', 1)
asset_widget('science', 2)

######################################## --- MAIN PANEL --- ########################################

frm_panel = ctk.CTkFrame(window, 
    # fg_color=clr_panels
    fg_color='transparent'
)

frm_panel.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

# run gui
window.mainloop()