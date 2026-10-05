from abc import ABC , abstractmethod

class Account(ABC) :
    @abstractmethod
    def deposit(self , amount):
        pass
    @abstractmethod
    def withdraw(self , amount):
        pass

class BankAccount(Account):
    def __init__(self , account_number ,name , password , balance):
        self.account_number = str(account_number)
        self.name = name
        self.__password = password
        self.__balance = int(balance)
    def get_password(self):
        return self.__password
    def get_balance(self):
        return self.__balance
    
    account_type = 'Basic'

    def set_name(self, name):
        self.name = name

    def set_password(self, password):
        self.__password = password

    def _deduct(self, amount):         
        self.__balance -= amount

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if amount > self.__balance :
            return False
        self.__balance -= amount
        return True
    
    def __str__(self):
        return f'{self.account_number} {self.name} {self.__balance}'

class SavingsAccount(BankAccount):
    account_type = 'Savings'
    FEE = 0.01

    def withdraw(self, amount):          # السحب فيه رسوم 1%
        total = amount + int(amount * self.FEE)
        return super().withdraw(total)

class CurrentAccount(BankAccount):
    account_type = 'Current'
    OVERDRAFT = 500

    def withdraw(self, amount):          
        if amount > self.get_balance() + self.OVERDRAFT:
            return False
        self._deduct(amount)
        return True