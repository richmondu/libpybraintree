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

@app.route('/client_token', methods=['GET'])
def get_client_token():
	token = braintree.generate_client()
	return json.dumps({'status': 'OK', 'token': token})

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

def initialize():
	global braintree
	braintree = braintree_client()
	braintree.initialize()


if __name__ == '__main__':
	initialize()
	app.run(host='0.0.0.0', port=8000, debug=True)

