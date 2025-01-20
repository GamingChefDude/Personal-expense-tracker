import csv
import os
import datetime
import matplotlib.pyplot as plt
import time

global amount, expenses_file

def database_cvs():
    global expenses_file
    expenses_file = "expenses.csv" #setting the storage file name

    #makes the storage file
    if not os.path.isfile(expenses_file):
        with open(expenses_file, mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount"])      

def add_expense():
    global amount, expenses_file

    print("\nWhat expense would you like to add?")
    print("\n1. Food\n2. Transportation\n3. Entertainment\n4. Bill\n5. Housing\n6. Other\n7. Back: ")
    
    #setting the category
    try:
        category_input = int(input("Enter the number of the expense: "))
    except ValueError:
        pass
        print("invalid input")
        time.sleep(1.5)
        add_expense()
    category_list = ["Food", "Transportation", "Entertainment", "Bill", "Housing", "Other", "Back"]
    category = (category_list[category_input - 1])
    print(f"You selected {category}")
    time.sleep(.5)
    
    #setting the date
    datex = datetime.datetime.now() 
    print(datex.strftime("Date: %d-%m-%Y"))
    date = datex.strftime("%d-%m-%Y")

    #getting valid input for money
    def valid_amount():
        global amount
        try:
            amount = float(input("Enter the amount of the expense: "))
            if amount < 0:
                print("Number cant be negetive")
                return amount
        except ValueError as e:
            print(f"\n\nInvalid input: {e}, please try again")
            valid_amount()            

    valid_amount()

    #getting everything in the storage file
    with open(expenses_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount]) 
    
    print("Expense added successfully!") 
    print("")

    return_main()

def view_expenses():
    try:
        with open(expenses_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader) 
            print(f"{'Date':<15}{'Category':<15}{'Amount':<10}") #printing the header
            print("-" * 58) #printing the line between header and expenses
            for row in reader:
                try:
                    print(f"{row[0]:<15}{row[1]:<15}${row[2]:<10}") # printing date, category and amount
                except (ValueError, IndexError):
                    pass
    except FileNotFoundError:
        print("Storage file does not exist\n")
    print("")

    return_main()

def generate_report():
    try:
        with open(expenses_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader) 
            categories = {}
            for row in reader:
                try:
                    if row[1] not in categories:
                        categories[row[1]] = float(row[2])
                    else:
                        categories[row[1]] += float(row[2])
                except (ValueError, IndexError):
                    pass
        
        plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%', startangle=90)
        plt.legend(title="Expenses", loc = "best")
        plt.title("Expenses by category")
        plt.show()
    except FileNotFoundError:
        print("No expenses found. Add some first!\n")

def monthly_expenses():
    try:
        month = input("What month do you want to see (mm-yyyy)?: ") 

        with open(expenses_file, mode="r") as file:
            reader = csv.reader(file)
            next(reader)
            filtered = [row for row in reader if row[0].split('-')[1:] == month.split('-')] #finding the rigth month
            if filtered:
                print(f"\nExpenses for {month}:")
                print(f"{'Date':<15}{'Category':<15}{'Amount':<10}") #printing the header
                print("-" * 40)
                for row in filtered:
                    print(f"{row[0]:<15}{row[1]:<15}${row[2]:<10}") #printing the expenses
            else:
                print(f"No expense for {month}")
    except FileExistsError:
        print("Storage file does not exsist")

    return_main()

def total_expenses():
    
    with open(expenses_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader) 
        #setting all the amounts to zero
        food = 0
        transportation = 0
        entertainment = 0
        bill = 0
        housing = 0
        other = 0
        total = 0

        for row in reader:
            try:
                #adds the amount on the rows with the same category and rounds the number to (xx.xx)
                if row[1] == "Food":
                    food += float(row[2])
                    food = round(food, 2)
                elif row[1] == "Transportation":
                    transportation += float(row[2])
                    transportation = round(transportation, 2)
                elif row[1] == "Entertainment":
                    entertainment += float(row[2])
                    entertainment = round(entertainment, 2)
                elif row[1] == "Bill":
                    bill += float(row[2])
                    bill = round(bill, 2)
                elif row[1] == "Housing":
                    housing += float(row[2])
                    housing = round(housing, 2)
                elif row[1] == "Other":
                    other += float(row[2])
                    other = round(other, 2)
                total += float(row[2])
                total = round(total, 2)
            except (ValueError, IndexError):
                pass
        print("\n---Total expenses---")
        print("-" * 20)

    #prints the category with the amount
    print(f"Food: ${food}")
    print(f"Transportation: ${transportation}")  
    print(f"Entertainment: ${entertainment}")
    print(f"Bill: ${bill}")
    print(f"Housing: ${housing}")
    print(f"Other: ${other}")  
    print("-" * 20)

    #print the total
    if total == 0:
        print("No expenses found. Add some first!\n")
    else:
        print(f"Total: ${total}\n")
    
    return_main()
    
def exit():
    print("Goodbye!")

def main():
    
    print("\n\n---Personal Expense Tracker---")
    print("-" * 30,)
    print("\n 1. Add expense\n 2. View expenses\n 3. Generate report\n 4. Monthly Expenses\n 5. Total\n 6. Exit\n")
    categories_input = (input("input here: "))
    
    if categories_input == "1":
        add_expense()
    elif categories_input == "2":
        view_expenses()
    elif categories_input == "3":
        generate_report()
        main()
    elif categories_input == "4":
        monthly_expenses()
    elif categories_input == "5":
        total_expenses()
    elif categories_input == "6":
        exit()
    else:
        print("\n\n\nInvalid choice. Please try again.\n")
        time.sleep(2)
        main()

def return_main():
    choise = str(input("Want to go back to main (y/n): "))  
    if choise == "y":
        main()
    elif choise == "n":
        exit()
    else:
        print("invalid input")
        return_main()

database_cvs()
main()