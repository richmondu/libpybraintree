import braintree
from braintree_config import config as braintree_config
import calendar
import datetime
import json



class braintree_client:

	def __init__(self):
		mode = braintree.Environment.Production if braintree_config.CONFIG_MODE=="live" else braintree.Environment.Sandbox
		self.configuration = braintree.Configuration(
			mode,
			merchant_id = braintree_config.CONFIG_MERCHANT_ID,
			public_key = braintree_config.CONFIG_PUBLIC_KEY,
			private_key = braintree_config.CONFIG_PRIVATE_KEY
		)

	def initialize(self):
		self.gateway = braintree.BraintreeGateway(self.configuration)

	def generate_client(self):
		client_token = self.gateway.client_token.generate()
		return client_token

	def process_transaction_recurring(self, PLAN, PLAN_AMOUNT, TYPE, NONCE, EMAIL, FIRST_NAME, LAST_NAME):
		customer_id = self._get_customer_id(EMAIL, FIRST_NAME, LAST_NAME)
		result, payment_method_token = self._create_payment_method(customer_id, NONCE)
		if result:
			remaining_days, total_days = self._get_remaining_days()
			discounted_amount, prorated_amount = self._get_discounted_amount(PLAN_AMOUNT, remaining_days, total_days)

			result = self._create_subscription(PLAN, payment_method_token, discounted_amount, prorated_amount)
			if not result:
				print("_create_subscription failed!")
				return False, ""

			print("  plan: {} - {} USD".format(PLAN, PLAN_AMOUNT))
			print("  remaining days  : {} / {}".format(remaining_days, total_days))
			print("  prorated amount : {} USD".format(prorated_amount))
			print("  recurring amount: {} USD".format(PLAN_AMOUNT))
		else:
			print("_create_payment_method failed!")
			return False, payment_method_token
		#print(result)

		display = "User subscribed successfully! {} USD for current month, {} USD for succeeding months".format(prorated_amount, PLAN_AMOUNT)
		print(display)
		print()
		return True, display

	def process_transaction_basic(self, AMOUNT, NONCE=None, TOKEN=None):
		if NONCE:
			options = {
				'amount': str(AMOUNT),
				'payment_method_nonce': NONCE,
				'options': {
					"submit_for_settlement": True
				}
			}
		else:
			options = {
				'amount': str(AMOUNT),
				'payment_method_token': TOKEN,
				'options': {
					"submit_for_settlement": True
				}
			}
		result = self.gateway.transaction.sale(options)
		if not result.is_success:
			print("Failed")
			return False
		return True

	def _get_customer_id(self, EMAIL, FIRST_NAME, LAST_NAME):
		customer_id = None
		print("Getting customer information...")
		print("  email: {}".format(EMAIL))
		print("  name: {} {}".format(FIRST_NAME, LAST_NAME))
		collection = self.gateway.customer.search(braintree.CustomerSearch.email == EMAIL)
		for customer in collection.items:
			if customer.first_name == FIRST_NAME and customer.last_name == LAST_NAME:
				customer_id = customer.id
				break
		if customer_id == None:
			print("Not found. Creating customer information...")
			result = self.gateway.customer.create({
				"first_name": FIRST_NAME,
				"last_name": LAST_NAME,
				"email": EMAIL,
			})
			customer_id = result.customer.id
		print("  id: {}".format(customer_id))
		return customer_id

	def _create_payment_method(self, customer_id, NONCE):
		print("Creating payment method...")
		result = self.gateway.payment_method.create({
			"customer_id": customer_id,
			"payment_method_nonce": NONCE
		})
		if not result.is_success:
			print(result)
			return False, 'Cannot use a payment_method_nonce more than once.'
		return True, result.payment_method.token

	def _create_subscription(self, plan, payment_method_token, discounted_amount, prorated_amount):
		print("Creating subscription...")
		# succeeding recurrent months
		result = self.gateway.subscription.create({
			'payment_method_token': payment_method_token, 
			'plan_id': plan
		})
		if not result.is_success:
			print(result)
			return False

		# current prorated month
		if True:
			# process as a single transaction
			self.process_transaction_basic(prorated_amount, TOKEN=payment_method_token)
		else:
			# current month prorated, charged immediately
			# prorated_amount = plan_amt*(total_days-remaining_days)/total_days
			# discounted_amount = plan_amount - prorated_amount
			# plan_amount = plan_amount - discounted_amount
			result = self.gateway.subscription.create({
				'payment_method_token': payment_method_token, 
				'plan_id': plan,
				"options": {
					"start_immediately": True # overwrite to 
				},
				'never_expires': False,
				"number_of_billing_cycles": 1,
				"discounts": {
					"add": [
						{
							"inherited_from_id": "ProrationDiscount",
							"amount": discounted_amount,
							"never_expires": False,
							"number_of_billing_cycles": 1
						}
					]
				}
			})

		if not result.is_success:
			print("Failed")
			print(result)
			return False
		return True

	def _get_remaining_days(self):
		now = datetime.datetime.now()
		total_days = calendar.monthrange(now.year, now.month)[1]
		remaining_days = total_days - now.day + 1
		return remaining_days, total_days

	def _get_discounted_amount(self, plan_amount, remaining_days, total_days):
		prorated_amount = round(plan_amount * remaining_days / total_days, 2)
		discounted_amount = str(plan_amount - prorated_amount)
		return discounted_amount, prorated_amount


