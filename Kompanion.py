import customtkinter as ctk
from PIL import Image
import krpc

# connection
conn = krpc.connect(
    name='Kompanion',
    address='127.0.0.1',
    rpc_port=50000,
    stream_port=50001,
)

# game mode
gm = str(conn.space_center.game_mode)

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

frm_topbar_wgt = ctk.CTkFrame(frm_topbar,
    # fg_color='transparent'
    fg_color=clr_window
)

frm_topbar_wgt.grid(row=0, column=0, padx=5, pady=5, sticky='ns')
frm_topbar_wgt.columnconfigure(0, weight=1)

asset_wgt_size = 18
asset_wgt_font = ctk.CTkFont(size=asset_wgt_size)

asset_wgt_icn_x = asset_wgt_size
asset_wgt_icn_y = asset_wgt_icn_x
asset_wgt_icn_x_y = (asset_wgt_icn_x, asset_wgt_icn_y)

asset_wgt_icn_funds = ctk.CTkImage(Image.open('icons/icn_funds.png'), size=(asset_wgt_icn_x_y))
asset_wgt_icn_rep = ctk.CTkImage(Image.open('icons/icn_rep.png'), size=(asset_wgt_icn_x_y))
asset_wgt_icn_sci = ctk.CTkImage(Image.open('icons/icn_sci.png'), size=(asset_wgt_icn_x_y))

# define widgets
def wgt_funds():
    funds = conn.add_stream(getattr, conn.space_center, 'funds')

    lbl_funds = ctk.CTkLabel(
        frm_topbar_wgt,
        text="{:,}".format(round(funds())),
        image=asset_wgt_icn_funds,
        compound='left',
        font=asset_wgt_font,
        padx=5,
        pady=5
    )

    lbl_funds.grid(row=0, column=0, padx=5)

    def check_funds(x):
        lbl_funds.configure(text="{:,}".format(round(funds())))

    funds.add_callback(check_funds)

def wgt_reputation():
    rep = conn.add_stream(getattr, conn.space_center, 'reputation')

    lbl_rep = ctk.CTkLabel(
        frm_topbar_wgt,
        text=round(rep(),1),
        image=asset_wgt_icn_rep,
        compound='left',
        font=asset_wgt_font,
        padx=5,
        pady=5
    )

    lbl_rep.grid(row=0, column=1, padx=5)

    def check_rep(x):
        lbl_rep.configure(text = round(rep(),1))

    rep.add_callback(check_rep)

def wgt_science():
    sci = conn.add_stream(getattr, conn.space_center, 'science')

    lbl_sci = ctk.CTkLabel(
        frm_topbar_wgt,
        text="{:,}".format(sci()),
        image=asset_wgt_icn_sci,
        compound='left',
        font=asset_wgt_font,
        padx=5,
        pady=5
    )

    lbl_sci.grid(row=0, column=2, padx=5)

    def check_sci(x):
        lbl_sci.configure(text = "{:,}".format(sci()))

    sci.add_callback(check_sci)

# set relevant game mode widgets
if gm == 'GameMode.career':
    wgt_funds(),
    wgt_reputation(),
    wgt_science()

elif gm == 'GameMode.science_sandbox':
    wgt_science()

######################################## --- MAIN PANEL --- ########################################

frm_panel = ctk.CTkFrame(window, 
    # fg_color=clr_panels
    fg_color='transparent'
)

frm_panel.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

# run gui
window.mainloop()