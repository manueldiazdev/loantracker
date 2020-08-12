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
def loan_calculator(lst, transaction = ""):
    output = ""
    total_sums = 0.0
    total_paid = 0.0
    total_borrowed = 0.0
    try:
        file1 = open(lst, 'r')
    except FileNotFoundError:
        return "File not in system."
    #if transaction is NOT blank then it will insert anything.



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

        global person
        person = entry.get()


        #entry.delete(first= 0, last= len(person) )
        global loan
        loan = person
        loan.lower()
        loan += "loan.txt"
        text.delete(1.0,END)
        text.insert(INSERT, loan_calculator(loan))
        if (loan_calculator(loan)) == "File not in system.":
            button2.config(state= DISABLED)
            button3.config(state= DISABLED)
            window.title("Manny Banks (v1.2)")

        else:
            window.title("Manny Banks (v1.2): " + person)
            button2.config(state=NORMAL)
            button3.config(state=NORMAL)

    def paying_back():
        global person
        person = entry.get()
        global loan
        loan = person
        loan.lower()
        loan += "loan.txt"
        money = ("-"+entry2.get())
        f = open(loan, 'a')
        f.write(money + "\n")
        f.close()





    def borrowing():
        global person
        person = entry.get()
        global loan
        loan = person
        loan.lower()
        loan += "loan.txt"
        money = ("+"+entry2.get())
        f = open(loan, 'a')
        f.write(money + "\n")
        f.close()



    def create_loan():
        new_file = entry3.get()
        entry3.delete(first=0, last=len(entry3.get()))
        txt_file = open((new_file.lower()+"loan.txt"), "w+")
        txt_file.close()
        var3.set(f"Created {new_file}'s loan!\nType another name")


    window = tkinter.Tk()
    window.geometry("500x600")
    window.title("Manny Banks (v1.2)")
    var = StringVar()
    var.set("Who's loan do you want to view?")

    label = Label(window, textvariable = var)
    button = Button(window, text="Submit/Update", command = submit)
    text = Text(window)
    entry = Entry(window)

    #Edit a dept page
    var2 = StringVar()
    var2.set("Insert amount paying or borrowing.")
    label2 = Label(window, textvariable = var2)
    entry2 = Entry(window)

    button2 = Button(window, text= "paying back", state = DISABLED, command = paying_back)
    button3 = Button(window, text= "borrowing", state = DISABLED, command = borrowing)


    #An option that allows the user to make a text file
    var3 = StringVar()
    var3.set("Create a loan file for someone. Type name below.")
    label3 = Label(window, textvariable = var3)
    entry3 = Entry(window)
    button4 = Button(window, text = "Create file", command = create_loan)

    text.pack()
    label.pack()
    entry.pack()
    button.pack()
    label2.pack()
    entry2.pack()
    button2.pack()
    button3.pack()
    label3.pack()
    entry3.pack()
    button4.pack()


    window.mainloop()







main()