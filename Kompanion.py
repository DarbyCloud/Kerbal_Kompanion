import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import krpc

# connection
conn = krpc.connect(
    name="Kompanion",
    address='127.0.0.1',
    rpc_port=50000,
    stream_port=50001,
)

# get game mode
gm = str(conn.space_center.game_mode)

# window
window = tk.Tk()
window.title("Kompanion")
window.geometry('300x350+50+50')

window.rowconfigure(1, minsize=300, weight=1)
window.columnconfigure(0, minsize=250, weight=1)

# theming
style = ttk.Style()
default_font = 'TkDefaultFont'
drk_bg = "#191919"
drk_acc = "#2c2c2c"

### --- TOPBAR --- ###

# icons
icn_funds_img = ImageTk.PhotoImage(Image.open('./icons/icn_funds.png').resize((16,16)))
icn_rep_img = ImageTk.PhotoImage(Image.open('./icons/icn_rep.png').resize((16,16)))
icn_sci_img = ImageTk.PhotoImage(Image.open('./icons/icn_sci.png').resize((16,16)))

# define widgets
def wgt_funds():
    funds = conn.add_stream(getattr, conn.space_center, 'funds')

    frm_funds = tk.Frame(frm_topbar_wgt, bg=drk_bg, padx=5)
    frm_funds.grid(row=0, column=0, padx=5)

    icn_funds = tk.Label(frm_funds, image=icn_funds_img, borderwidth=0)
    icn_funds.grid(row=0, column=0)

    lbl_funds = ttk.Label(frm_funds, text="{:,}".format(round(funds())), style='topbar.TLabel')
    lbl_funds.grid(row=0, column=1, padx=2)

    def check_funds(x):
        lbl_funds['text'] = "{:,}".format(round(funds()))

    funds.add_callback(check_funds)

def wgt_reputation():
    rep = conn.add_stream(getattr, conn.space_center, 'reputation')

    frm_rep = tk.Frame(frm_topbar_wgt, bg=drk_bg)
    frm_rep.grid(row=0, column=1, padx=5)

    icn_rep = tk.Label(frm_rep, image=icn_rep_img, borderwidth=0)
    icn_rep.grid(row=0, column=0)

    lbl_rep = ttk.Label(frm_rep, text=round(rep(),1), style='topbar.TLabel')
    lbl_rep.grid(row=0, column=1, padx=5)

    def check_rep(x):
        lbl_rep['text'] = round(rep(),1)

    rep.add_callback(check_rep)

def wgt_science():
    sci = conn.add_stream(getattr, conn.space_center, 'science')

    frm_sci = tk.Frame(frm_topbar_wgt, bg=drk_bg)
    frm_sci.grid(row=0, column=2, padx=5)

    icn_sci = tk.Label(frm_sci, image=icn_sci_img, borderwidth=0)
    icn_sci.grid(row=0, column=0)

    lbl_sci = ttk.Label(frm_sci, text="{:,}".format(sci()), style='topbar.TLabel')
    lbl_sci.grid(row=0, column=3, padx=3)

    def check_sci(x):
        lbl_sci['text'] = "{:,}".format(sci())

    sci.add_callback(check_sci)

# set style
style.configure(
    'topbar.TLabel',
    foreground='white',
    background=drk_bg,
    font=(default_font, 10)
)

# add frame to window
frm_topbar = tk.Frame(
    window,
    bg=drk_bg,
    padx=8,
    pady=8,
)

frm_topbar.grid(row=0, column=0, sticky="ew")
frm_topbar.columnconfigure(0, weight=1)

# add widgets to topbar
frm_topbar_wgt = tk.Frame(
    frm_topbar,
    bg=drk_bg
)

frm_topbar_wgt.grid(row=0, column=0)

# set relevant game mode widgets
if gm == 'GameMode.career':
    wgt_funds(),
    wgt_reputation(),
    wgt_science()

elif gm == 'GameMode.science_sandbox':
    wgt_science()

### --- MAIN PANEL --- ###

# frame
frm_panel = tk.Frame(
    window,
    bg=drk_acc,
    padx=5,
    pady=5
)

frm_panel.grid(row=1, column=0, sticky="nsew")

# run gui
window.mainloop()