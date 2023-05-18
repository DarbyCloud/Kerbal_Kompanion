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

# frames
frm_topbar = tk.Frame(
    window,
    bg=drk_bg,
    padx=10,
    pady=10
)

frm_panel = tk.Frame(
    window,
    bg=drk_acc,
    padx=5,
    pady=5
)

# streams
funds = conn.add_stream(getattr, conn.space_center, 'funds')
rep = conn.add_stream(getattr, conn.space_center, 'reputation')
sci = conn.add_stream(getattr, conn.space_center, 'science')

# labels
lbl_funds = ttk.Label(frm_topbar, text="F: " + "{:,}".format(round(funds())), foreground="white", background=drk_bg)
lbl_rep = ttk.Label(frm_topbar, text=f"R: {round(rep(),1)}", foreground="white", background=drk_bg)
lbl_sci = ttk.Label(frm_topbar, text="S: " + "{:,}".format(sci()), foreground="white", background=drk_bg)

# geometry
lbl_funds.grid(row=0, column=0, sticky="ns", padx=5)
lbl_rep.grid(row=0, column=1, sticky="ns", padx=5)
lbl_sci.grid(row=0, column=2, sticky="ns", padx=5)

frm_topbar.grid(row=0, column=0, sticky="nsew")
frm_panel.grid(row=1, column=0, sticky="nsew")

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

window.mainloop()