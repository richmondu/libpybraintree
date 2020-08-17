import json
from flask import Blueprint, request
from payment.app_init import payment_client
from payment.blueprint_utils import PaymentUtils



blueprint_transaction = Blueprint('blueprint_transaction', __name__)

# /payment/transaction/checkout
@blueprint_transaction.route("/checkout", methods=['POST'])
def process_transaction():

	data = request.get_json()
	if data is None:
		return json.dumps({'status': 'NG'})
	if data["plan"] is None or data["nonce"] is None or data["type"] is None or data["customer_details"] is None:
		return json.dumps({'status': 'NG'})
	print("\nnonce:\n{}\n".format(data["nonce"]))

	plan_amount = PaymentUtils.get_plan_amount(payment_client.get_plans(), data["plan"])
	remaining_days, total_days = PaymentUtils.get_remaining_days()
	discounted_amount, prorated_amount = PaymentUtils.get_discounted_amount(plan_amount, remaining_days, total_days)

	# get or create customer
	customer = payment_client.get_customer(data["customer_details"])
	if customer is None:
		customer = payment_client.create_customer(data["customer_details"])

	# create payment method
	payment_method = payment_client.create_payment_method(customer.id, data["nonce"])
	if payment_method is None:
		return json.dumps({'status': 'NG'})

	# process succeeding recurrent months
	subscription = payment_client.create_subscription(data["plan"], payment_method.token)
	if not subscription:
		return json.dumps({'status': 'NG'})

	# process current prorated month
	transaction = payment_client.create_transaction_by_token(prorated_amount, payment_method.token)
	if not transaction:
		return json.dumps({'status': 'NG'})

	PaymentUtils.display_transaction_recurring(data["plan"], plan_amount, remaining_days, total_days, prorated_amount)
	return json.dumps({'status': 'OK', 'msg': "User subscribed successfully! {} USD for current month, {} USD for succeeding months".format(prorated_amount, plan_amount)})


