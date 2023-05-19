import tkinter as tk
import tkinter.ttk as ttk
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

window.rowconfigure(1, minsize=400, weight=1)
window.columnconfigure(0, minsize=600, weight=1)

# theming
style = ttk.Style()
drk_bg = "#191919"
drk_acc = "#2c2c2c"

### --- TOPBAR --- ###

# define widgets
def wgt_funds():
    funds = conn.add_stream(getattr, conn.space_center, 'funds')
    lbl_funds = ttk.Label(frm_topbar, text="F: " + "{:,}".format(round(funds())), style='topbar.TLabel')
    lbl_funds.grid(row=0, column=1, sticky="ns", padx=5)

    def check_funds(x):
        lbl_funds['text'] = "F: " + "{:,}".format(round(funds()))

    funds.add_callback(check_funds)

def wgt_reputation():
    rep = conn.add_stream(getattr, conn.space_center, 'reputation')
    lbl_rep = ttk.Label(frm_topbar, text=f"R: {round(rep(),1)}", style='topbar.TLabel')
    lbl_rep.grid(row=0, column=2, sticky="ns", padx=5)

    def check_rep(x):
        lbl_rep['text'] = f"R: {round(rep(),1)}"

    rep.add_callback(check_rep)

def wgt_science():
    sci = conn.add_stream(getattr, conn.space_center, 'science')
    lbl_sci = ttk.Label(frm_topbar, text="S: " + "{:,}".format(sci()), style='topbar.TLabel')
    lbl_sci.grid(row=0, column=3, sticky="ns", padx=5)

    def check_sci(x):
        lbl_sci['text'] = "S: " + "{:,}".format(sci())

    sci.add_callback(check_sci)

# set style
style.configure('topbar.TLabel', foreground='white', background=drk_bg, padx=10, pady=10)

# add frame
frm_topbar = tk.Frame(
    window,
    bg=drk_bg,
    padx=10,
    pady=10
)

frm_topbar.grid(row=0, column=0, sticky="nsew")

# add mode label
lbl_game_mode = ttk.Label(frm_topbar, text="", style='topbar.TLabel')
lbl_game_mode.grid(row=0, column=0, sticky="ns", padx=5)

# set relevant game mode widgets
if gm == 'GameMode.career':
    lbl_game_mode['text'] = 'Career'
    wgt_funds(),
    wgt_reputation(),
    wgt_science()

elif gm == 'GameMode.science_sandbox':
    lbl_game_mode['text'] = 'Science'
    wgt_science()

elif gm == 'GameMode.sandbox':
    lbl_game_mode['text'] = 'Sandbox'

else: lbl_game_mode['text'] = gm

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