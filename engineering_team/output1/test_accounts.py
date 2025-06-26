import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account(user_id='user123', initial_deposit=1000.0)

    def test_initial_balance(self):
        self.assertEqual(self.account.cash_balance, 1000.0)

    def test_deposit_funds(self):
        self.account.deposit_funds(500.0)
        self.assertEqual(self.account.cash_balance, 1500.0)
        self.assertEqual(self.account.get_transactions(), [('Deposit', 500.0)])

    def test_withdraw_funds_success(self):
        result = self.account.withdraw_funds(200.0)
        self.assertTrue(result)
        self.assertEqual(self.account.cash_balance, 800.0)
        self.assertEqual(self.account.get_transactions(), [('Deposit', 500.0), ('Withdrawal', 200.0)])

    def test_withdraw_funds_failure(self):
        result = self.account.withdraw_funds(2000.0)
        self.assertFalse(result)
        self.assertEqual(self.account.cash_balance, 800.0)

    def test_buy_shares_success(self):
        result = self.account.buy_shares('AAPL', 2)
        self.assertTrue(result)
        self.assertEqual(self.account.cash_balance, 700.0)
        self.assertEqual(self.account.get_holdings(), {'AAPL': 2})
        self.assertEqual(self.account.get_transactions(), [('Deposit', 500.0), ('Withdrawal', 200.0), ('Buy', 'AAPL', 2)])

    def test_buy_shares_failure(self):
        result = self.account.buy_shares('AAPL', 10)
        self.assertFalse(result)
        self.assertEqual(self.account.cash_balance, 700.0)

    def test_sell_shares_success(self):
        self.account.buy_shares('AAPL', 2)
        result = self.account.sell_shares('AAPL', 1)
        self.assertTrue(result)
        self.assertEqual(self.account.cash_balance, 850.0)
        self.assertEqual(self.account.get_holdings(), {'AAPL': 1})
        self.assertEqual(self.account.get_transactions(), [('Deposit', 500.0), ('Withdrawal', 200.0), ('Buy', 'AAPL', 2), ('Sell', 'AAPL', 1)])

    def test_sell_shares_failure(self):
        result = self.account.sell_shares('AAPL', 1)
        self.assertFalse(result)

    def test_get_portfolio_value(self):
        self.account.deposit_funds(500.0)
        self.account.buy_shares('AAPL', 2)
        value = self.account.get_portfolio_value()
        self.assertEqual(value, 700.0 + (150.0 * 2))

    def test_get_profit_or_loss(self):
        self.account.deposit_funds(500.0)
        self.account.buy_shares('AAPL', 2)
        profit_loss = self.account.get_profit_or_loss()
        self.assertEqual(profit_loss, (700.0 + (150.0 * 2)) - 1000.0)

if __name__ == '__main__':
    unittest.main()