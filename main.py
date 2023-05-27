from tkinter import *
from functions import Functions
from vars import PINK, RED, GREEN, YELLOW, DARK_GREEN, PURPLE, BLUE, FONT_NAME

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Time management ")
window.config(padx=100, pady=50, bg=YELLOW)
window.geometry("320x280+0+0")
fun = Functions()

# ---------- TOTAL ----------------
total_title = Label(text="Total", font=(FONT_NAME, 20, "bold"), bg=YELLOW)
total_title.place(x=-75, y=-20)


total_timer = Label(text="00:00", font=(FONT_NAME, 20, "bold"), bg=YELLOW)
total_timer.place(x=-75, y=10)


# ---------- CURRENT TIMER ----------------
curr_title = Label(text="Timer", font=(FONT_NAME, 30, "bold"), fg=DARK_GREEN, bg=YELLOW)
curr_title.place(x=30, y=-40)


curr_timer = Label(text="00:00", font=(FONT_NAME, 30, "bold"), fg=BLUE, bg=YELLOW)
curr_timer.place(x=30, y=10)


# ----------BUTTONS----------------
run_button = Button(text="Start", font=(FONT_NAME, 16, "bold"), command=lambda: fun.run_button(curr_title, curr_timer, window), highlightthickness=0)
run_button.place(x=55, y=60)


stop_button = Button(text="Stop", font=(FONT_NAME, 16, "bold"), command=lambda: fun.stop_button(window, curr_timer, curr_title, total_timer), highlightthickness=0)
stop_button.place(x=60, y=100)


pause_button = Button(text="Pause", font=(FONT_NAME, 16, "bold"), command=lambda: fun.pause_button(curr_title, window), highlightthickness=0)
pause_button.place(x=55, y=140)

show_details_button = Button(text="show\ndetails", font=(FONT_NAME, 16, "bold"), command=fun.show_details, highlightthickness=0)
show_details_button.place(x=-90, y=75)

write_to_csv_button = Button(text="save", font=(FONT_NAME, 16, "bold"), command=lambda: fun.save_to_csv(total_timer), highlightthickness=0)
write_to_csv_button.place(x=-75, y=140)

take_down_button = Button(text="-2", font=(FONT_NAME, 16, "bold"), command=fun.take_down_2_minuets, highlightthickness=0)
take_down_button.place(x=70, y=180)


# ------------ KEY PANELS------------ #
window.bind('<space>', lambda event, curr_title = curr_title, curr_timer = curr_timer, window=window: fun.on_space_key(event, curr_title, curr_timer, window))

window.bind('s', lambda event, total_timer = total_timer: fun.on_s_key(event, total_timer))

window.bind('x', lambda event, window = window, curr_timer=curr_timer, curr_title=curr_title, total_timer=total_timer : fun.on_x_key(event, window, curr_timer, curr_title, total_timer))

window.bind('<Escape>', lambda event, window = window : fun.on_Escape_key(event, window))


window.mainloop()

