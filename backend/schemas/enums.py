from enum import StrEnum


class CashFlowType(StrEnum):
    INCOME = "income"
    EXPENSE = "expense"


class AccountType(StrEnum):
    CHECKING = "checking"
    SAVINGS = "savings"
    CASH = "cash"
    INVESTMENT = "investment"
