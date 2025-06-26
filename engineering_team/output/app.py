import gradio as gr
from accounts import Account

# Create an account instance for demonstration
account = None

def create_account(username: str, initial_deposit: float):
    global account
    account = Account(username, initial_deposit)
    return f"Account created for {username} with initial deposit of ${initial_deposit}"

def deposit_funds(amount: float):
    if account:
        account.deposit(amount)
        return f"Deposited: ${amount}. New balance: ${account.balance}"
    return "No account found."

def withdraw_funds(amount: float):
    if account:
        success = account.withdraw(amount)
        if success:
            return f"Withdrew: ${amount}. New balance: ${account.balance}"
        return "Insufficient funds for withdrawal."
    return "No account found."

def buy_shares(symbol: str, quantity: int):
    if account:
        success = account.buy_shares(symbol, quantity)
        if success:
            return f"Bought {quantity} shares of {symbol}. New balance: ${account.balance}"
        return "Insufficient funds or invalid transaction."
    return "No account found."

def sell_shares(symbol: str, quantity: int):
    if account:
        success = account.sell_shares(symbol, quantity)
        if success:
            return f"Sold {quantity} shares of {symbol}. New balance: ${account.balance}"
        return "Not enough shares to sell or invalid transaction."
    return "No account found."

def portfolio_value():
    if account:
        return f"Total portfolio value: ${account.get_portfolio_value()}"
    return "No account found."

def profit_or_loss():
    if account:
        return f"Profit/Loss: ${account.get_profit_or_loss()}"
    return "No account found."

def report_holdings():
    if account:
        holdings = account.get_holdings()
        return f"Current holdings: {holdings}"
    return "No account found."

def list_transactions():
    if account:
        transactions = account.list_transactions()
        return f"Transactions: {transactions}"
    return "No account found."

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# Account Management System")
    username = gr.Textbox(label="Username")
    initial_deposit = gr.Number(label="Initial Deposit")
    create_btn = gr.Button("Create Account")
    result_box = gr.Textbox(label="Result", interactive=False)
    create_btn.click(create_account, inputs=[username, initial_deposit], outputs=result_box)

    deposit_amount = gr.Number(label="Deposit Amount")
    deposit_btn = gr.Button("Deposit")
    deposit_btn.click(deposit_funds, inputs=deposit_amount, outputs=result_box)

    withdraw_amount = gr.Number(label="Withdraw Amount")
    withdraw_btn = gr.Button("Withdraw")
    withdraw_btn.click(withdraw_funds, inputs=withdraw_amount, outputs=result_box)

    buy_symbol = gr.Textbox(label="Stock Symbol to Buy")
    buy_quantity = gr.Number(label="Quantity to Buy")
    buy_btn = gr.Button("Buy Shares")
    buy_btn.click(buy_shares, inputs=[buy_symbol, buy_quantity], outputs=result_box)

    sell_symbol = gr.Textbox(label="Stock Symbol to Sell")
    sell_quantity = gr.Number(label="Quantity to Sell")
    sell_btn = gr.Button("Sell Shares")
    sell_btn.click(sell_shares, inputs=[sell_symbol, sell_quantity], outputs=result_box)

    portfolio_btn = gr.Button("View Portfolio Value")
    portfolio_btn.click(portfolio_value, outputs=result_box)

    profit_btn = gr.Button("View Profit/Loss")
    profit_btn.click(profit_or_loss, outputs=result_box)

    holdings_btn = gr.Button("Report Holdings")
    holdings_btn.click(report_holdings, outputs=result_box)

    transactions_btn = gr.Button("List Transactions")
    transactions_btn.click(list_transactions, outputs=result_box)

demo.launch()