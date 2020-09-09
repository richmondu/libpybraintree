from abc import abstractmethod, ABC

class PaymentClientInterface(ABC):

	'''
	' plans
	'''
	@abstractmethod
	def get_plans(self):
		raise NotImplementedError

	@abstractmethod
	def display_plans(self):
		raise NotImplementedError

	'''
	' authentication
	'''
	@abstractmethod
	def generate_client_token(self):
		raise NotImplementedError


	'''
	' customer
	'''
	@abstractmethod
	def create_customer(self, customer_details):
		raise NotImplementedError

	@abstractmethod
	def get_customer(self, customer_details):
		raise NotImplementedError


	'''
	' payment method
	'''
	@abstractmethod
	def create_payment_method(self, customer_id, nonce):
		raise NotImplementedError


	'''
	' transaction
	'''
	@abstractmethod
	def create_transaction_by_nonce(self, amount, nonce):
		raise NotImplementedError

	@abstractmethod
	def create_transaction_by_token(self, amount, token):
		raise NotImplementedError

	@abstractmethod
	def commit_transaction(self, tid):
		raise NotImplementedError

	@abstractmethod
	def find_transaction(self, tid):
		raise NotImplementedError


	'''
	' subscription
	'''
	@abstractmethod
	def create_subscription(self, plan, payment_method_token):
		raise NotImplementedError

	@abstractmethod
	def update_subscription(self, sub_id, options):
		raise NotImplementedError

	@abstractmethod
	def cancel_subscription(self, sub_id):
		raise NotImplementedError
