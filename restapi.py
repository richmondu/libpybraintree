import time
from flask import Flask, request
from flask_cors import CORS
from payment.app import PaymentApp



app = Flask(__name__)
CORS(app)


# decorator
def api_logger(func):

	def wrapper(*args, **kwargs):
		starttime = time.time()
		print("\n>>> {}".format(func.__name__))

		try:
			params = "".join([str(arg) for arg in args])
			print("params:  [{}]".format(params))
		except:
			pass
		try:
			headers = dict(request.headers) 
			#print("headers: [{}]".format(headers))
		except:
			pass
		try:
			data = request.get_json()
			print("data:    [{}]".format(data))
		except:
			pass

		val = func(*args, **kwargs)
		print("<<< {} {:.2f}\n".format(func.__name__, time.time()-starttime))
		return val

	wrapper.__name__ = func.__name__
	return wrapper


def initialize():
	paymentapp = PaymentApp(app)

if __name__ == '__main__':
	initialize()
	app.run(host='0.0.0.0', port=8000, debug=True)

