from your_main_file_name import BankAccount, PersonalAccount, BusinessAccount, InvalidInputError, BankingSystem

acc = BankAccount("12345", "1111", "Personal", 100)
result = acc.deposit(50)
assert result == "Deposit completed."
assert acc.funds == 150

acc = BankAccount("12345", "1111", "Personal", 100)
result = acc.deposit(-20)
assert result == "Invalid amount for deposit."
assert acc.funds == 100

acc = BankAccount("12345", "1111", "Personal", 100)
result = acc.withdraw(50)
assert result == "Withdrawal completed."
assert acc.funds == 50

acc = BankAccount("12345", "1111", "Personal", 100)
result = acc.withdraw(200)
assert result == "Insufficiency of funds or invalid withdrawal sum."
assert acc.funds == 100

acc1 = BankAccount("12345", "1111", "Personal", 100)
acc2 = BankAccount("54321", "2222", "Personal", 50)
result = acc1.transfer(40, acc2)
assert result == "Transfer completed."
assert acc1.funds == 60
assert acc2.funds == 90

acc1 = BankAccount("12345", "1111", "Personal", 30)
acc2 = BankAccount("54321", "2222", "Personal", 50)
result = acc1.transfer(100, acc2)
assert result == "Insufficiency of funds or invalid withdrawal sum."
assert acc1.funds == 30
assert acc2.funds == 50

bank = BankingSystem()
acc = bank.create_account("Personal")
assert acc.account_category == "Personal"

bank = BankingSystem()
acc = bank.create_account("Business")
assert acc.account_category == "Business"

bank = BankingSystem()
acc = bank.create_account("Personal")
logged_in = bank.login(acc.account_id, acc.passcode)
assert logged_in.account_id == acc.account_id

bank = BankingSystem()
try:
    bank.login("wrongid", "wrongpass")
except InvalidInputError:
    pass
else:
    assert False, "Login should have failed"

acc = BankAccount("12345", "1111", "Personal", 100)
topup_amount = 30
result = acc.withdraw(topup_amount)
assert result == "Withdrawal completed."
assert acc.funds == 70

bank = BankingSystem()
acc = bank.create_account("Personal")
acc_id = acc.account_id
bank.delete_account(acc_id)
assert acc_id not in bank.accounts

print("All tests passed successfully!")

