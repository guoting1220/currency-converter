from unittest import TestCase
from app import app
from check_valid import check_currency_code, check_amount, get_error_message_for_invalid_code, get_error_message_for_invalid_amt


class FlaskTests(TestCase):

    def test_homepage(self):
        """test the home page"""
        
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Converting from', html)

       
    def test_code_valid_function(self):
        """ test check_currency_code(code) function """

        self.assertEqual(check_currency_code("USD"), True)
        self.assertEqual(check_currency_code("xxx"), False)
        self.assertEqual(check_currency_code(""), False)


    def test_amount_valid_function(self):
        """ test check_amount(amt) function """

        self.assertEqual(check_amount("1"), True)
        self.assertEqual(check_amount("1.11111"), True)
        self.assertEqual(check_amount("0"), True)
        self.assertEqual(check_amount(""), False)


    def test_get_error_msg_function(self):
        """ test get error message function """

        self.assertEqual(get_error_message_for_invalid_code(""), "Invalid currency code")
        self.assertEqual(get_error_message_for_invalid_amt(), "The amount can not be empty")

        
    def test_result_page(self):
        """ test if result page show convertion correctly """

        with app.test_client() as client:
            res = client.get(
                "/check_valid?convertFrom=INR&convertTo=CNY&amount=1")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('₹', html)
            self.assertIn('¥', html)
            self.assertIn('0.09', html)
            self.assertIn('=', html)
            self.assertNotIn('Invalid currency code', html)
            self.assertNotIn('The amount can not be empty', html)

    
    def test_error_page(self):
        """ test if the error message showing correctly """

        with app.test_client() as client:
            res = client.get("/check_valid?convertFrom=xxx&convertTo=CNY&amount=1")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Invalid currency code", html)
            self.assertNotIn('￥', html)

            res = client.get(
                "/check_valid?convertFrom=USD&convertTo=CNY&amount=")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("The amount can not be empty", html)
            self.assertNotIn('$', html)

            res = client.get(
                "/check_valid?convertFrom=&convertTo=xx&amount=")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("The amount can not be empty", html)
            self.assertIn("Invalid currency code", html)




