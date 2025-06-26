```python
# app.py
import gradio as gr
from accounts import Account, get_share_price

# Initialize the account with a demo user and initial deposit
user_account = Account(user_id="demo_user", initial_deposit=10000.0)

def create_account(user_id: str, initial_deposit: float):
    global user_account
    user_account = Account(user_id=user_id, initial_deposit=initial_deposit)
    return "Account created!", user_account.cash_balance, user_account.get_holdings(), user_account.get_transactions()

def deposit(amount: float):
    user_account.deposit_funds(amount)
    return user_account.cash_balance, user_account.get_holdings(), user_account.get_transactions()

def withdraw(amount: float):
    success = user_account.withdraw_funds(amount)
    if success:
        return user_account.cash_balance, user_account.get_holdings(), user_account.get_transactions(), "Withdrawal successful"
    else:
        return user_account.cash_balance, user_account.get_holdings(), user_account.get_transactions(), "Insufficient funds"

def buy(symbol: str, quantity: int):
    success = user_account.buy_shares(symbol, quantity)
    if success:
        return user_account.cash_balance, user_account.get_holdings(), user_account.get_transactions(), f"Bought {quantity} shares of {symbol}"
    else:
        return user_account.cash_balance, user_account.get_holdings(), user_account.get_transactions(), "Cannot buy shares, check your balance or share symbol"

def sell(symbol: str, quantity: int):
    success = user_account.sell_shares(symbol, quantity)
    if success:
        return user_account.cash_balance, user_account.get_holdings(), user_account.get_transactions(), f"Sold {quantity} shares of {symbol}"
    else:
        return user_account.cash_balance, user_account.get_holdings(), user_account.get_transactions(), "Cannot sell shares, check holdings or share symbol"

def portfolio_value():
    value = user_account.get_portfolio_value()
    return value

def profit_or_loss():
    pnl = user_account.get_profit_or_loss()
    return pnl

with gr.Blocks() as demo:
    gr.Markdown("### Trading Simulation Platform")

    with gr.TabItem("Account Management"):
        user_id_input = gr.Textbox(label="User ID")
        initial_deposit_input = gr.Number(label="Initial Deposit")
        create_btn = gr.Button("Create Account")
        create_output = gr.Textbox(label="Status")
        cash_output = gr.Number(label="Cash Balance")
        holdings_output = gr.JSON(label="Holdings")
        transactions_output = gr.JSON(label="Transactions")

        create_btn.click(
            create_account,
            inputs=[user_id_input, initial_deposit_input],
            outputs=[create_output, cash_output, holdings_output, transactions_output]
        )

    with gr.TabItem("Transactions"):
        deposit_input = gr.Number(label="Deposit Amount")
        deposit_btn = gr.Button("Deposit")
        withdraw_input = gr.Number(label="Withdraw Amount")
        withdraw_btn = gr.Button("Withdraw")
        transaction_output = gr.Textbox(label="Transaction Status", interactive=False)

        deposit_btn.click(
            deposit,
            inputs=[deposit_input],
            outputs=[cash_output, holdings_output, transactions_output, transaction_output]
        )
        withdraw_btn.click(
            withdraw,
            inputs=[withdraw_input],
            outputs=[cash_output, holdings_output, transactions_output, transaction_output]
        )

    with gr.TabItem("Trading"):
        symbol_input = gr.Textbox(label="Stock Symbol")
        buy_quantity_input = gr.Number(label="Buy Quantity")
        sell_quantity_input = gr.Number(label="Sell Quantity")
        buy_btn = gr.Button("Buy")
        sell_btn = gr.Button("Sell")
        trading_output = gr.Textbox(label="Trading Status", interactive=False)

        buy_btn.click(
            buy,
            inputs=[symbol_input, buy_quantity_input],
            outputs=[cash_output, holdings_output, transactions_output, trading_output]
        )
        sell_btn.click(
            sell,
            inputs=[symbol_input, sell_quantity_input],
            outputs=[cash_output, holdings_output, transactions_output, trading_output]
        )

    with gr.TabItem("Portfolio"):
        portfolio_value_btn = gr.Button("Get Portfolio Value")
        portfolio_value_output = gr.Number(label="Portfolio Value")

        portfolio_value_btn.click(
            portfolio_value,
            inputs=[],
            outputs=[portfolio_value_output]
        )

        profit_or_loss_btn = gr.Button("Get Profit or Loss")
        profit_or_loss_output = gr.Number(label="Profit/Loss")

        profit_or_loss_btn.click(
            profit_or_loss,
            inputs=[],
            outputs=[profit_or_loss_output]
        )

demo.launch()
```

This code provides a simple Gradio UI to interact with the account management system defined in the `accounts.py`. It allows users to create an account, deposit and withdraw funds, buy and sell shares, and view the portfolio value and profit/loss. The app is divided into tabs to organize different functionalities.