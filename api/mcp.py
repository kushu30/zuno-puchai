from typing import Annotated
from pydantic import Field
from mcp.types import ErrorData, INVALID_PARAMS
from mcp import McpError

expenses = {}

def _get_group(group_id: str):
    if group_id not in expenses:
        expenses[group_id] = []
    return expenses[group_id]

async def split_expense(
    group_id: Annotated[str, Field(description="Group/conversation ID")],
    total: Annotated[float, Field(description="Total amount to split")],
    people: Annotated[list[str], Field(description="List of participant names")]
) -> dict:
    if total <= 0 or not people:
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Invalid amount or empty people list"))
    per_person = round(total / len(people), 2)
    return {
        "per_person": per_person,
        "breakdown": {p: per_person for p in people}
    }

async def add_expense(
    group_id: str,
    description: str,
    amount: float,
    paid_by: str
) -> dict:
    group = _get_group(group_id)
    group.append({"description": description, "amount": amount, "paid_by": paid_by})
    return {"message": f"Added expense '{description}' of {amount} paid by {paid_by}"}

async def get_balances(group_id: str) -> dict:
    group = _get_group(group_id)
    balances = {}
    for exp in group:
        share = exp["amount"] / len(group)
        for p in balances.keys() | {exp["paid_by"]}:
            balances.setdefault(p, 0)
        balances[exp["paid_by"]] -= exp["amount"] - share
        for p in balances:
            if p != exp["paid_by"]:
                balances[p] += share
    return balances

async def settle_payment(group_id: str, payer: str, payee: str, amount: float) -> dict:
    return {"message": f"{payer} settled {amount} with {payee} in group {group_id}"}
