menu = """
------------------------------------
[D]-Deposit
[W]-Withdraw
[E]-Extract
[Q]-Quit
------------------------------------
"""

balance = 0
limit = 500
extract = ""
num_withdraw = 0
LIMIT_WITHDRAW = 3

while True:
    print(menu)
    option = input('Choice one option: ')
    if option.upper() == "D":
        value = float(input("Enter the deposit amount: "))
        if value > 0:
            balance += value
            extract += f"Deposit of  {value:.2f}\n"
        else:
            print("Operation failed! The value entered is invalid.")

    elif option.upper() == "W":
        if num_withdraw != LIMIT_WITHDRAW:
            value = float(input("Enter the withdrawal amount: "))
            if balance < value:
                print("Operation failed! You do not have enough balance.")
            elif limit < value:
                print("Operation failed! Withdrawal amount exceeds limit.")
            elif value > 0:
                balance -= value
                extract += f"Withdrawal of $ {value:.2f}\n"
                num_withdraw += 1
            else:
                print("Operation failed! The value entered is invalid.")
        else:
            print("Operation failed! Withdrawal limit reached.")

    elif option.upper() == "E":
        print("\n================ EXTRACT ================")
        print("No movements were made." if not extract else extract)
        print(f"\nBalance: $ {balance:.2f}")
        print("==========================================")

    elif option == "Q":
        break

    else:
        print("Invalid operation, please select the desired operation again.")