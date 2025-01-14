import csv
import os
import datetime
import matplotlib.pyplot as plt

global amount

def database_cvs():
    if not os.path.isfile("expenses.csv"):
        with open("expenses.csv", mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount"])

def add_expense():
    global amount
    
    print("\nWhat expense would you like to add?")
    print("\n1. Food\n2. Transpotation\n3. Entertainment\n4. Bill\n5. Housing\n6. Other\n7. Back: ")
    expenses_input = input("Enter the number of the expense: ")
    if expenses_input == "1":
        expenses = "Food"
    elif expenses_input == "2":
        expenses = "Transpotation"
    elif expenses_input == "3":
        expenses = "Entertainment"
    elif expenses_input == "4":
        expenses = "Bill"
    elif expenses_input == "5":
        expenses = "Housing"
    elif expenses_input == "6":
        expenses = "Other"
    elif expenses_input == "7":
        main()
    else:
        print("error, invalid category")
        add_expense()
        print()

    datex = datetime.datetime.now() 
    print(datex.strftime("Date: %d-%m-%Y"))
    date = datex.strftime("%d-%m-%Y")

    def valid_amount():
        global amount
        try:
            amount = float(input("Enter the amount of the expense: "))
            if amount < 0:
                print("Number cant be negetive")
                return amount
        except ValueError as e:
            print(f"Invalid input: {e}, please try again")
            valid_amount()            

    valid_amount()

    with open("expenses.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, expenses, amount]) 
    
    print("Expense added successfully!") 
    print("")

    main = str(input("Want to go back to main (y/n): "))     
    if main == "y":
        main()
    else:
        exit()
    
def view_expenses():
    try:
        with open("expenses.csv", mode='r') as file:
            reader = csv.reader(file)
            next(reader) 
            print(f"{'Date':<15}{'Category':<15}{'Amount':<10}")
            print("-" * 58)
            for row in reader:
                try:
                    print(f"{row[0]:<15}{row[1]:<15}${row[2]:<10}")
                except (ValueError, IndexError):
                    pass
    except FileNotFoundError:
        print("Storage file does not exist\n")
    print("")
    
    Main = str(input("Want to go back to main (y/n): "))     
    if Main == "y":
        main()
    else:
        exit()

def generate_report():
    try:
        with open("expenses.csv", mode='r') as file:
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

def total_expenses():
    
    with open("expenses.csv", mode='r') as file:
        reader = csv.reader(file)
        next(reader) 
        food = 0
        transportation = 0
        entertainment = 0
        bill = 0
        housing = 0
        other = 0
        total = 0
        for row in reader:
            try:
                if row[1] == "Food":
                    food += float(row[2])
                    food = round(food, 2)
                elif row[1] == "Transpotation":
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

    print(f"Food: ${food}")
    print(f"Transpotation: ${transportation}")  
    print(f"Entertainment: ${entertainment}")
    print(f"Bill: ${bill}")
    print(f"Housing: ${housing}")
    print(f"Other: ${other}")  
    print("-" * 20)

    if total == 0:
        print("No expenses found. Add some first!\n")
    else:
        print(f"Total: ${total}\n")
    
    main = str(input("Want to go back to main (y/n): "))     
    if main == "y":
        main()
    else:
        exit()
    
def exit():
    print("Goodbye!")

def main():
    global Main
    print("\n\n---Personal Expense Tracker---")
    print("-" * 30,)
    print("\n 1. Add expense\n 2. View expenses\n 3. Generate report\n 4. Total\n 5. Exit\n")
    categories = input("input here: ")

    if categories == "1":
        add_expense()
    elif categories == "2":
        view_expenses()
    elif categories == "3":
        generate_report()
        main()
    elif categories == "4":
        total_expenses()
    elif categories == "5":
        exit()
    else:
        print("Invalid choice. Please try again.\n")
        main()

database_cvs()
main()