import datetime
import calendar

class PaymentUtils():

	@staticmethod
	def get_remaining_days():
		now = datetime.datetime.now()
		total_days = calendar.monthrange(now.year, now.month)[1]
		remaining_days = total_days - now.day + 1
		return remaining_days, total_days

	@staticmethod
	def get_discounted_amount(plan_amount, remaining_days, total_days):
		if plan_amount<0:
			return 0
		prorated_amount = round(plan_amount * remaining_days / total_days, 2)
		discounted_amount = str(plan_amount - prorated_amount)
		return discounted_amount, prorated_amount

	@staticmethod
	def display_transaction_recurring(plan, plan_amount, remaining_days, total_days, prorated_amount):
		print("  plan: {} - {} USD".format(plan, plan_amount))
		print("  remaining days  : {} / {}".format(remaining_days, total_days))
		print("  prorated amount : {} USD".format(prorated_amount))
		print("  recurring amount: {} USD".format(plan_amount))


	@staticmethod
	def process_transaction_recurring(braintree, plan, plan_amount, type, nonce, customer):
		payment_method = braintree.create_payment_method(customer.id, nonce)
		if payment_method:
			remaining_days, total_days = PaymentUtils.get_remaining_days()
			discounted_amount, prorated_amount = PaymentUtils.get_discounted_amount(plan_amount, remaining_days, total_days)

			# succeeding recurrent months
			subscription = braintree.create_subscription(plan, payment_method.token)
			if not subscription:
				print("_create_subscription failed!")
				return False, ""

			# current prorated month
			transaction = braintree.create_transaction_by_token(prorated_amount, payment_method.token)
			if not transaction:
				print("_create_subscription failed!")
				return False, ""

			PaymentUtils.display_transaction_recurring(plan, plan_amount, remaining_days, total_days, prorated_amount)
		else:
			print("_create_payment_method failed!")
			return False, ""
		#print(result)

		display = "User subscribed successfully! {} USD for current month, {} USD for succeeding months".format(prorated_amount, plan_amount)
		print(display)
		print()
		return True, display