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
    if opcao.upper() == "D":
        valor = float(input("Enter the deposit amount: "))
        if valor > 0:
            balance += valor
            extract += f"Deposit of  {valor:.2f}\n"
        else:
            print("Operation failed! The value entered is invalid.")

    elif option.upper() == "W":
        if num_withdraw != LIMIT_WITHDRAW:
            valor = float(input("Enter the withdrawal amount: "))
            if balance < valor:
                print("Operation failed! You do not have enough balance.")
            elif limit < valor:
                print("Operation failed! Withdrawal amount exceeds limit.")
            elif valor > 0:
                balance -= valor
                extract += f"Withdrawal of $ {valor:.2f}\n"
                num_withdraw += 1
            else:
                print("Operation failed! The value entered is invalid.")
        else:
            print("Operation failed! Withdrawal limit reached.")

    elif opcao.upper() == "E":
        print("\n================ EXTRACT ================")
        print("No movements were made." if not extract else extract)
        print(f"\nBalance: $ {saldo:.2f}")
        print("==========================================")

    elif opcao.upper() == "Q":
        break

    else:
        print("Invalid operation, please select the desired operation again.")