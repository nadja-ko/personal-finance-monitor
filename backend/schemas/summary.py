from decimal import Decimal

from pydantic import BaseModel


class CashFlowSummary(BaseModel):
    income: Decimal
    expenses: Decimal
    net_cash_flow: Decimal
