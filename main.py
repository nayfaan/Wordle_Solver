import tkinter as tk

def to_uppercase(var, index):
    low_alp = "abcdefghijklmnopqrstuvwxyz"
    up_alp = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    while len(var.get()) > 0 and var.get()[-1] not in list(low_alp + up_alp):
        var.set(var.get()[:-1])
    
    try:
        var.set(var.get().upper()[-1])
    except:
        pass
    
    if var.get() not in list(up_alp):
        var.set("")
    else:
        try:
            entry_box[-1][index+1].focus()
        except:
            pass
    
def force_upper(entry_var):
    for row in entry_var:
        for ind, alpha in enumerate(row):
            alpha.trace("w", lambda name, index, mode, ind=ind, alpha=alpha: to_uppercase(alpha, ind))
            
def new_row():
    try:
        for box in entry_box[-1]:
            box_color = box['background']
            box['state'] = 'disabled'
            if box_color != "white":
                box["disabledbackground"] = box_color
            else:
                box["disabledbackground"] = "grey"
    except:
        pass
    
    entry_var.append([])
    entry_box.append([])
    
    frame_1 = tk.Frame(master = root, borderwidth = 1, padx=box_size/10, pady=box_size/10)
    for i in range(5):
        #entry box
        entry_frame = tk.Frame(master = frame_1, relief=tk.RAISED, borderwidth = 1, width=box_size, height=box_size)
        entry_frame.pack_propagate(0)
        
        entry_var[-1].append(tk.StringVar(root))
        entry = tk.Entry(master = entry_frame, width = 1, font=("Imperial", int(0.7*box_size)), justify='center', textvariable = entry_var[0][i], background = "white")
        
        entry_box[-1].append(entry)
        
        entry.pack(fill="both", expand=True)
        
        entry_frame.grid(row = 0, column = i)
        
        #cycle_button
        cycle_frame = tk.Frame(master = frame_1, relief=tk.RAISED, borderwidth = 1, width=box_size, height=box_size/3)
        cycle_frame.pack_propagate(0)
        
        cycle = tk.Button(master = cycle_frame, width = 1, height = 1)
        cycle.pack(fill="both", expand=True)
        cycle_frame.grid(row = 1, column = i)
        
    frame_1.pack()

def init():
    global entry_var
    entry_var = []
    global entry_box
    entry_box = []
    new_row()

    
    
    #submit_btn = tk.Button(text="send", highlightbackground='#3E4149').pack()

def run():
    global root
    root = tk.Tk()
    
    init()
    force_upper(entry_var)
    
    tk.mainloop()

if __name__ == "__main__":
    with open("./input/possible_solutions.txt", "rt") as f:
        sol = f.read().splitlines()
        
    global box_size
    box_size = 60
    
    run()