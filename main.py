import math
import tkinter
from tkinter import *
import csv
import datetime
import os

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
    count()  # pass total elapsed time as the starting value of counter


def count():
    global timer
    global elapsed_time
    counter = elapsed_time + 1
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
    timer = window.after(1000, count)


# ---------------------------- TAKE DOWN 2 MINUTES ------------------------------- #
def take_down_2_minuets():
    global elapsed_time
    elapsed_time -= 120


# ---------------------------- SHOW DETAILS- POPUP MASSAGE ------------------------------- #
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
    popup.geometry("400x800")
    popup.resizable(False, False)
    popup_label = tkinter.Label(popup, font=(FONT_NAME, 15, "bold"), text=file_contents)
    popup_label.pack(padx=10, pady=10)

    def average_fun():
        sum_time = 0
        counter = 0
        with open("time_records.csv", "r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] == "date":
                    continue
                existing_time_str = row[1]
                existing_hours, existing_minutes, existing_seconds = map(int, existing_time_str.split(":"))
                existing_time = existing_hours * 3600 + existing_minutes * 60 + existing_seconds
                sum_time += existing_time
                counter += 1

        # Convert new time to "HH:MM:SS" format
        hours, rem = divmod(int(sum_time/counter), 3600)
        minutes, seconds = divmod(rem, 60)
        avg_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        avg_title.config(text=f"{avg_str}", fg=DARK_GREEN)

    avg_button = Button(popup, text="average", font=(FONT_NAME, 16, "bold"), command=average_fun, highlightthickness=0)
    avg_button.pack(padx=10, pady=10)
    avg_title = Label(popup, text="", font=(FONT_NAME, 20, "bold"))
    avg_title.pack(padx=10, pady=10)

    def clear_info():
        filename = "time_records.csv"
        with open(filename, 'r+') as f:
            f.readline()  # read one line
            f.truncate(f.tell())  # terminate the file here. f.tell() returns the current position of the file pointer.
            popup.destroy()
            show_details()

    clear_title = Button(popup, text="clear all", font=(FONT_NAME, 16, "bold"), command=clear_info, highlightthickness=0)
    clear_title.pack(padx=10, pady=10)

    def keep_last_7_days():
        filename = "time_records.csv"
        history_filename = "history.csv"

        with open(filename, 'r+', newline='') as record_file, open(history_filename, 'a', newline='') as history_file:

            reader = csv.reader(record_file)
            # Skipping the header row
            header = next(reader)
            rows = list(reader)  # read all rows into a list

            rows_to_keep = []
            rows_to_move = []

            for row in reversed(rows):
                if len(rows_to_keep) <= 6:
                    rows_to_keep.append(row)
                else:
                    rows_to_move.append(row)

            with open("time_records2.csv", 'w', newline='') as updated_record:
                writer = csv.writer(updated_record)
                writer.writerow(header)
                writer.writerows(reversed(rows_to_keep))

            writer_history = csv.writer(history_file)
            writer_history.writerows(reversed(rows_to_move))  # write rows to move to the history file

        os.remove("time_records.csv")
        os.rename("time_records2.csv", "time_records.csv")
        popup.destroy()
        show_details()

    keep_7_days_button = Button(popup, text="keep last week", font=(FONT_NAME, 16, "bold"), command=keep_last_7_days, highlightthickness=0)
    keep_7_days_button.pack(padx=10, pady=10)


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
window.geometry("320x280+0+0")

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

show_details_button = Button(text="show\ndetails", font=(FONT_NAME, 16, "bold"), command=show_details, highlightthickness=0)
show_details_button.place(x=-90, y=75)

write_to_csv_button = Button(text="save", font=(FONT_NAME, 16, "bold"), command=save_to_csv, highlightthickness=0)
write_to_csv_button.place(x=-75, y=140)

take_down_button = Button(text="-2", font=(FONT_NAME, 16, "bold"), command=take_down_2_minuets, highlightthickness=0)
take_down_button.place(x=70, y=180)


window.mainloop()

