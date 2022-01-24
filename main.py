import tkinter as tk

def output_area():
    frame_l = tk.Frame(master = root)
    frame_r = tk.Frame(master = root, borderwidth = 2, width = 5*box_size)
    frame_r.pack_propagate(0)
    frame_l.pack(fill=tk.Y, side=tk.LEFT)
    frame_r.pack(fill=tk.Y, side=tk.LEFT)
    
    return (frame_l, frame_r)

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
            
            
def cycle_color(i):
    color_list = [white, yellow, green]
    
    box_color = entry_box[-1][i]["background"]
    entry_box[-1][i]["background"] = color_list[(color_list.index(box_color) + 1) % len(color_list)]

def disable_last_row():
    try:
        for i in range(5):
            box_color = entry_box[-1][i]["background"]
            
            cycle_btn[-1][i].master.destroy()
            
            entry_box[-1][i]["state"] = "disabled"
            if box_color != white:
                entry_box[-1][i]["disabledbackground"] = box_color
            else:
                entry_box[-1][i]["disabledbackground"] = "grey"
    except:
        pass

def new_row(submit_btn, frame_l):
    disable_last_row()
    
    entry_var.append([])
    entry_box.append([])
    cycle_btn.append([])
    
    frame_1 = tk.Frame(master = frame_l, borderwidth = 1, padx=box_size/10, pady=box_size/10)
    for i in range(5):
        #entry box
        entry_frame = tk.Frame(master = frame_1, relief=tk.RAISED, borderwidth = 1, width=box_size, height=box_size)
        entry_frame.pack_propagate(0)
        
        entry_var[-1].append(tk.StringVar(root))
        entry = tk.Entry(master = entry_frame,
                         width = 1,
                         font=("Imperial", int(0.7*box_size)),
                         justify='center',
                         textvariable = entry_var[len(entry_var)-1][i],
                         background = white)
        
        entry_box[-1].append(entry)
        
        entry.pack(fill="both", expand=True)
        
        entry_frame.grid(row = 0, column = i)
        
        #cycle_button
        cycle_frame = tk.Frame(master = frame_1, relief=tk.RAISED, borderwidth = 1, width=box_size, height=box_size/3)
        cycle_frame.pack_propagate(0)
        
        cycle = tk.Button(master = cycle_frame, width = 1, height = 1)
        cycle_btn[-1].append(cycle)
        cycle.bind("<Button-1>", lambda event, i=i: cycle_color(i))
        
        cycle.pack(fill="both", expand=True)
        cycle_frame.grid(row = 1, column = i)
    frame_1.pack()
    
    submit_btn.pack_forget()
    submit_btn.pack()
    
def submit_btn_press(submit_btn, frame_l):
    if len(entry_box) < 6:
        new_row(submit_btn, frame_l)
    else:
        disable_last_row()
        submit_btn.destroy()

def init():
    global entry_var
    entry_var = []
    global entry_box
    entry_box = []
    global cycle_btn
    cycle_btn = []
    
    main_frame = (frame_l, frame_r) = output_area()
    
    submit_btn = tk.Button(master = frame_l, text="send", highlightbackground='#3E4149')
    submit_btn.bind("<Button-1>", lambda event, submit_btn=submit_btn, frame_l=frame_l: submit_btn_press(submit_btn, frame_l))
    
    output_word_list = "Possible words:\n\n" + ", ".join(sol)
    output_word_list_label = tk.Text(master = frame_r, width = 5*box_size)#, state = "disabled")
    output_word_list_label.insert("1.0", output_word_list)
    output_word_list_label.pack()
    
    new_row(submit_btn, frame_l)

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
    global white
    global yellow
    global green
    white = "white"
    yellow = "#b59f3b"
    green = "#538d4e"
    
    run()