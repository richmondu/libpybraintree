import braintree
import payment.braintree_config as braintree_config
from payment.payment_client_interface import PaymentClientInterface


class BrainTreeClient(PaymentClientInterface):

	def __init__(self):
		mode = braintree.Environment.Production if braintree_config.CONFIG_MODE=="live" else braintree.Environment.Sandbox
		self.configuration = braintree.Configuration(
			mode,
			merchant_id = braintree_config.CONFIG_MERCHANT_ID,
			public_key  = braintree_config.CONFIG_PUBLIC_KEY,
			private_key = braintree_config.CONFIG_PRIVATE_KEY
		)
		self.gateway = braintree.BraintreeGateway(self.configuration)


	'''
	' plans
	'''
	def get_plans(self):
		print("Getting subscription plans...")
		self.plans = self.gateway.plan.all()
		return self.plans

	def display_plans(self):
		for plan in self.plans:
			print("{}".format(plan.id))
			print("{}".format(plan.name))
			print("{}".format(plan.merchant_id))
			print("{}".format(plan.billing_day_of_month))
			print("{}".format(plan.billing_frequency))
			print("{}".format(plan.number_of_billing_cycles))
			print("{}".format(plan.currency_iso_code))
			print("{}".format(plan.price))
			print("{}".format(plan.trial_duration))
			print("{}".format(plan.trial_duration_unit))
			print("{}".format(plan.trial_period))
			print("{}".format(plan.created_at))
			print("{}".format(plan.updated_at))
			print("{}".format(plan.add_ons))
			print("{}".format(plan.discounts))
			print("{}".format(plan.description))
			print()

	'''
	' authentication
	'''
	def generate_client_token(self):
		print("Creating client token...")
		client_token = self.gateway.client_token.generate()
		return client_token


	'''
	' customer
	'''
	def create_customer(self, customer_details):
		print("Creating customer information...")
		result = self.gateway.customer.create({
			"first_name": customer_details["firstName"],
			"last_name": customer_details["lastName"],
			"email":customer_details["email"],
		})
		print("  id: {}".format(result.customer.id))
		return result.customer

	def get_customer(self, customer_details):
		print("Getting customer information...")
		collection = self.gateway.customer.search(braintree.CustomerSearch.email == customer_details["email"])
		for customer in collection.items:
			if customer.first_name == customer_details["firstName"] and customer.last_name == customer_details["lastName"]:
				return customer
		return customer


	'''
	' payment method
	'''
	def create_payment_method(self, customer_id, nonce):
		print("Creating payment method...")
		result = self.gateway.payment_method.create({
			"customer_id": customer_id,
			"payment_method_nonce": nonce
		})
		if not result.is_success:
			print(result)
			print('Cannot use a payment_method_nonce more than once.')
			return None
		return result.payment_method


	'''
	' transaction
	'''
	def create_transaction_by_nonce(self, amount, nonce):
		print("Creating transaction...")
		options = {
			'amount': str(amount),
			'payment_method_nonce': nonce,
			'options': {
				"submit_for_settlement": True
			}
		}
		result = self.gateway.transaction.sale(options)
		if not result.is_success:
			print("Failed")
			return None
		return result.transaction

	def create_transaction_by_token(self, amount, token):
		print("Creating transaction...")
		options = {
			'amount': str(amount),
			'payment_method_token': token,
			'options': {
				"submit_for_settlement": True
			}
		}
		result = self.gateway.transaction.sale(options)
		if not result.is_success:
			print("Failed")
			return None
		return result.transaction

	def commit_transaction(self, tid):
		print("Committing transaction...")
		return self.gateway.transaction.submit_for_settlement(tid)

	def find_transaction(self, tid):
		print("Finding transaction...")
		return self.gateway.transaction.find(tid)


	'''
	' subscription
	'''
	def create_subscription(self, plan, payment_method_token):
		print("Creating subscription...")
		options = {
			'payment_method_token': payment_method_token, 
			'plan_id': plan
		}
		result = self.gateway.subscription.create(options)
		# current month prorated, charged immediately
		# prorated_amount = plan_amt*(total_days-remaining_days)/total_days
		# discounted_amount = plan_amount - prorated_amount
		# plan_amount = plan_amount - discounted_amount
		# result = self.gateway.subscription.create({
		# 	'payment_method_token': payment_method_token, 
		# 	'plan_id': plan,
		# 	"options": {
		# 		"start_immediately": True # overwrite to 
		# 	},
		# 	'never_expires': False,
		# 	"number_of_billing_cycles": 1,
		# 	"discounts": {
		# 		"add": [
		# 			{
		# 				"inherited_from_id": "ProrationDiscount",
		# 				"amount": discounted_amount,
		# 				"never_expires": False,
		# 				"number_of_billing_cycles": 1
		# 			}
		# 		]
		# 	}
		# })

		if not result.is_success:
			print(result)
			return None
		return result.subscription

	def update_subscription(self, sub_id, options):
		result = self.gateway.subscription.update(sub_id, options)
		if not result.is_success:
			print(result)
			return None
		return result.subscription

	def cancel_subscription(self, sub_id):
		result = self.gateway.subscription.cancel(sub_id)
		if not result.is_success:
			print(result)
			return None
		return result.subscription
