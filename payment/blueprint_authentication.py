from flask import Blueprint, jsonify
from payment.app_init import payment_client
from api_logger import ApiLogger



blueprint_authentication = Blueprint('blueprint_authentication', __name__)

# /payment/authentication/client_token
@blueprint_authentication.route("/client_token", methods=['GET'])
@ApiLogger.log
def get_client_token():

	token = payment_client.generate_client_token()
	print("\nclient_token:\n{}\n".format(token))
	return jsonify(status='OK', token=token)


