import unittest

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account('test_user', 1000.0)

    def test_initialization(self):
        self.assertEqual(self.account.username, 'test_user')
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.shares, {})
        self.assertEqual(self.account.transactions, [])

    def test_deposit(self):
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertIn('Deposited: $500.0', self.account.transactions)

    def test_withdraw_success(self):
        result = self.account.withdraw(200.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 800.0)
        self.assertIn('Withdrew: $200.0', self.account.transactions)

    def test_withdraw_failure(self):
        result = self.account.withdraw(1100.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)

    def test_buy_shares_success(self):
        result = self.account.buy_shares('AAPL', 5)
        self.assertTrue(result)
        self.assertEqual(self.account.shares['AAPL'], 5)
        self.assertIn('Bought 5 shares of AAPL at $150.0 each', self.account.transactions)

    def test_buy_shares_failure(self):
        result = self.account.buy_shares('GOOGL', 1)
        self.assertFalse(result)
        self.assertNotIn('GOOGL', self.account.shares)

    def test_sell_shares_success(self):
        self.account.buy_shares('TSLA', 1)
        result = self.account.sell_shares('TSLA', 1)
        self.assertTrue(result)
        self.assertNotIn('TSLA', self.account.shares)
        self.assertIn('Sold 1 shares of TSLA at $700.0 each', self.account.transactions)

    def test_sell_shares_failure(self):
        result = self.account.sell_shares('AAPL', 1)
        self.assertFalse(result)
        self.assertNotIn('Sold 1 shares of AAPL at $150.0 each', self.account.transactions)

    def test_get_portfolio_value(self):
        self.account.buy_shares('AAPL', 1)
        self.assertEqual(self.account.get_portfolio_value(), 850.0)

    def test_get_profit_or_loss(self):
        self.account.deposit(500.0)
        self.account.buy_shares('AAPL', 1)
        self.assertEqual(self.account.get_profit_or_loss(), -150.0)

    def test_list_transactions(self):
        self.account.deposit(500.0)
        self.assertEqual(self.account.list_transactions(), ['Deposited: $500.0'])

    def test_get_holdings(self):
        self.account.buy_shares('AAPL', 5)
        self.assertEqual(self.account.get_holdings(), {'AAPL': 5})

if __name__ == '__main__':
    unittest.main()