from payment.blueprint_authentication import blueprint_authentication
from payment.blueprint_transaction import blueprint_transaction


class PaymentApp:

    def __init__(self, app):

        app.register_blueprint(blueprint_authentication, url_prefix="/payment/authentication")
        app.register_blueprint(blueprint_transaction, url_prefix="/payment/transaction")
