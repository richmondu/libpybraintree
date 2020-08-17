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
		discounted_amount = plan_amount - prorated_amount
		return discounted_amount, prorated_amount

	@staticmethod
	def get_plan_amount(plans, plan_id):
		for plan in plans:
			if plan.id == plan_id:
				return float(plan.price)
		return None

	@staticmethod
	def display_transaction_recurring(plan, plan_amount, remaining_days, total_days, prorated_amount):
		print("  plan: {} - {} USD".format(plan, plan_amount))
		print("  remaining days  : {} / {}".format(remaining_days, total_days))
		print("  prorated amount : {} USD".format(prorated_amount))
		print("  recurring amount: {} USD".format(plan_amount))
