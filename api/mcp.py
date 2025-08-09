from mcp.server.fastmcp import FastMCP

mcp = FastMCP()

@mcp.function("split_expense", description="Split an expense equally among participants")
def split_expense(amount: float, people: int):
    if people <= 0:
        return {"error": "Number of people must be greater than zero"}
    per_person = round(amount / people, 2)
    return {
        "per_person": per_person,
        "breakdown": f"₹{per_person} each"
    }

@mcp.function("add_expense", description="Add an expense to the group record")
def add_expense(description: str, amount: float):
    return {"status": "success", "description": description, "amount": amount}

@mcp.function("get_balances", description="Get current balances for group")
def get_balances():
    return {"balances": "Feature not yet implemented"}

@mcp.function("settle_payment", description="Mark a payment as settled")
def settle_payment(payer: str, payee: str, amount: float):
    return {"status": "success", "message": f"{payer} settled ₹{amount} with {payee}"}

app = mcp.app
