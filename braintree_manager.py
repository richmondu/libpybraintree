import json
import flask
from flask import Flask
from flask_cors import CORS
from braintree_client import braintree_client



braintree = None
app = Flask(__name__)
CORS(app)



@app.route('/', methods=['GET'])
def index():
	return json.dumps({'status': 'OK'})

# Request:
#   GET /client_token
#   headers: {'Content-Type': 'application/json'}
# Response:
#   {'status': 'OK', 'token': string}
@app.route('/client_token', methods=['GET'])
def get_client_token():
	token = braintree.generate_client()
	print("\nclient_token:\n{}\n".format(token))
	return json.dumps({'status': 'OK', 'token': token})

# Request:
#   POST /nonce
#   headers: {'Content-Type': 'application/json'}
#   data: {
#     'plan':        string, // Subscription plan type Basic10, Pro30, Enterprise50
#     'nonce':       string, // Nonce value returned by Braintree to Frontend
#     'type':        string, // Payment method type - Paypal, CreditCard, Venmo, ApplePay, GooglePay, SamsungPay
#     'details': {
#       'email':     string,
#       'firstName': string,
#       'lastName':  string,
#     }
#   }
# Response:
#   {'status': 'OK', 'msg': string}
@app.route('/nonce', methods=['POST'])
def process_transaction():
	data = flask.request.get_json()
	if data is None:
		return json.dumps({'status': 'NG'})
	if data["plan"] is None or data["nonce"] is None or data["type"] is None or data["details"] is None:
		return json.dumps({'status': 'NG'})

	PLAN, PLAN_AMOUNT = _get_plan_amount(data["plan"])
	NONCE = data["nonce"]
	TYPE = data["type"]

	details = data["details"]
	EMAIL = details["email"]
	FIRST_NAME = details["firstName"]
	LAST_NAME = details["lastName"]

	result, msg = braintree.process_transaction_recurring(PLAN, PLAN_AMOUNT, TYPE, NONCE, EMAIL, FIRST_NAME, LAST_NAME)
	return json.dumps({'status': 'OK', 'msg': msg})

def _get_plan_amount(plan_name):
	plans = [
		{"name": "Basic10",      "amount": "10.00"},
		{"name": "Pro30",        "amount": "30.00"},
		{"name": "Enterprise50", "amount": "50.00"}
	]
	for plan in plans:
		if plan["name"] == plan_name:
			return plan["name"], float(plan["amount"])
	return None, float(0)

def initialize():
	global braintree
	braintree = braintree_client()
	braintree.initialize()


if __name__ == '__main__':
	initialize()
	app.run(host='0.0.0.0', port=8000, debug=True)

