import random
import tkinter as tk
from tkinter import messagebox, simpledialog

class BankAccount:
    def __init__(self, account_id, pin, account_type, balance=0):
        self.account_id = account_id
        self.pin = pin
        self.account_type = account_type
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return "Deposit successful."
        else:
            return "Invalid deposit amount."

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            return "Withdrawal successful."
        else:
            return "Insufficient balance or invalid amount."

    def transfer(self, amount, receiver):
        withdraw_msg = self.withdraw(amount)
        if withdraw_msg == "Withdrawal successful.":
            receiver.deposit(amount)
            return "Transfer successful."
        else:
            return withdraw_msg

class BankingSystem:
    def __init__(self, filename="accounts.txt"):
        self.filename = filename
        self.accounts = self.load_accounts()

    def load_accounts(self):
        accounts = {}
        try:
            with open(self.filename, "r") as f:
                for line in f:
                    acc_id, pin, acc_type, bal = line.strip().split(",")
                    accounts[acc_id] = BankAccount(acc_id, pin, acc_type, float(bal))
        except FileNotFoundError:
            pass
        return accounts

    def save_accounts(self):
        with open(self.filename, "w") as f:
            for acc in self.accounts.values():
                f.write(f"{acc.account_id},{acc.pin},{acc.account_type},{acc.balance}\n")

    def create_account(self, acc_type):
        acc_id = str(random.randint(10000, 99999))
        while acc_id in self.accounts:
            acc_id = str(random.randint(10000, 99999))
        pin = str(random.randint(1000, 9999))
        account = BankAccount(acc_id, pin, acc_type)
        self.accounts[acc_id] = account
        self.save_accounts()
        return account

    def login(self, acc_id, pin):
        if acc_id in self.accounts:
            acc = self.accounts[acc_id]
            if acc.pin == pin:
                return acc
        return None

    def delete_account(self, acc_id):
        if acc_id in self.accounts:
            del self.accounts[acc_id]
            self.save_accounts()
            return True
        return False

class BankingAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank App")
        self.bank = BankingSystem()
        self.current_account = None

        self.label = tk.Label(root, text="Welcome to Bank App")
        self.label.pack(pady=10)

        self.login_btn = tk.Button(root, text="Login", command=self.login)
        self.login_btn.pack(pady=5)

        self.create_btn = tk.Button(root, text="Create Account", command=self.create_account)
        self.create_btn.pack(pady=5)

        self.logout_btn = tk.Button(root, text="Logout", command=self.logout)
        self.logout_btn.pack(pady=5)
        self.logout_btn.config(state=tk.DISABLED)

        self.options_frame = tk.Frame(root)
        self.options_frame.pack(pady=10)

    def create_account(self):
        acc_type = simpledialog.askstring("Create Account", "Enter account type (Personal or Business):")
        if acc_type not in ["Personal", "Business"]:
            messagebox.showerror("Error", "Invalid account type.")
            return
        acc = self.bank.create_account(acc_type)
        messagebox.showinfo("Account Created", f"ID: {acc.account_id}\nPIN: {acc.pin}")

    def login(self):
        acc_id = simpledialog.askstring("Login", "Enter Account ID:")
        pin = simpledialog.askstring("Login", "Enter PIN:")
        acc = self.bank.login(acc_id, pin)
        if acc:
            self.current_account = acc
            messagebox.showinfo("Login", f"Welcome! You logged into {acc.account_type} account {acc.account_id}.")
            self.show_options()
            self.logout_btn.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Login Failed", "Wrong ID or PIN.")

    def logout(self):
        self.current_account = None
        self.clear_options()
        self.logout_btn.config(state=tk.DISABLED)
        messagebox.showinfo("Logout", "You logged out.")

    def show_options(self):
        self.clear_options()
        tk.Button(self.options_frame, text="Check Balance", command=self.check_balance).pack(pady=2)
        tk.Button(self.options_frame, text="Deposit", command=self.deposit).pack(pady=2)
        tk.Button(self.options_frame, text="Withdraw", command=self.withdraw).pack(pady=2)
        tk.Button(self.options_frame, text="Transfer", command=self.transfer).pack(pady=2)
        tk.Button(self.options_frame, text="Top-Up Mobile", command=self.mobile_topup).pack(pady=2)
        tk.Button(self.options_frame, text="Delete Account", command=self.delete_account).pack(pady=2)

    def clear_options(self):
        for widget in self.options_frame.winfo_children():
            widget.destroy()

    def check_balance(self):
        bal = self.current_account.balance
        messagebox.showinfo("Balance", f"Your balance is: {bal}")

    def deposit(self):
        amt_str = simpledialog.askstring("Deposit", "Enter amount to deposit:")
        try:
            amt = float(amt_str)
            msg = self.current_account.deposit(amt)
            self.bank.save_accounts()
            messagebox.showinfo("Deposit", msg)
        except:
            messagebox.showerror("Error", "Invalid amount.")

    def withdraw(self):
        amt_str = simpledialog.askstring("Withdraw", "Enter amount to withdraw:")
        try:
            amt = float(amt_str)
            msg = self.current_account.withdraw(amt)
            self.bank.save_accounts()
            messagebox.showinfo("Withdraw", msg)
        except:
            messagebox.showerror("Error", "Invalid amount.")

    def transfer(self):
        rec_id = simpledialog.askstring("Transfer", "Enter recipient account ID:")
        if rec_id not in self.bank.accounts:
            messagebox.showerror("Error", "Recipient not found.")
            return
        amt_str = simpledialog.askstring("Transfer", "Enter amount to transfer:")
        try:
            amt = float(amt_str)
            recipient = self.bank.accounts[rec_id]
            msg = self.current_account.transfer(amt, recipient)
            self.bank.save_accounts()
            messagebox.showinfo("Transfer", msg)
        except:
            messagebox.showerror("Error", "Invalid amount.")

    def mobile_topup(self):
        number = simpledialog.askstring("Mobile Top-Up", "Enter mobile number:")
        amt_str = simpledialog.askstring("Mobile Top-Up", "Enter amount to top up:")
        try:
            amt = float(amt_str)
            msg = self.current_account.withdraw(amt)
            self.bank.save_accounts()
            if msg == "Withdrawal successful.":
                messagebox.showinfo("Top-Up", f"{amt} topped up to {number}.")
            else:
                messagebox.showerror("Top-Up Failed", msg)
        except:
            messagebox.showerror("Error", "Invalid input.")

    def delete_account(self):
        confirm = messagebox.askyesno("Delete Account", "Are you sure?")
        if confirm:
            success = self.bank.delete_account(self.current_account.account_id)
            if success:
                messagebox.showinfo("Deleted", "Account deleted.")
                self.logout()
            else:
                messagebox.showerror("Error", "Account could not be deleted.")

root = tk.Tk()
app = BankingAppGUI(root)
root.mainloop()
