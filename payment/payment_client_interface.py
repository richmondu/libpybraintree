class PaymentClientInterface(object):

	'''
	' plans
	'''
	def get_plans(self):
		return None

	def display_plans(self):
		pass

	'''
	' authentication
	'''
	def generate_client_token(self):
		return None


	'''
	' customer
	'''
	def create_customer(self, customer_details):
		return None

	def get_customer(self, customer_details):
		return None


	'''
	' payment method
	'''
	def create_payment_method(self, customer_id, nonce):
		return None


	'''
	' transaction
	'''
	def create_transaction_by_nonce(self, amount, nonce):
		return None

	def create_transaction_by_token(self, amount, token):
		return None

	def commit_transaction(self, tid):
		return None

	def find_transaction(self, tid):
		return None


	'''
	' subscription
	'''
	def create_subscription(self, plan, payment_method_token):
		return None

	def update_subscription(self, sub_id, options):
		return None

	def cancel_subscription(self, sub_id):
		return None
