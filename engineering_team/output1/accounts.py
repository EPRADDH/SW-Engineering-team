class Account:
    def __init__(self, user_id: str, initial_deposit: float) -> None:
        self.user_id = user_id
        self.cash_balance = initial_deposit
        self.holdings = {}
        self.transactions = []
        self.initial_deposit = initial_deposit

    def deposit_funds(self, amount: float) -> None:
        self.cash_balance += amount
        self.transactions.append(('Deposit', amount))

    def withdraw_funds(self, amount: float) -> bool:
        if amount <= self.cash_balance:
            self.cash_balance -= amount
            self.transactions.append(('Withdrawal', amount))
            return True
        return False

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        price = get_share_price(symbol)
        total_cost = price * quantity
        if total_cost <= self.cash_balance:
            self.cash_balance -= total_cost
            if symbol in self.holdings:
                self.holdings[symbol] += quantity
            else:
                self.holdings[symbol] = quantity
            self.transactions.append(('Buy', symbol, quantity))
            return True
        return False

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if symbol in self.holdings and quantity <= self.holdings[symbol]:
            price = get_share_price(symbol)
            total_revenue = price * quantity
            self.holdings[symbol] -= quantity
            if self.holdings[symbol] == 0:
                del self.holdings[symbol]
            self.cash_balance += total_revenue
            self.transactions.append(('Sell', symbol, quantity))
            return True
        return False

    def get_portfolio_value(self) -> float:
        total_value = self.cash_balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def get_profit_or_loss(self) -> float:
        total_portfolio_value = self.get_portfolio_value()
        return total_portfolio_value - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.holdings.copy()

    def get_transactions(self) -> list:
        return self.transactions.copy()


def get_share_price(symbol: str) -> float:
    prices = {'AAPL': 150.0, 'TSLA': 700.0, 'GOOGL': 2800.0}
    return prices.get(symbol, 0.0)