import json
from flask import Blueprint
from payment.app_init import payment_client



blueprint_authentication = Blueprint('blueprint_authentication', __name__)

# /payment/authentication/client_token
@blueprint_authentication.route("/client_token", methods=['GET'])
def get_client_token():

	token = payment_client.generate_client_token()
	print("\nclient_token:\n{}\n".format(token))
	return json.dumps({'status': 'OK', 'token': token})


