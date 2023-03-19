import math
import tkinter
from tkinter import *
import csv
import datetime

import pandas

# ---------------------------- CONSTANTS ------------------------------- #

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
DARK_GREEN = "#68b38a"
PURPLE = "#a05eb5"
BLUE = "#5e8eb5"
FONT_NAME = "Courier"
timer = None
elapsed_time = 0
total_time = 0


# ---------------------------- TIMER RESET ------------------------------- #
def stop_button():
    global timer
    global elapsed_time
    global total_time
    total_time += elapsed_time
    elapsed_time = 0  # reset total elapsed time to zero

    window.after_cancel(timer)
    curr_timer.config(text="00:00")
    curr_title.config(text="Stopped", fg=DARK_GREEN)

    total_minutes = total_time // 60
    total_seconds = total_time % 60
    total_timer.config(text=f"{total_minutes:02d}:{total_seconds:02d}")


# ---------------------------- TIMER PAUSE ------------------------------- #
def pause_button():
    global timer
    curr_title.config(text="Paused", fg=DARK_GREEN)
    window.after_cancel(timer)


# ---------------------------- TIMER RUN ------------------------------- #
def run_button():
    curr_title.config(text="Running", fg=DARK_GREEN)
    global elapsed_time
    count(elapsed_time)  # pass total elapsed time as the starting value of counter


def count(counter):
    global timer
    global elapsed_time
    minutes = math.floor(counter/60)
    seconds = counter % 60
    min_text = ""
    seconds_text = ""
    if seconds < 10:
        seconds_text = "0"+str(seconds)
    else:
        seconds_text = str(seconds)
    if minutes < 10:
        min_text = "0"+str(minutes)
    else:
        min_text = str(minutes)

    elapsed_time = counter
    curr_timer.config(text=f"{min_text}:{seconds_text}")
    timer = window.after(1000, count, counter+1)


# ---------------------------- SHOW DETAILS ------------------------------- #
def show_details():
    # Read the contents of the CSV file and format as a table
    with open("time_records.csv", "r") as file:
        csv_reader = csv.reader(file)
        d = "date"
        t = "learning time"
        file_contents = f"{d:<15} {t:<15}\n"
        for row in csv_reader:
            if row[0] == "date":
                continue
            file_contents += f"{row[0]:<15} {row[1]:<15}\n"

    popup = tkinter.Toplevel()
    popup.title("Message")
    popup.geometry("400x400")
    popup.resizable(False, False)
    popup_label = tkinter.Label(popup, font=(FONT_NAME, 15, "bold"), text=file_contents)
    popup_label.pack(padx=10, pady=10)
    ok_button = tkinter.Button(popup, text="OK", command=popup.destroy)
    ok_button.pack(pady=10)


# ---------------------------- SAVE TO CSV ------------------------------- #
def save_to_csv():
    global total_time
    today = datetime.date.today()
    data = pandas.read_csv("time_records.csv")

    # Find the row index where the date column matches today's date
    today_index = data[data["date"] == str(today)].index
    if not today_index.empty:
        # Convert existing time to seconds
        existing_time_str = data.loc[today_index, "timeClockRun"].item()
        existing_hours, existing_minutes, existing_seconds = map(int, existing_time_str.split(":"))
        existing_time = existing_hours * 3600 + existing_minutes * 60 + existing_seconds

        # Add total_time to existing time
        new_time = existing_time + total_time

        # Convert new time to "HH:MM:SS" format
        hours, rem = divmod(new_time, 3600)
        minutes, seconds = divmod(rem, 60)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        # Update timeClockRun column with new time
        data.loc[today_index, "timeClockRun"] = time_str
    else:
        # Convert total_time from seconds to "HH:MM:SS" format
        hours, rem = divmod(total_time, 3600)
        minutes, seconds = divmod(rem, 60)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        new_row = {'date': today, 'timeClockRun': time_str}
        data = pandas.concat([data, pandas.DataFrame([new_row])], ignore_index=True)

    data.to_csv('time_records.csv', index=False)
    total_time = 0
    total_timer.config(text="00:00")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Time management ")
window.config(padx=100, pady=50, bg=YELLOW)
window.geometry("320x250+0+0")

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
run_button = Button(text="Start", font=(FONT_NAME, 16, "bold"), command=run_button, highlightthickness=0)
run_button.place(x=55, y=60)


stop_button = Button(text="Stop", font=(FONT_NAME, 16, "bold"), command=stop_button, highlightthickness=0)
stop_button.place(x=60, y=100)


pause_button = Button(text="Pause", font=(FONT_NAME, 16, "bold"), command=pause_button, highlightthickness=0)
pause_button.place(x=55, y=140)


write_to_csv_button = Button(text="save", font=(FONT_NAME, 16, "bold"), command=save_to_csv, highlightthickness=0)
write_to_csv_button.place(x=-75, y=140)

show_details_button = Button(text="show\ndetails", font=(FONT_NAME, 16, "bold"), command=show_details, highlightthickness=0)
show_details_button.place(x=-90, y=75)

window.mainloop()

