import os,sys
import subprocess

# implement pip as a subprocess to install packages:
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q","-r", "requirements.txt"])

# GUI Tools
from tkinter import*
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox


# Makes tables and allows data analysis
import pandas as pd
import pandastable as pt
import numpy as np

# Will fetch the html files
import requests

# Pulls data from html files
from bs4 import BeautifulSoup
import urllib.request

# All additional python files with all of their respective functions
from bill_tracker import*
from bloom_extract import*
from date_validator import *

# For date validation/ formatting
import datetime

#WIP
class sector_page:
    def __init__(self,date):
        self.window = Tk()
        self.window.title("Company Sectors/ Bill Subject")
        self.window.attributes('-fullscreen',False) #Makes the page take up the full screen

        #Allows user toggle full screen if desired
        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)

        #Sets the default resolution of the main page
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.window.geometry(str(width)+ "x" + str(height)) #Sets resolution

        self.date = date
        #Sets up the buttons
        self.company_sector()
        self.window.mainloop()

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)
    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)

    def company_sector(self):
        global selected_sector
        global selected_subject

        bloom,bloom_error = bloom_data() # Extracts bloom data
        subjects,subject_error = subject_list() 

        # bloom = bloom_data(date)
        sectors = bloom["sector"].unique().tolist()
        selected_sectors = ['0']*len(sectors)

        prompt = Label(self.window,text = "Please select the S&P 500 company sector(s) that you desire:",font = 30)
        prompt.grid(row = 0, column = 0)

        for i,sector in enumerate(sectors):
            selected_sectors[i] = ttk.Checkbutton(self.window,text=sector,style = "b.TCheckbutton")
            selected_sectors[i].grid(row=i+1, column=0)

        

        subjects,error_message = subject_list() 
        selected_subjects = ['0']*len(subjects)

        prompt = Label(self.window,text = "Please select the US Congress bill subject(s) that you desire:",font = 30)
        prompt.grid(row = i+2, column = 0)
        for j,subject in enumerate(subjects):
            selected_subjects[j] = ttk.Checkbutton(self.window,text=subject['name'],style = "b.TCheckbutton")
            selected_subjects[j].grid(row=i+3+j, column=0)

        confirm = Button(self.window,text = "Continue", font = 30)
        confirm.grid(row = i+4+j, column = 0)
        #confirm.config(command = lambda: self.bill_subject())
        if bloom_error != "":
            messagebox.showinfo("Error", bloom_error, parent = self.window)
        if subject_error != "":
            messagebox.showinfo("Error", subject_error,parent = self.window)

    def bill_subject(self):
        global selected_subject

        subjects = subject_list() 
        selected_subjects = ['0']*len(subjects)

        prompt = Label(self.window,text = "Please select the US Congress bill subject(s) that you desire:",font = 30)
        prompt.grid(row = 0, column = 0)
        for i,subject in enumerate(subjects):
            selected_subjects[i] = ttk.Checkbutton(self.window,text=subject['name'],style = "b.TCheckbutton")
            selected_subjects[i].grid(row=i+1, column=0)

        confirm = Button(self.window,text = "Continue", font = 30)
        confirm.grid(row = i+2, column = 0)
        confirm.config(command = lambda: self.bill_subject())


class Main_Page:
    def __init__(self):
        self.window = Tk()
        self.window.title("Bloomberg Terminal S&P 500 Index Companies")
        self.window.attributes('-fullscreen',False) #Makes the page take up the full screen

        #Allows user toggle full screen if desired
        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)

        #Sets the default resolution of the main page
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.window.geometry(str(width)+ "x" + str(height)) #Sets resolution


        #Sets up the buttons
        self.buttons()
        self.window.mainloop()

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)
    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)


    def date_button(self,event,button):
        date_str = simpledialog.askstring("Input", "Enter a date (mm-dd-yyyy): ", parent=self.window)
        print(f"Button {event.widget['text']} clicked. Date entered: {date_str}")

    def buttons(self):
        color = theme(0)
        options = ["Start Date", "End Date"]
        month = [None]*2
        day = [None]*2
        year = [None]*2
        
        text_color = 'black'

        # Creates labels for the header row
        header = Label(self.window, text = 'Date',background = color)
        header.grid(row = 0, column = 0)

        month_label = Label(self.window, text = 'Month',background = color)
        month_label.grid(row= 0, column = 1)

        day_label = Label(self.window, text = 'Day',background = color)
        day_label.grid(row= 0, column = 2)

        year_label = Label(self.window, text = 'Year',background = color)
        year_label.grid(row= 0, column = 3)
        
        for i,option in enumerate(options):
            # Creates a color theme
            color = theme(i)
            
            label = Label(self.window, text = option, fg=text_color,background = color)
            label.grid(row=i+1, column= 0)

            month[i] = Entry(self.window, fg=text_color, background=color)
            month[i].grid(row=i+1, column=1)

            day[i] = Entry(self.window, fg=text_color, background=color)
            day[i].grid(row=i+1, column=2)

            year[i] = Entry(self.window, fg=text_color, background=color)
            year[i].grid(row=i+1, column=3)
        # Displays the confirm button
        confirm = Button(self.window, text="Confirm", fg=text_color, background=color)
        confirm.grid(row=i+2, column=2)
        confirm.config(command=lambda e=i, b=confirm: self.confirmationPage( options, month,day,year))

    def confirmationPage(self, options, month, day, year):
        date = [None]*2
        check = True
        date, error = date_config(options,month,day,year)

        if len(error) == 0:
            messagebox.showinfo("Confirmation", "All entries are valid")
            sector_page(date)
        else:
            messagebox.showerror("Error", error)


# Sets color theme
def theme(index):
    if index % 2 == 0:
        return 'white'
    else:
        return 'white'

#bloom = []
#subjects=[]
app = Main_Page()



