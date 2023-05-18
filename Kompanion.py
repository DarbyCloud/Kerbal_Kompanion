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

# color theme
drk_bg = "#191919"
drk_acc = "#2c2c2c"

# window
window = tk.Tk()
window.title("Kompanion")

window.rowconfigure(1, minsize=400, weight=1)
window.columnconfigure(0, minsize=600, weight=1)

style = ttk.Style()

### topbar ###

# streams
funds = conn.add_stream(getattr, conn.space_center, 'funds')
rep = conn.add_stream(getattr, conn.space_center, 'reputation')
sci = conn.add_stream(getattr, conn.space_center, 'science')

# styles
style.configure('drk_bg.TLabel', foreground='white', background='#191919')

# frames
frm_topbar = tk.Frame(
    window,
    bg=drk_bg,
    padx=10,
    pady=10
)

# labels
lbl_funds = ttk.Label(frm_topbar, text="F: " + "{:,}".format(round(funds())), style='drk_bg.TLabel')
lbl_rep = ttk.Label(frm_topbar, text=f"R: {round(rep(),1)}", style='drk_bg.TLabel')
lbl_sci = ttk.Label(frm_topbar, text="S: " + "{:,}".format(sci()), style='drk_bg.TLabel')

# geometry
lbl_funds.grid(row=0, column=0, sticky="ns", padx=5)
lbl_rep.grid(row=0, column=1, sticky="ns", padx=5)
lbl_sci.grid(row=0, column=2, sticky="ns", padx=5)

# callback functions
def check_funds(x):
    lbl_funds['text'] = "F: " + "{:,}".format(round(funds()))

def check_rep(x):
    lbl_rep['text'] = f"R: {round(rep(),1)}"

def check_sci(x):
    lbl_sci['text'] = "S: " + "{:,}".format(sci())

# callbacks
funds.add_callback(check_funds)
rep.add_callback(check_rep)
sci.add_callback(check_sci)

### main panel ###

# frame
frm_panel = tk.Frame(
    window,
    bg=drk_acc,
    padx=5,
    pady=5
)

frm_topbar.grid(row=0, column=0, sticky="nsew")
frm_panel.grid(row=1, column=0, sticky="nsew")

window.mainloop()