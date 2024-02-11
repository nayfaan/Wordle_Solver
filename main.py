#!/usr/bin/env python
import tkinter as tk
import itertools


def output_area():
    frame_l = tk.Frame(master=root)
    frame_r = tk.Frame(master=root, borderwidth=2, width=5 * box_size)
    frame_r.pack_propagate(0)
    frame_l.pack(fill=tk.Y, side=tk.LEFT)
    frame_r.pack(fill=tk.Y, side=tk.LEFT, expand=True)

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
            entry_box[-1][index + 1].focus()
        except:
            pass

        entry_box[-1][index + 1].icursor(1)


def force_upper(entry_var):
    for ind, alpha in enumerate(entry_var[-1]):
        alpha.trace(
            "w",
            lambda name, index, mode, ind=ind, alpha=alpha: to_uppercase(alpha, ind),
        )


def cycle_color(i):
    color_list = [white, yellow, green]

    box_color = entry_box[-1][i]["background"]
    entry_box[-1][i]["background"] = color_list[
        (color_list.index(box_color) + 1) % len(color_list)
    ]


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
            entry_box[-1][i]["disabledforeground"] = "black"
    except:
        pass


def select_on_focus(event):
    event.widget.config(
        highlightthickness=2, highlightbackground="red", highlightcolor="red"
    )


def select_off_focus(event):
    event.widget.config(
        highlightthickness=2, highlightbackground="black", highlightcolor="black"
    )


def new_row(buttons, frame_l):
    disable_last_row()

    entry_var.append([])
    entry_box.append([])
    cycle_btn.append([])

    frame_1 = tk.Frame(
        master=frame_l, borderwidth=1, padx=box_size / 10, pady=box_size / 10
    )
    for i in range(5):
        # entry box
        entry_frame = tk.Frame(
            master=frame_1,
            relief=tk.RAISED,
            borderwidth=1,
            width=box_size,
            height=box_size,
        )
        entry_frame.pack_propagate(0)

        entry_var[-1].append(tk.StringVar(root))
        entry = tk.Entry(
            master=entry_frame,
            width=1,
            font=("Imperial", int(0.7 * box_size)),
            justify="center",
            textvariable=entry_var[len(entry_var) - 1][i],
            background=white,
            foreground="black",
            highlightthickness=2,
            highlightbackground="black",
            highlightcolor="black",
        )
        entry.bind("<FocusIn>", select_on_focus)
        entry.bind("<FocusOut>", select_off_focus)

        entry_box[-1].append(entry)

        entry.pack(fill="both", expand=True)

        entry_frame.grid(row=0, column=i)

        # cycle_button
        cycle_frame = tk.Frame(
            master=frame_1,
            relief=tk.RAISED,
            borderwidth=1,
            width=box_size,
            height=box_size / 2,
        )
        cycle_frame.pack_propagate(0)

        cycle = tk.Button(master=cycle_frame, text=">", width=1, height=1)
        cycle_btn[-1].append(cycle)
        cycle.bind("<Button-1>", lambda event, i=i: cycle_color(i))

        cycle.pack(fill="both", expand=True)
        cycle_frame.grid(row=1, column=i)
    frame_1.pack()

    force_upper(entry_var)

    (submit_btn, reset_btn) = buttons
    submit_btn.pack_forget()
    submit_btn.pack()
    reset_btn.pack_forget()
    reset_btn.pack()

    root.geometry("")
    if root.winfo_height() < min_height:
        root.geometry("614x{}".format(min_height))

    try:
        entry_box[-1][0].focus()
    except:
        pass


def wordl_logic(last_sol, last_input, last_color):
    sol_return = []

    green_list = []
    yellow_list = []
    for index, alpha in enumerate(last_input):
        if last_color[index] == yellow:
            yellow_list.append(alpha)
        elif last_color[index] == green:
            green_list.append(alpha)
            current_green[index] = alpha

    active_letters.update(green_list)
    active_letters.update(yellow_list)

    for word in last_sol:
        match = True

        for index, alpha in enumerate(last_input):
            if last_color[index] == white:
                if alpha in yellow_list or alpha in green_list:
                    alpha_repeat_count = yellow_list.count(alpha) + green_list.count(
                        alpha
                    )
                    if list(word.upper()).count(alpha) > alpha_repeat_count:
                        match = False
                elif alpha in word.upper():
                    match = False
            elif last_color[index] == yellow:
                if alpha not in word.upper():
                    match = False
                if word.upper()[index] == alpha:
                    match = False
            elif last_color[index] == green:
                if word.upper()[index] != alpha:
                    match = False

        if match:
            sol_return.append(word)

        sol_return.sort()

    return sol_return

def avoid_green(word):
    noMatch = True
    for index,alpha in enumerate(current_green):
        if word[index] == alpha:
            noMatch = False
    return noMatch



def update_recommended(analyzed):
    oustanding_alpha = []
    for alpha in list(analyzed.keys()):
        if not alpha.upper() in active_letters:
            oustanding_alpha.append(alpha)

    recommended = None
    backup_recommend = None

    if len(sol_remain) > 0 and len(sol_remain) <= 2:
        recommended = sol_remain[0]

    for i in [5, 4, 3, 2]:
        if not recommended:
            test_alpha = list(itertools.combinations(oustanding_alpha[: i + 1], i))
            for test_alpha_tuple in test_alpha:
                test_alpha_set = set(test_alpha_tuple)
                for word in all_valid:
                    word_set = set(word)
                    if test_alpha_set.issubset(word_set):
                        if avoid_green(word):
                            recommended = word
                        elif not backup_recommend:
                            backup_recommend = word

                    if recommended:
                        break
                if recommended:
                    break

    if not recommended:
        recommended = backup_recommend

    if recommended:
        recommended = recommended.upper()

    return recommended


def submit_btn_press(submit_btn, reset_btn, frame_l):
    last_input = [alpha.get() for alpha in entry_var[-1]]
    if len(list(filter(None, last_input))) == 5:
        last_color = [color["background"] for color in entry_box[-1]]

        if len(entry_box) < 11:
            new_row((submit_btn, reset_btn), frame_l)
        else:
            disable_last_row()
            submit_btn.destroy()

        global sol_remain
        sol_remain = wordl_logic(sol_remain, last_input, last_color)
        analyzed = analyze_remain(sol_remain)
        recommend = update_recommended(analyzed)
        if recommend:
            recommended_word.set("TRY: " + recommend)
            # set next row to recommend
            for index, value in enumerate(entry_box[-1]):
                value.insert(0,recommend[index])
            move_cursor_after_key(0)
        else:
            recommended_word.set("TRY: N/A")


        # display result to text box
        output_word_list_Text.delete("1.0", tk.END)
        output_word_list = "Possible words:\n\n" + ", ".join(sol_remain)
        output_word_list_Text.insert("1.0", output_word_list)

        output_frequency_analysis_label.config(text=__str_freq(analyzed))
        output_frequency_analysis_label.pack()
    
    print(current_green)


def reset_btn_press(reset_btn, frame_l):
    global sol_remain
    sol_remain = sol

    global root
    root.destroy()
    root = tk.Tk()

    init()


def analyze_remain(sol_remain_analyze):
    remain_frequency_analysis = {}
    remain_alphabets = list(set("".join(sol_remain_analyze)))
    remain_alphabets.sort()
    for alpha in remain_alphabets:
        remain_frequency_analysis[alpha] = 0
    for alpha in "".join(sol_remain_analyze):
        remain_frequency_analysis[alpha] += 1
    return dict(
        sorted(
            remain_frequency_analysis.items(), key=lambda item: item[1], reverse=True
        )
    )


def __str_freq(freq):
    s = ""
    max_val = max(freq.values())
    digit = len(str(max_val))
    for alpha, count in freq.items():
        s += alpha + ": " + str(count).rjust(digit) + ", "
    s = s[:-2]
    return s


def get_current_focus():
    current_focus = -1
    current_focus_obj = root.focus_get()
    for i, entry in enumerate(entry_box[-1]):
        if entry == current_focus_obj:
            current_focus = i

    return current_focus


def move_cursor_after_key(new_focus):
    new_focus_obj = entry_box[-1][new_focus]

    try:
        new_focus_obj.focus()
    except:
        pass

    new_focus_obj.icursor(1)


def left_key_pressed(e):
    new_focus = max(0, get_current_focus() - 1)
    move_cursor_after_key(new_focus)


def right_key_pressed(e):
    new_focus = min(4, get_current_focus() + 1)
    move_cursor_after_key(new_focus)


def init():
    global active_letters
    active_letters = set()

    global current_green
    current_green = [None, None, None, None, None]

    global entry_var
    entry_var = []
    global entry_box
    entry_box = []
    global cycle_btn
    cycle_btn = []

    main_frame = (frame_l, frame_r) = output_area()

    global recommended_word_Text
    global recommended_word
    recommended_word = tk.StringVar()
    recommended_word_Text = tk.Label(master=frame_r, textvariable=recommended_word)
    recommended_word.set("TRY: " + "SAINE")
    recommended_word_Text.pack()

    global output_word_list_Text
    output_word_list = "Possible words:\n\n" + ", ".join(sol_remain)
    output_word_list_Text = tk.Text(
        master=frame_r, width=5 * box_size
    )  # , state = "disabled")
    output_word_list_Text.insert("1.0", output_word_list)
    output_word_list_Text.pack()

    global output_frequency_analysis_label
    output_frequency_analysis_label = tk.Label(
        master=frame_r,
        wraplength=5 * box_size,
        text=__str_freq(analyze_remain(sol_remain)),
    )
    output_frequency_analysis_label.pack(fill="both", expand=True)

    submit_btn = tk.Button(master=frame_l, text="send", highlightbackground="#3E4149")
    submit_btn.bind(
        "<Button-1>",
        lambda event, submit_btn=submit_btn, frame_l=frame_l: submit_btn_press(
            submit_btn, reset_btn, frame_l
        ),
    )

    reset_btn = tk.Button(master=frame_l, text="reset", highlightbackground="#3E4149")
    reset_btn.bind(
        "<Button-1>",
        lambda event, reset_btn=reset_btn, frame_l=frame_l: reset_btn_press(
            reset_btn, frame_l
        ),
    )

    new_row((submit_btn, reset_btn), frame_l)
    for index, value in enumerate(entry_box[-1]):
                value.insert(0,"SAINE"[index])
    move_cursor_after_key(0)

    root.bind(
        "<KeyRelease-Return>",
        lambda event, submit_btn=submit_btn, frame_l=frame_l: submit_btn_press(
            submit_btn, reset_btn, frame_l
        ),
    )
    root.bind("<KeyRelease-Left>", left_key_pressed)
    root.bind("<KeyRelease-Right>", right_key_pressed)
    root.bind("<KeyRelease-BackSpace>", left_key_pressed)


def run():
    global root
    root = tk.Tk()

    init()

    tk.mainloop()


if __name__ == "__main__":
    with open("./input/possible_solutions.txt", "rt") as f:
        sol = f.read().splitlines()

    global all_valid
    with open("./input/all_allowed_sans_dupe.txt", "rt") as f:
        all_valid = f.read().splitlines()

    global sol_remain
    sol_remain = sol

    global box_size
    box_size = 60
    global white
    global yellow
    global green
    white = "white"
    yellow = "#b59f3b"
    green = "#538d4e"

    global min_height
    min_height = 410

    run()
