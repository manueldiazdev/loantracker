#Manuel Diaz
#Calculator for personal loans
#Takes a file and calculates dept for the selected file (Person)
#v1
import re
import tkinter
from tkinter import StringVar
from tkinter import *

#Static method that extracts the number from a single line from the *.txt file, ignoring other characters,
#Returning the number as an int.
def extract_number(line):
    number = re.findall('\d*\.?\d+', line)
    return number

#Static method that takes in a *.txt file as 'lst' and calculates the amount the person owes, or not.
#returns a long string of each transaction and total amount owed.
def loan_calculator(lst):
    output = ""
    total_sums = 0.0
    total_paid = 0.0
    total_borrowed = 0.0
    try:
        file1 = open(lst, 'r')
    except FileNotFoundError:
        return "File not in system."

    loan_doc = file1.read()
    # loop till all lines are read

    for line in loan_doc.splitlines():

        # if the sign is '=' then add it to totalSums
        if line[0] == '=':

            total_sums += float(extract_number(line)[0])


        # if the sign is '+' then add it to totalBorrowed: "+" is the money they are borrowing.
        elif line[0] == '+':

            total_borrowed += float(extract_number(line)[0])
            output += ("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
                  "BORROWING: " + str(round(float(extract_number(line)[0]), 2)))
            output += ("\nLeft to pay: " + str(round((total_borrowed - total_paid), 2))+
                   "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

        # if the sign is '-' then add it to totalPaid: "-" is the money they have payed off.
        elif line[0] == '-':

            total_paid += float(extract_number(line)[0])
            output += ("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
                  "PAYING: " + str(round(float(extract_number(line)[0]), 2)))
            output += ("\nLeft to pay: " + str(round((total_borrowed - total_paid), 2))+
                   "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

    output += ("Total Money borrowed: " + str( round(total_borrowed, 2)))
    output += ("\nTotal Money paid: " + str( round(total_paid, 2)) )
    output += ("\nLeft to pay: " + str (round((total_borrowed - total_paid), 2)))





    file1.close()

    return output


#main
#creates an interface to display calculations and have user input
def main():

    #static method that reads the input by the user and looks for the file
    #displays string returned by 'loan_calculator()' on text box (GUI).
    def submit():
        output = ""
        person = entry.get()

        entry.delete(first= 0, last= len(person) )
        loan = person
        loan.lower()
        loan += "loan.txt"
        text.delete(1.0,END)
        text.insert(INSERT, loan_calculator(loan))


    



    window = tkinter.Tk()
    window.geometry("450x400")
    window.title("Manny Banks (v1)")
    var = StringVar()
    var.set("Who's loan do you want to view? [Enter = 'Tony'] ")

    label = Label(window, textvariable = var)
    button = Button(window, text="Submit", command = submit)
    text = Text(window)

    entry = Entry(window)

    text.pack()
    label.pack()
    entry.pack()
    button.pack()


    window.mainloop()
    again = True







main()