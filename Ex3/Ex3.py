import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Client:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def perform_transaction(self, account, transaction):
        transaction.record(account)

    def add_account(self, account):
        self.accounts.append(account)


class Individual(Client):
    def __init__(self, name, birth_date, cpf, address):
        super().__init__(address)
        self.name = name
        self.birth_date = birth_date
        self.cpf = cpf


class Account:
    def __init__(self, number, client):
        self._balance = 0
        self._number = number
        self._agency = "0001"
        self._client = client
        self._history = History()

    @classmethod
    def new_account(cls, client, number):
        return cls(number, client)

    @property
    def balance(self):
        return self._balance

    @property
    def number(self):
        return self._number

    @property
    def agency(self):
        return self._agency

    @property
    def client(self):
        return self._client

    @property
    def history(self):
        return self._history

    def withdraw(self, amount):
        exceeded_balance = amount > self.balance

        if exceeded_balance:
            print("\n@@@ Transaction failed! Insufficient funds. @@@")

        elif amount > 0:
            self._balance -= amount
            print("\n=== Withdrawal successful! ===")
            return True

        else:
            print("\n@@@ Transaction failed! Invalid amount. @@@")

        return False

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print("\n=== Deposit successful! ===")
        else:
            print("\n@@@ Transaction failed! Invalid amount. @@@")
            return False

        return True


class CheckingAccount(Account):
    def __init__(self, number, client, limit=500, withdrawal_limit=3):
        super().__init__(number, client)
        self._limit = limit
        self._withdrawal_limit = withdrawal_limit

    def withdraw(self, amount):
        num_withdrawals = len(
            [transaction for transaction in self.history.transactions if transaction["type"] == Withdrawal.__name__]
        )

        exceeded_limit = amount > self._limit
        exceeded_withdrawals = num_withdrawals >= self._withdrawal_limit

        if exceeded_limit:
            print("\n@@@ Transaction failed! Withdrawal amount exceeds the limit. @@@")

        elif exceeded_withdrawals:
            print("\n@@@ Transaction failed! Maximum number of withdrawals exceeded. @@@")

        else:
            return super().withdraw(amount)

        return False

    def __str__(self):
        return f"""
            Agency:	{self.agency}
            Account:	{self.number}
            Holder:	{self.client.name}
        """


class History:
    def __init__(self):
        self._transactions = []

    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction):
        self._transactions.append(
            {
                "type": transaction.__class__.__name__,
                "amount": transaction.amount,
                "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transaction(ABC):
    @property
    @abstractproperty
    def amount(self):
        pass

    @abstractclassmethod
    def record(self, account):
        pass


class Withdrawal(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def record(self, account):
        transaction_success = account.withdraw(self.amount)

        if transaction_success:
            account.history.add_transaction(self)


class Deposit(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def record(self, account):
        transaction_success = account.deposit(self.amount)

        if transaction_success:
            account.history.add_transaction(self)

import textwrap

def menu():
    menu_text = """\n
    ================ MENU ================
    [1]\tDeposit
    [2]\tWithdraw
    [3]\tStatement
    [4]\tNew User
    [5]\tNew Account
    [6]\tList Accounts  
    [7]\tQuit
    Choice a Option:
    => """
    return input(textwrap.dedent(menu_text))

def filter_client(cpf, clients):
    filtered_clients = [client for client in clients if client.cpf == cpf]
    return filtered_clients[0] if filtered_clients else None

def retrieve_client_account(client):
    if not client.accounts:
        print("\n Client has no account!")
        return
    return client.accounts[0]

def deposit(clients):
    cpf = input("Enter client CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\nClient not found!")
        return

    amount = float(input("Enter deposit amount: "))
    transaction = Deposit(amount)

    account = retrieve_client_account(client)
    if not account:
        return

    client.perform_transaction(account, transaction)

def withdraw(clients):
    cpf = input("Enter client CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\nClient not found!")
        return

    amount = float(input("Enter withdrawal amount: "))
    transaction = withdraw(amount)

    account = retrieve_client_account(client)
    if not account:
        return

    client.perform_transaction(account, transaction)

def display_statement(clients):
    cpf = input("Enter client CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\nClient not found!")
        return

    account = retrieve_client_account(client)
    if not account:
        return

    print("\n================ STATEMENT ===============")
    transactions = account.history.transactions

    statement = ""
    if not transactions:
        statement = "No transactions made."
    else:
        for transaction in transactions:
            statement += f"\n{transaction['type']}:\n\t$ {transaction['amount']:.2f}"

    print(statement)
    print(f"\nBalance:\n\t$ {account.balance:.2f}")
    print("==========================================")

def create_client(clients):
    cpf = input("Enter CPF (numbers only): ")
    client = filter_client(cpf, clients)

    if client:
        print("\n A client with this CPF already exists!")
        return

    name = input("Enter full name: ")
    birth_date = input("Enter birth date (dd-mm-yyyy): ")
    address = input("Enter address (street, number - neighborhood - city/state abbreviation): ")

    client = Individual(name=name, birth_date=birth_date, cpf=cpf, address=address)

    clients.append(client)

    print("\n=== Client successfully created! ===")

def create_account(account_number, clients, accounts):
    cpf = input("Enter client CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\nClient not found, account creation process terminated!")
        return

    account = CheckingAccount.new_account(client=client, number=account_number)
    accounts.append(account)
    client.accounts.append(account)

    print("\nAccount successfully created!")

def list_accounts(accounts):
    if accounts == []:
        print('=' * 100)
        print('No accounts created')
        print('=' * 100)
    else:
        for account in accounts:
            print("=" * 100)
            print(textwrap.dedent(str(account)))

def main():
    clients = []
    accounts = []

    while True:
        option = menu()
        match option:
            case '1':
                deposit(clients)
            case '2':
                withdraw(clients)
            case "3":
                display_statement(clients)
            case '4':
                create_client(clients)
            case '5':
                account_number = len(accounts) + 1
                create_account(account_number, clients, accounts)
            case '6':
                list_accounts(accounts)
            case '7':
                break
            case _:
                print("\nInvalid operation, please select the desired operation again.")

if __name__ == '__main__':
    main()
