from forex_python.converter import CurrencyRates, RatesNotAvailableError
from decimal import *

c = CurrencyRates()

"""check if the currency code is valid"""
def check_currency_code(code):
    if code == "":
        return False

    try: c.get_rates(code)
    except RatesNotAvailableError:
        return False

    return True    


"""check if the currency amount is valid"""
def check_amount(amt):
    if amt == "":
        return False

    return True    


""" return the error message for invalid currency code """
def get_error_message_for_invalid_code(cur):
    return "Invalid currency code"



""" return the error message for invalid currency amount """
def get_error_message_for_invalid_amt():
    return "The amount can not be empty"
