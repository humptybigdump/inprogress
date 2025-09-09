import logging

# Set up the logging configuration
logging.basicConfig(filename='bank_transactions.log', 
                    level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Create a logger for this module
logger = logging.getLogger(__name__)

class BankAccount:
    def __init__(self, account_holder: str, balance: float):
        self.account_holder = account_holder
        self.balance = balance
        logger.info(f"Account created for {account_holder} with balance ${balance}")

    def deposit(self, amount: float):
        if amount <= 0:
            logger.warning(f"Deposit amount must be positive. Tried to deposit ${amount}")
            return
        self.balance += amount
        logger.info(f"Deposited ${amount} to {self.account_holder}'s account. New balance: ${self.balance}")

    def withdraw(self, amount: float):
        if amount > self.balance:
            logger.error(f"Insufficient funds: tried to withdraw ${amount}, but balance is ${self.balance}")
            raise ValueError("Insufficient funds")
        if amount > 1000:  # Daily withdrawal limit
            logger.warning(f"Attempted withdrawal of ${amount} exceeds daily limit of $1000. This transaction will be skipped.")
            return  # Skip the transaction without raising an error
        self.balance -= amount
        logger.info(f"Withdrew ${amount} from {self.account_holder}'s account. New balance: ${self.balance}")

def process_transactions():
    # Simulate bank transactions
    account = BankAccount("Customer A", 5000)

    # Deposit money
    account.deposit(1500)  # Normal deposit
    account.deposit(-100)  # Invalid deposit (negative amount)

    # Withdraw money
    try:
        account.withdraw(500)  # Valid withdrawal
        account.withdraw(1200)  # Exceeds daily limit (warning)
        account.withdraw(7000)  # Insufficient funds (error)
    except ValueError as e:
        logger.exception(f"Transaction failed: {e}")

if __name__ == "__main__":
    process_transactions()
