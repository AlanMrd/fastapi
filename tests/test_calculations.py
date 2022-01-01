import py
from app.calculations import add, BankAccount, InsufficientFunds
import pytest

@pytest.mark.parametrize("num1, num2, expected", [(1,2,3),(4,5,9),(2,9,11)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

def test_bank_inital_amount():
    bank_account = BankAccount(50)
    assert bank_account.balance == 50

    
def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(20) 
    assert bank_account.balance == 30

def test_deposit(bank_account):
    bank_account.deposit(30) 
    assert bank_account.balance == 80

def test_collect_interest(bank_account):
    bank_account.collect_interest() 
    assert round(bank_account.balance, 6) == 55

@pytest.mark.parametrize("deposited, withdraw, expected", [(200,100,100),(50,10,40),(1200,200,1000)])
def test_bank_transaction(zero_bank_account, deposited, withdraw, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)