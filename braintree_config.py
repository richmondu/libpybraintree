import os


class config:

    CONFIG_MODE                   = "sandbox" # sandbox or live
    CONFIG_MERCHANT_ID            = os.environ["BRAINTREE_MERCHANT_ID"]
    CONFIG_PUBLIC_KEY             = os.environ["BRAINTREE_PUBLIC_KEY"]
    CONFIG_PRIVATE_KEY            = os.environ["BRAINTREE_PRIVATE_KEY"]
