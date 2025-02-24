import textwrap
balance = 0
limit = 500
extract = ""
num_withdraw = 0
LIMIT_WITHDRAW = 3
users = []
accounts =[]
AGENCY = "0001"


def menu():
    menu = """
    ------------------------------------
    [1]-Deposit
    [2]-Withdraw
    [3]-Extract
    [4]-New Account
    [5]-Account List
    [6]-New User
    [7]-Quit
    ------------------------------------
    Choice one option:
    """

    return input(textwrap.dedent(menu))

def deposit_func(balance,value,extract):
    if value > 0:
        balance += value
        extract += f"Deposit of $ {value:.2f}\n"
    else:
        print("Operation failed! The value entered is invalid.")
    return balance , extract

def withdraw_func(*,balance,extract,limit,num_withdraw):
    value = float(input("Enter the withdrawal amount: "))
    if balance < value:
        print("Operation failed! You do not have enough balance.")
    elif limit < value:
        print("Operation failed! Withdrawal amount exceeds limit.")
    elif value > 0:
        balance -= value
        extract += f"Withdrawal of $ {value:.2f}\n"
        num_withdraw += 1
        return balance , extract
    else:
        print("Operation failed! The value entered is invalid.")

def extract_func(balance,/,*, extract):
    print("\n================ EXTRACT ================")
    print("No movements were made." if not extract else extract)
    print(f"\nBalance: $ {balance:.2f}")
    print("==========================================")

def create_user(users):
    cpf = input('Enter your CPF (Only numbers): ')
    user = filter_users(cpf,users)

    if user:
        print('There is already a user with this CPF')
        return

    name = input("Enter your name: ")
    date = input("Enter your date of birth(DD-MM-YYYY): ")
    adress = input("Inform your address (street, number, neighborhood, city): ")

    users.append({'Name':name,"Date":date,"CPF":cpf,"Adress":adress})

    print("User created successfully")

def filter_users(cpf, users):
    users_filter = [user for user in users if user['CPF'] == cpf]
    return users_filter[0] if users_filter else None

def create_account(agency,number_account,users):
    cpf = input("'Enter your CPF (Only numbers): ")
    user = filter_users(cpf,users)

    if user:
        print("Account created successfully")
        return {"Agency": agency,"Number Account":number_account,"User":user}

    print("User not found!")

def accounts_list(accounts):
    for account in accounts:
        info = f"""
            Agency:\t{account['Agency']}
            C/C:\t\t{account['Number Account']}
            User:\t{account['User']['Name']}
        """
        print('=' *50)
        print(textwrap.dedent(info))

while True:
    option = menu()

    match option:
        case '1':
            value = float(input("Enter the deposit amount: "))
            balance , extract = deposit_func(balance,value,extract)

        case '2':
            if num_withdraw != LIMIT_WITHDRAW:
                balance , extract = withdraw_func(balance=balance,extract = extract,limit=limit,num_withdraw=num_withdraw)
            else:
                print("Operation failed! Withdrawal limit reached.")

        case "3":
            extract_func(balance, extract= extract)

        case "4":
            number_account = len(accounts) + 1
            account = create_account(AGENCY, number_account, users)

            if account:
                accounts.append(account)

        case "5":
            accounts_list(accounts)

        case "6":
            create_user(users)

        case "7":
            break

        case _:
            print("Invalid operation, please select the desired operation again.")