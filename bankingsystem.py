from abc import ABC, abstractmethod
import streamlit as st
import random

# --- Classes ---
class Account(ABC):
    def __init__(self, account_no, customer, balance=0):
        self.account_no = account_no
        self.customer = customer
        self._balance = balance  

    @abstractmethod
    def calculate_interest(self):
        pass

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return f"Deposited ₹{amount}, New Balance: ₹{self._balance}"
        else:
            return "Enter a valid amount."

    def withdraw(self, amount):
        if amount <= self._balance:
            self._balance -= amount
            return f"Withdrew ₹{amount}, New Balance: ₹{self._balance}"
        else:
            return "Insufficient balance."

    def get_balance(self):
        return self._balance


class SavingsAccount(Account):
    interest_rate = 0.04
    MIN_BALANCE = 10000

    def __init__(self, account_no, customer, balance=0):
        if balance < self.MIN_BALANCE:
            raise ValueError("Minimum balance of ₹10,000 required to open Savings Account.")
        super().__init__(account_no, customer, balance)

    def withdraw(self, amount):
        if self._balance - amount < self.MIN_BALANCE:
            return f"❌ Cannot withdraw ₹{amount}. Minimum balance of ₹{self.MIN_BALANCE} must be maintained."
        else:
            return super().withdraw(amount)

    def calculate_interest(self):
        return self._balance * self.interest_rate


class CurrentAccount(Account):
    interest_rate = 0.01
    def calculate_interest(self):
        return self._balance * self.interest_rate


class Customer:
    def __init__(self, name, customer_id):
        self.name = name
        self._customer_id = customer_id
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)


class Bank:
    def __init__(self, name):
        self.name = name
        self.customers = []

    def add_customer(self, customer):
        self.customers.append(customer)


st.title("🏦 Bank Account Management System")

bankdetail = st.text_input("Enter your Bank Name")
cust_name = st.text_input("Enter your Name")

# Generate random IDs once (and store in session state)
if "customer_id" not in st.session_state:
    st.session_state.customer_id = random.randint(10000, 99999)
if "account_no" not in st.session_state:
    st.session_state.account_no = random.randint(1000000000, 9999999999)

st.write(f"🆔 Your Generated Customer ID: {st.session_state.customer_id}")
st.write(f"🏷️ Your Generated Account Number: {st.session_state.account_no}")

account_type = st.selectbox("Select Account Type", ["Savings Account", "Current Account"])
initial_balance = st.number_input("Enter Initial Balance", min_value=0, step=1000)

# Store account in session state
if st.button("Open Account"):
    try:
        customer = Customer(cust_name, st.session_state.customer_id)
        if account_type == "Savings Account":
            st.session_state.account = SavingsAccount(st.session_state.account_no, customer, initial_balance)
            st.success("Congrats! You have opened a Savings Account.")
        else:
            st.session_state.account = CurrentAccount(st.session_state.account_no, customer, initial_balance)
            st.success("Congrats! You have opened a Current Account.")
    except ValueError as e:
        st.error(str(e))

# Only show if account exists
if "account" in st.session_state:
    account = st.session_state.account

    st.info(f"💰 Current Balance: ₹{account.get_balance()}")
    st.info(f"📈 Interest Earned: ₹{account.calculate_interest()}")

    deposit_amount = st.number_input("Deposit Amount", min_value=0, step=500, key="deposit")
    if st.button("Deposit Money"):
        st.success(account.deposit(deposit_amount))

    withdraw_amount = st.number_input("Withdraw Amount", min_value=0, step=500, key="withdraw")
    if st.button("Withdraw Money"):
        st.warning(account.withdraw(withdraw_amount))
# Modify the Savings account class to ensure that user keeps a minimum balance of 10000 and you also have to use random library to include customerID and account_no with the help of random library

