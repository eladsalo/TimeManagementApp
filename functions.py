import math
import tkinter
from tkinter import *
import csv
import datetime
import os
import pandas
from vars import timer, elapsed_time, total_time, DARK_GREEN, FONT_NAME
from dateutil.parser import parse

class Functions:

    # ---------------------------- TIMER RESET ------------------------------- #
    def stop_button(self,window, curr_timer, curr_title, total_timer):
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
    def pause_button(self, curr_title, window):
        global timer
        curr_title.config(text="Paused", fg=DARK_GREEN)
        window.after_cancel(timer)

    # ---------------------------- TIMER RUN ------------------------------- #
    def run_button(self, curr_title, curr_timer, window):
        curr_title.config(text="Running", fg=DARK_GREEN)
        self.count(curr_timer, window)  # pass total elapsed time as the starting value of counter

    def count(self, curr_timer, window):
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
        timer = window.after(1000, self.count, curr_timer, window)

    # ---------------------------- TAKE DOWN 2 MINUTES ------------------------------- #
    def take_down_2_minuets(self):
        global elapsed_time
        elapsed_time -= 120

    # ---------------------------- SHOW DETAILS- POPUP MASSAGE ------------------------------- #
    def show_details(self):
        # Read the contents of the CSV file and format as a table
        with open("time_records.csv", "r") as file:
            csv_reader = csv.reader(file)
            d = "date"
            t = "learning time"
            file_contents = f"{d:<15} {t:<15}\n"
            for row in csv_reader:
                print(row)
                if row[0] == "date":
                    continue
                file_contents += f"{row[0]:<15} {row[1]:<15}\n"

        popup = tkinter.Toplevel()
        popup.title("Message")
        popup.geometry("400x800")
        popup.resizable(False, False)
        popup_label = tkinter.Label(popup, font=(FONT_NAME, 15, "bold"), text=file_contents)
        popup_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

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
            self.show_details()

        keep_7_days_button = Button(popup, text="keep last week", font=(FONT_NAME, 16, "bold"), command=keep_last_7_days, highlightthickness=0)
        keep_7_days_button.grid(row=1, column=0, padx=10, pady=10)

        def best_day_fun():
            popup_best_day = tkinter.Toplevel()
            popup_best_day.title("Best day")
            popup_best_day.geometry("300x100")
            popup_best_day.resizable(False, False)

            popup_best_day_label = tkinter.Label(popup_best_day, font=(FONT_NAME, 15, "bold"), text="")
            popup_best_day_label.pack(padx=10, pady=10)
            with open("best_day.txt", 'r') as file:
                best_day = file.read()
            popup_best_day_label.config(text=best_day)

        best_day_button = Button(popup, text="best day", font=(FONT_NAME, 16, "bold"), command=best_day_fun, highlightthickness=0)
        best_day_button.grid(row=2, column=0, padx=10, pady=10)

        def best_average_fun():
            popup_best_average = tkinter.Toplevel()
            popup_best_average.title("Best day")
            popup_best_average.geometry("300x100")
            popup_best_average.resizable(False, False)

            popup_best_average_label = tkinter.Label(popup_best_average, font=(FONT_NAME, 15, "bold"), text="")
            popup_best_average_label.pack(padx=10, pady=10)
            with open("best_avg.txt", 'r') as file:
                best_average = file.read()
            popup_best_average_label.config(text=best_average)

        best_avg_button = Button(popup, text="best average", font=(FONT_NAME, 16, "bold"), command=best_average_fun, highlightthickness=0)
        best_avg_button.grid(row=3, column=0, padx=10, pady=10)


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
            self.update_best_avg(avg_str)

        avg_button = Button(popup, text="average", font=(FONT_NAME, 16, "bold"), command=average_fun, highlightthickness=0)
        avg_button.grid(row=1, column=1, padx=10, pady=10)
        avg_title = Label(popup, text="", font=(FONT_NAME, 20, "bold"))
        avg_title.grid(row=2, column=1, padx=10, pady=10)


        def display_history():
            with open("history.csv", "r") as file:
                csv_reader = csv.reader(file)
                d = "date"
                t = "learning time"
                file_contents = f"{d:<15} {t:<15}\n"
                for row in csv_reader:
                    if row[0] == "date":
                        continue
                    file_contents += f"{row[0]:<15} {row[1]:<15}\n"
            popup_history = tkinter.Toplevel()
            popup_history.title("History")
            popup_history.geometry("400x800")
            popup_history.resizable(False, False)
            popup_history_label = tkinter.Label(popup_history, font=(FONT_NAME, 15, "bold"), text=file_contents)
            popup_history_label.pack(padx=10, pady=10)

        history_button = Button(popup, text="history", font=(FONT_NAME, 16, "bold"), command=display_history, highlightthickness=0)
        history_button.grid(row=4, column=0, padx=10, pady=10)



        # def clear_info():
        #     filename = "time_records.csv"
        #     with open(filename, 'r+') as f:
        #         f.readline()  # read one line
        #         f.truncate(f.tell())  # terminate the file here. f.tell() returns the current position of the file pointer.
        #         popup.destroy()
        #         self.show_details()
        #
        # clear_title = Button(popup, text="clear all", font=(FONT_NAME, 16, "bold"), command=clear_info, highlightthickness=0)
        # clear_title.pack(padx=10, pady=10)


    # ---------------------------- SAVE TO CSV ------------------------------- #
    def save_to_csv(self, total_timer):
        global total_time
        today = datetime.date.today()
        data = pandas.read_csv("time_records.csv")
        time_str = ""
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

        self.update_time_sheets_if_needed()  # filling missing dates
        self.update_best_day(time_str)  # checking if today time is bigger from 'best_time' and update if it necessary

    # ------------ UPDATING MISSING DATES------------ #
    def update_time_sheets_if_needed(self):
        data = pandas.read_csv("time_records.csv")
        data['date'] = pandas.to_datetime(data['date'])
        date_range = pandas.date_range(start=data['date'].min(), end=data['date'].max())

        # for date in date_range:
        #     if date not in data['date'].values:
        #         new_row = {'date': date, 'timeClockRun': '00:00:00'}
        #         data = pandas.concat([data, pandas.DataFrame(new_row, index=[0])], ignore_index=True)
        for date in date_range:
            if date not in data['date'].values:
                new_row = {'date': date, 'timeClockRun': '00:00:00'}
                data = pandas.concat([data, pandas.DataFrame(new_row, index=[0])], ignore_index=True)
        data = data.sort_values(by='date')
        data.to_csv('time_records.csv', index=False)

    # ------------ UPDATE BEST DAY------------ #
    def update_best_day(self, time_str):
        filename = 'best_day.txt'
        try:
            # Read the contents of the file and parse them as a date
            with open(filename, 'r') as file:
                contents = file.read().strip()
            if contents:
                best_day = parse(contents)
            else:
                best_day = None
        except FileNotFoundError:
            # If the file doesn't exist, set best_day to None
            best_day = None
        except ValueError:
            # If the contents of the file can't be parsed as a datetime object, print an error message
            print(f'Error: could not parse contents of {filename} as a date')
            return

        # If best_day is None or today_time is later than best_day, write today_time to the file
        if best_day is None or parse(time_str) > best_day:
            with open(filename, 'w') as file:
                file.write(time_str)
                print(f'Successfully wrote to file {filename}')


        # ------------ UPDATE BEST AVERAGE------------ #
    def update_best_avg(self, time_str):
        filename = 'best_avg.txt'
        try:
            # Read the contents of the file and parse them as a date
            with open(filename, 'r') as file:
                contents = file.read().strip()
            if contents:
                # parse() function can parse a wide variety of date and time formats.
                # from dateutil.parser import parse
                best_avg = parse(contents)
            else:
                best_avg = None
        except FileNotFoundError:
            # If the file doesn't exist, set best_day to None
            best_avg = None
        except ValueError:
            # If the contents of the file can't be parsed as a datetime object, print an error message
            print(f'Error: could not parse contents of {filename} as a date')
            return

        # If best_day is None or today_time is later than best_day, write today_time to the file
        if best_avg is None or parse(time_str) > best_avg:
            with open(filename, 'w') as file:
                file.write(time_str)
                print(f'Successfully wrote to file {filename}')

    # ------------ KEY PANELS ACTIVATE FUNCTIONS------------ #
    def on_space_key(self, event, curr_title, curr_timer, window):
        if curr_title.cget("text") == "Stopped" or curr_title.cget("text") == "Timer" or\
                curr_title.cget("text") == "Paused":
            self.run_button(curr_title, curr_timer, window)
        else:
            self.pause_button(curr_title, window)

    def on_s_key(self, event, total_timer):
        self.save_to_csv(total_timer)

    def on_x_key(self, event, window, curr_timer, curr_title, total_timer):
        self.stop_button(window, curr_timer, curr_title, total_timer)

