import math
from tkinter import *
import csv
import datetime

import pandas

# ---------------------------- CONSTANTS ------------------------------- #

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
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
    curr_title.config(text="Stopped", fg=GREEN)

    total_minutes = total_time // 60
    total_seconds = total_time % 60
    total_timer.config(text=f"{total_minutes:02d}:{total_seconds:02d}")


# ---------------------------- TIMER PAUSE ------------------------------- #
def pause_button():
    global timer
    curr_title.config(text="paused", fg=GREEN)
    window.after_cancel(timer)


# ---------------------------- TIMER RUN ------------------------------- #
def run_button():
    curr_title.config(text="running", fg=GREEN)
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


# ---------------------------- SAVE TO CSV ------------------------------- #\

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


# def save_to_csv():
#     global total_time
#     today = datetime.date.today()
#
#     # Check if today's date already exists in the file
#     existing_data = None
#     with open('time_records.csv', mode='r') as csv_file:
#         csv_reader = csv.reader(csv_file)
#         for row in csv_reader:
#             if row[0] == str(today):
#                 existing_data = row
#                 break
#         csv_file.seek(0)
#
#     # If today's date already exists, update the time
#     if existing_data:
#         total_time += int(existing_data[1])
#         with open('time_records.csv', mode='w', newline='') as csv_file:
#             writer = csv.writer(csv_file)
#             for row in csv.reader(open('time_records.csv', 'r')):
#                 if row[0] == str(today):
#                     writer.writerow([str(today), total_time])
#                 else:
#                     writer.writerow(row)
#             csv_file.seek(0)
#
#     # If today's date doesn't exist, add a new row
#     else:
#         with open('time_records.csv', mode='a', newline='') as csv_file:
#             writer = csv.writer(csv_file)
#             writer.writerow([str(today), total_time])
#
#     total_time = 0
#     total_timer.config(text="00:00")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Time management ")
window.config(padx=100, pady=50, bg=YELLOW)


# ---------- TOTAL ----------------
total_title = Label(text="Total", font=(FONT_NAME, 20, "bold"), bg=YELLOW)
total_title.grid(row=0, column=0)

total_timer = Label(text="00:00", font=(FONT_NAME, 20, "bold"), bg=YELLOW)
total_timer.grid(row=1, column=0)


# # ---------- JUST FOR GAPS ----------------
# title_label_4 = Label(text="          ", font=(FONT_NAME, 20, "bold"), bg=YELLOW)
# title_label_4.grid(row=0, column=1)
#
# title_label_5 = Label(text="          ", font=(FONT_NAME, 20, "bold"), bg=YELLOW)
# title_label_5.grid(row=1, column=1)
#
# title_label_5 = Label(text="          ", font=(FONT_NAME, 20, "bold"), bg=YELLOW)
# title_label_5.grid(row=1, column=1)


# ---------- CURRENT TIMER ----------------
curr_title = Label(text="Timer", font=(FONT_NAME, 25, "bold"), fg=GREEN, bg=YELLOW)
curr_title.grid(row=0, column=3)

curr_timer = Label(text="00:00", font=(FONT_NAME, 25, "bold"), fg=RED, bg=YELLOW)
curr_timer.grid(row=1, column=3)


# ----------BUTTONS----------------
run_button = Button(text="Start", font=(FONT_NAME, 16, "bold"), command=run_button, highlightthickness=0)
run_button.grid(row=2, column=3)

stop_button = Button(text="Stop", font=(FONT_NAME, 16, "bold"), command=stop_button, highlightthickness=0)
stop_button.grid(row=3, column=3)

pause_button = Button(text="Pause", font=(FONT_NAME, 16, "bold"), command=pause_button, highlightthickness=0)
pause_button.grid(row=4, column=3)

write_to_csv_button = Button(text="save to csv", font=(FONT_NAME, 16, "bold"), command=save_to_csv, highlightthickness=0)
write_to_csv_button.grid(row=4, column=2)

window.mainloop()

