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
class company_page:
    def __init__(self,subject):
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
        self.buttons(subjects)
        self.window.mainloop()

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)
    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)

    def buttons(self,bills):
        self.selected = []

        for i,bill in enumerate(bills):
            # Creates a color theme
            color = theme(i)
            
            # Selecting product class to operate on
            b = Button(self.window,text="Select Product Class" ,background=color)
            b.grid(row=i, column=0)
            b.config(command = lambda e=i, b = b: self.productPage(e, b))

            # Displays the product class name
            self.e = Entry(self.window, width=150, fg='white',font=('Arial',16,'bold'),background = color)
            self.e.grid(row=i, column= 1)
            self.e.insert(END, subject['name'])

    def productPage(self,index,btn):
        stats = Category_Page(data,index)


class Main_Page:
    def __init__(self,subjects,bloom):
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
        self.buttons(subjects)
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

    def buttons(self,subjects):
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

        if len(error) != 0:
            messagebox.showerror("Error", error)


# Sets color theme
def theme(index):
    if index % 2 == 0:
        return 'white'
    else:
        return 'blue'

#bloom = bloom_data()
#subjects = subject_list()
bloom = []
subjects=[]
app = Main_Page(subjects,bloom)



