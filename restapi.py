from flask import Flask, request
from flask_cors import CORS
from payment.app import PaymentApp



app = Flask(__name__)
CORS(app)


def initialize():
	paymentapp = PaymentApp(app)


if __name__ == '__main__':
	initialize()
	app.run(host='0.0.0.0', port=8000, debug=True)

