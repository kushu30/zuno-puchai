import os
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

from mcp_tools import split_expense, add_expense, get_balances, settle_payment

mcp = FastMCP("expense-splitter")

mcp.tool()(split_expense)
mcp.tool()(add_expense)
mcp.tool()(get_balances)
mcp.tool()(settle_payment)

async def app(scope, receive, send):
    if scope["type"] == "http":
        await mcp.run_http(scope, receive, send)
