#Manuel Diaz
#Calculator Rewritten v1.2



#Notes for next time:

import re
import tkinter as tk
from tkinter import StringVar
from tkinter import *
import os
from tkinter.filedialog import *

class Tools:
    @staticmethod
    def transaction_summary(list):
        """
        Static method that returns a long String of each transation and the total amount of money borrowed/paid off.

        ???: Use list(Dynamic Array), maybe use an list argument instead of a single int.
            Then you can probably add all elements within that list to display total money borrowed, payed off, and left to pay.

        Returns a long String
        """
        #variables
        statement = ""
        total = 0
        total_borrowed = 0
        total_paidoff = 0

        #Loop troughout the list to make a 'receipt'
        for x in list:
            total += x
            
            statement += "*"*25
            if x >= 0:
                statement += f"\nBorrowing: ${x:.2f} \nLeft to pay: ${total:.2f} \n"
                total_borrowed += x
            else:
                statement += f"\nPayed: ${(-1 * x):.2f} \nLeft to pay: ${total:.2f} \n"
                total_paidoff += (-1 * x)

        #'Final statement'
        statement += "*"*25
        statement += f"\nTotal money borrowed: ${total_borrowed:.2f}\nTotal money payed off: ${total_paidoff:.2f}\nLeft to pay: ${total:.2f}\n"
        statement += "*"*25+'\n'

        return statement


    @staticmethod
    def extract_file_to_list(file1, list1):
        """
        Static method that extraxts a a float from a multiple line string(like a txt fiile) 

        Returns a list with floats in them   ex. "[-2,34.54,-34.23]"
        """
        list1.clear()

        try:
            line = open(file1, 'r')
        except FileNotFoundError:
            return False

        filetext = line.read()
        
        for transaction in filetext.splitlines():
            if transaction[0] == '-':
                list1.append(-float(transaction[1:]))        
            elif transaction[0] == '+':
                list1.append(float(transaction[1:]))   
                


        return Tools.transaction_summary(list1)

    @staticmethod
    def add_transaction(file1, num):
        """
        Adds a string to a txt file as '+6' or '-4' in new line
        """

        line = open(file1, 'a')
        line.write(f'{str(num)}\n')
        return



class MyWindow():
    
    def __init__(self, win):
        """
        Initialize the window interface.
        """
        self.savelocation = askdirectory() # show an "Open" dialog box and return the path to the selected file
        
        self.current_displayed = "none"
        self.path_saves = ""

        #Create canvas for text and scrollbar
        self.canvas = Canvas(win)
        #Scrollbar for Text box
        self.scrollbar = Scrollbar(self.canvas)
        #Text Display Boxes
        self.text1 = Text(self.canvas, yscrollcommand = self.scrollbar.set)
        self.text1.insert(INSERT, "Please enter the name of the person that has a loan on file.\nOr feel free to make one.")
        self.text1.config(state = DISABLED)

        
        
        #Label Boxes
        self.label1 = Label(win, text = "Whos loan do you want to view?")
        self.label2 = Label(win, text = "Are they paying back or borrowing?")
        self.label3 = Label(win,text = "Currently viewing: No one")

        #Entry Boxes
        self.entry1 = Entry(win)
        self.entry2 = Entry(win)
        self.entry3 = Entry(win)

        #Buttons
        self.button1 = Button(win, text = "Submit", command = self.submit)
        self.button2 = Button(win, text = "Loan", command = self.loan, state = DISABLED)
        self.button3 = Button(win, text = "Paying", command = self.paying, state = DISABLED)
        self.button4 = Button(win, text = "Create", command = self.create)



        #Button placements
        self.canvas.pack()
        self.scrollbar.pack(side = RIGHT, fill="y")
        self.text1.pack(side = TOP)
        self.label3.pack()
        self.entry1.pack()
        self.button1.pack()
        self.button4.pack()
        self.entry2.pack()
        self.button2.pack()
        self.button3.pack()

        

        #Key binds
        self.entry1.bind('<Return>', self.submit)
        self.button1.bind('<Return>', self.submit)
        self.button2.bind('<Return>',self.loan)

        

    #Functions for buttons
    def submit(self, event = None):
        """
        Gets the name entered in one of the entries and tries to find that file within the data
        if found then it will display the transactions in that account.
        else prompt the user if they would like to make a file bc such file does not exist yet
        """
        self.text1.config(state = NORMAL)
        self.text1.delete(1.0,END)
        list1 = list()
        self.current_displayed = f'{self.savelocation}/{self.entry1.get().lower()}'
        file_found = Tools.extract_file_to_list(f'{self.current_displayed.lower()}.txt', list1)

        if False == file_found:
            temp = f'File not found. Would you like to create a file for {self.current_displayed}?\nOr try another search.\n'
            self.text1.insert(INSERT, temp)
            self.text1.tag_add("start", float(f'1.{temp.find(self.current_displayed)}')
                                       , float(f'1.{temp.find(self.current_displayed)+len(self.current_displayed)}'))
            self.text1.tag_config("start", background = 'yellow', underline = True )
            self.button2.config(state = DISABLED)
            self.button3.config(state = DISABLED)
            self.label3.config(text = 'Currently viewing: No one')
            
            
        else:
            self.text1.insert(INSERT, file_found)
            self.button2.config(state = NORMAL)
            self.button3.config(state = NORMAL)
            self.scrollbar.config(command = self.text1.yview)
            self.label3.config(text = f'Currently viewing: {self.current_displayed}')
            self.text1.yview_moveto('1.0')
            
            
            
        
        

        
        self.text1.config(state = DISABLED)
        
        return
    def create(self):
        """
        makes a txt file if the file that the user is trying to look for is not found
        """
        self.label3.config(text = 'Currently viewing: No one')

        self.text1.config(state = NORMAL)
        self.text1.delete(1.0, END)
        if os.path.isfile(f'{self.current_displayed}.txt'):
            self.text1.insert(INSERT, 'File already exist')
            self.button2.config(state = DISABLED)
            self.button3.config(state = DISABLED)
            
        else:    
            open((f'{self.current_displayed}.txt'), "w+")
            self.text1.insert(INSERT, f'{self.current_displayed}\'s loan file has now been created.')

        self.text1.config(state = DISABLED)
        self.entry1.delete(0, 'end')
        return
    def loan(self):
        """
        only accessable if a loan is being displayed
        will add a loan to the file that is currently being displayed
        """
        valid_input = True
        user_input = self.entry2.get()
        try:
            float(user_input)
        except ValueError:
            valid_input = False

        if valid_input:
            Tools.add_transaction(f'{self.current_displayed}.txt', f'+{self.entry2.get()}')
            self.submit()
        else:
            self.text1.config(state = NORMAL)
            self.text1.delete(1.0, END)
            self.text1.insert(INSERT, f'Please use a valid input for {self.current_displayed}\'s loan.')
            self.text1.config(state = DISABLED)
        return

    def paying(self):
        """
        only accessable if a loan is being displayed
        will add a payment to the file that is currently being displayed
        """
        valid_input = True
        user_input = self.entry2.get()
        try:
            float(user_input)
        except ValueError:
            valid_input = False

        if valid_input:
            Tools.add_transaction(f'{self.current_displayed}.txt', f'-{self.entry2.get()}')
            self.submit()
        else:
            self.text1.config(state = NORMAL)
            self.text1.delete(1.0, END)
            self.text1.insert(INSERT, f'Please use a valid input for {self.current_displayed}\'s loan.')
            self.text1.config(state = DISABLED)
        return
    
    

    


def main():
        #Run extra line first, extract_number -> single_transaction_summary -> total_transaction_summary.
        
        window = Tk()
        mywin = MyWindow(window)
        window.title("Manny Loans")
        window.geometry("500x500+450+150")




        window.resizable(False, False)
        window.mainloop()
        return






if __name__ == "__main__":
    main()
