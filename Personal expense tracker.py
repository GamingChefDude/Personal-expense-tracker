import csv
import os
import datetime
import matplotlib.pyplot as plt
import time
import sys

def database_csv():
    global expenses_file
    expenses_file = "expenses.csv" #setting the storage file name

    #makes the storage file if it dont exicst already
    if not os.path.isfile(expenses_file):
        with open(expenses_file, mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount"])      

def password():
    print("\n\n---Personal Expense Tracker---")
    print("-" * 30,)
    print("This Program is password protected")
    real_password = "hellow"
    
    while True:
        password_input = input("Write the correct password: ")
        if real_password == password_input:
            print("Correct password! \nWelcome in")
            time.sleep(1)
            main()
            break
        else:
            print("Wrong password \nTry Again")

def check_budget():
        try:
            with open("budget.txt", mode='r') as file:
                budget_limit = float(file.read())

            current_month = datetime.datetime.now().strftime("%m-%Y")
            with open(expenses_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)
                total_expenses = sum(float(row[2]) for row in reader if row[0].split('-')[1:] == current_month.split('-'))

            if total_expenses > budget_limit:
                print(f"Warning: You have exceeded your budget of ${budget_limit:.2f}. Current expenses: ${total_expenses:.2f}.")
            else:
                print(f"You are within your budget. Current expenses: ${total_expenses:.2f}, Budget: ${budget_limit:.2f}.")
        except FileNotFoundError:
            print("No budget has been set. Please set a budget first.")
        except ValueError:
            print("Error in reading budget. Set it again.")
        return_main()

def valid_amount():
    while True:
        try:
            amount = float(input("Enter the amount of the expense: "))
            if amount < 0:
                print("Number cant be negetive")
            else:
                return amount
        except ValueError as e:
            print(f"\n\nInvalid input: {e}, please try again")   

def add_expense():
    print("\nWhat expense would you like to add?")
    print("\n1. Food\n2. Transportation\n3. Entertainment\n4. Bill\n5. Housing\n6. Other")
    
    category_list = ["Food", "Transportation", "Entertainment", "Bill", "Housing", "Other"]
    #setting the category
    while True:
        try:
            category_input = int(input("Enter the number of the expense: "))
            category = (category_list[category_input - 1])
            break
        except (ValueError, IndexError): #removing errors
            pass
            print("invalid input")
            time.sleep(1)

    print(f"You selected {category}")
    time.sleep(1)
    
    #setting the date
    datex = datetime.datetime.now() 
    print(datex.strftime("Date: %d-%m-%Y"))
    date = datex.strftime("%d-%m-%Y")

    #getting valid input for money     
    amount = valid_amount()

    #getting everything in the storage file
    with open(expenses_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount]) 
    
    print("Expense added successfully!") 
    print("")
    check_budget()

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
    except FileNotFoundError:
        print("Storage file does not exsist")

    return_main()

def total_expenses():
    with open(expenses_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader) 
        #setting all the amounts to zero
        category = {"food": 0, "transportation": 0, "entertainment": 0, "bill": 0, "housing": 0, "other": 0, "total": 0}

        for row in reader:
            try:
                expense = float(row[2])
                #adds the amount on the rows with the same category and rounds the number to (xx.xx)
                if row[1] == "Food":
                    category["food"] += expense
                elif row[1] == "Transportation":
                    category["transportation"] += expense
                elif row[1] == "Entertainment":
                    category["entertainment"] += expense
                elif row[1] == "Bill":
                    category["bill"] += expense
                elif row[1] == "Housing":
                    category["housing"] += expense
                elif row[1] == "Other":
                    category["other"] += expense
                category["total"] += expense
            except (ValueError, IndexError):
                pass
        print("\n---Total expenses---")
        print("-" * 20)

    #prints the category with the amount
    print(f"Food: ${round(category['food'], 2)}")
    print(f"Transportation: ${round(category['transportation'], 2)}")  
    print(f"Entertainment: ${round(category['entertainment'], 2)}")
    print(f"Bill: ${round(category['bill'], 2)}")
    print(f"Housing: ${round(category['housing'], 2)}")
    print(f"Other: ${round(category['other'], 2)}")  
    print("-" * 20)

    #print the total
    print(f"Total: ${round(category['total'], 2)}\n")
    
    return_main()

def fun_budget():   
    def set_budget():
        try:
            budget_limit = float(input("Set your monthly budget limit: $"))
            with open("budget.txt", mode='w') as file:
                file.write(str(budget_limit))
            print("Budget set successfully!")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            set_budget()
        return_main()
    print("\n1. Set budget \n2. See budget")
    select = input("What do you want to do?: ")
    if select == "1":
        print("You chose set budget")
        time.sleep(1)
        set_budget()
    elif select == "2":
        print("You chose see budget")
        time.sleep(1)
        check_budget()
    else:
        print("Invalid choise")

def main():
    while True:
        print("\n\n---Personal Expense Tracker---")
        print("-" * 30,)
        print("\n1. Add expense\n2. View expenses\n3. Generate report\n4. Monthly Expenses\n5. Total\n6. Set budget \n7. Exit\n")
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
            fun_budget()
        elif categories_input == "7":
            print("Goodbye")
            break
        else:
            print("\n\n\nInvalid choice. Please try again.\n")
            time.sleep(2)

def return_main():
    choise = str(input("Want to go back to main (y/n): "))  
    while True:
        if choise == "y":
            main()
        elif choise == "n":
            exit()
        else:
            print("invalid input")

database_csv()
password()