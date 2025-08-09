import os
from fastmcp import FastMCP
from dotenv import load_dotenv

# load env vars locally
load_dotenv()

from mcp_tools import split_expense, add_expense, get_balances, settle_payment

app = FastMCP("expense-splitter")

# Register tools
app.tool()(split_expense)
app.tool()(add_expense)
app.tool()(get_balances)
app.tool()(settle_payment)

# For local testing
if __name__ == "__main__":
    app.run()
