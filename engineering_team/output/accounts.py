class Account:
    def __init__(self, username: str, initial_deposit: float):
        """
        Initializes an account for a user with a specific username and initial deposit.

        Args:
        - username (str): The username of the account holder.
        - initial_deposit (float): The starting amount of money in the account.
        """
        self.username = username
        self.balance = initial_deposit
        self.shares = {}
        self.transactions = []

    def deposit(self, amount: float) -> None:
        """
        Deposits funds into the user's account.

        Args:
        - amount (float): The amount of money to deposit.
        """
        self.balance += amount
        self.transactions.append(f'Deposited: ${amount}')

    def withdraw(self, amount: float) -> bool:
        """
        Withdraws funds from the user's account if sufficient funds are available.

        Args:
        - amount (float): The amount of money to withdraw.

        Returns:
        - bool: True if the withdrawal was successful, False otherwise.
        """
        if amount > self.balance:
            return False
        self.balance -= amount
        self.transactions.append(f'Withdrew: ${amount}')
        return True

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        """
        Buys shares for a specific symbol if sufficient funds are available.

        Args:
        - symbol (str): The stock symbol to buy.
        - quantity (int): The number of shares to purchase.

        Returns:
        - bool: True if the purchase was successful, False otherwise.
        """
        total_cost = get_share_price(symbol) * quantity
        if total_cost > self.balance:
            return False
        self.balance -= total_cost
        self.shares[symbol] = self.shares.get(symbol, 0) + quantity
        self.transactions.append(f'Bought {quantity} shares of {symbol} at ${get_share_price(symbol)} each')
        return True

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        """
        Sells shares for a specific symbol if the user holds enough shares.

        Args:
        - symbol (str): The stock symbol to sell.
        - quantity (int): The number of shares to sell.

        Returns:
        - bool: True if the sale was successful, False otherwise.
        """
        if self.shares.get(symbol, 0) < quantity:
            return False
        total_sale_value = get_share_price(symbol) * quantity
        self.balance += total_sale_value
        self.shares[symbol] -= quantity
        if self.shares[symbol] == 0:
            del self.shares[symbol]
        self.transactions.append(f'Sold {quantity} shares of {symbol} at ${get_share_price(symbol)} each')
        return True

    def get_portfolio_value(self) -> float:
        """
        Calculates the current total value of the user's portfolio including cash and assets.

        Returns:
        - float: The total value of the portfolio in dollars.
        """
        total_value = self.balance
        for symbol, quantity in self.shares.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def get_profit_or_loss(self) -> float:
        """
        Calculates the profit or loss based on the initial deposit and the current portfolio value.

        Returns:
        - float: The profit or loss in dollars.
        """
        return self.get_portfolio_value() - self.balance

    def list_transactions(self) -> list:
        """
        Lists all transactions made by the user over time.

        Returns:
        - list: A list of transaction details.
        """
        return self.transactions

    def get_holdings(self) -> dict:
        """
        Reports the current holdings of the user.

        Returns:
        - dict: A dictionary with stock symbols as keys and quantities as values.
        """
        return self.shares

def get_share_price(symbol: str) -> float:
    """
    Retrieves the current price of a share for a given symbol.

    For testing purposes, use fixed prices for certain test symbols.

    Args:
    - symbol (str): The stock symbol whose price is needed.

    Returns:
    - float: The current price of the stock.
    """
    test_prices = {'AAPL': 150.0, 'TSLA': 700.0, 'GOOGL': 2800.0}
    return test_prices.get(symbol, 0.0)