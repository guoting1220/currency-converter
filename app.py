from flask import Flask, request, session, render_template, redirect
# from flask_debugtoolbar import DebugToolbarExtension
from forex_python.converter import CurrencyRates, CurrencyCodes, RatesNotAvailableError
from decimal import *
from check_valid import check_currency_code, check_amount, get_error_message_for_invalid_code, get_error_message_for_invalid_amt


app = Flask(__name__)

# app.config['SECRET_KEY'] = "secret"
# debug = DebugToolbarExtension(app)
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


c_rate = CurrencyRates()
c_code = CurrencyCodes()

# usage examples ------------------------
#  c = CurrencyRates()
#  c.convert('USD', 'INR', Decimal('10.45'))
# Decimal('705.09')
#  c.convert('USD', 'INR', 10)
# 674.73


@app.route("/")
def show_form():
    """ home page to show the convertion form """

    return render_template("home.html")


@app.route("/check_valid")
def check_input_valid():
    """ check if the inputs are valid """

    from_cur = request.args.get("convertFrom")
    to_cur = request.args.get("convertTo")
    amt = request.args.get("amount")

    is_from_cur_valid = check_currency_code(from_cur)
    is_to_cur_valid = check_currency_code(to_cur)
    is_amt_valid = check_amount(amt)    

    #  if all valid, render the result page
    if is_from_cur_valid and is_to_cur_valid and is_amt_valid:
        converted_amt = round(c_rate.convert(from_cur, to_cur, Decimal(amt)), 2)

        from_cur_symb = c_code.get_symbol(from_cur)
        to_cur_symb = c_code.get_symbol(to_cur)
        
        return render_template("result.html",
            converted_amt=converted_amt, 
            from_cur_symb=from_cur_symb,
            to_cur_symb=to_cur_symb, amt=amt)

    # if there is any invalid input, render the error message
    from_cur_err = "" if is_from_cur_valid else get_error_message_for_invalid_code(
        from_cur)
    to_cur_err = "" if is_to_cur_valid else get_error_message_for_invalid_code(
        to_cur)
    amt_err = "" if is_amt_valid else get_error_message_for_invalid_amt()

    return render_template("error.html", from_cur_err=from_cur_err, to_cur_err=to_cur_err, amt_err=amt_err)
    

        
   






