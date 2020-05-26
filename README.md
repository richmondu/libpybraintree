# libpybraintree

libpybraintree demonstrates usage of <b>Braintree's Python SDK</b> for processing online <b>recurring payments</b> including payment using Paypal.

To use Paypal library directly, refer to https://github.com/richmondu/libpypaypal
That repository demonstrates how to use the Paypal Python SDK for both normal payments and recurring payments.

Using <b>Braintree</b> library is easier than Paypal library itself. Braintree is a lot more developer-friendly.
Moreover, Braintree support <b>different payment methods</b> including Paypal, Apple Pay, Google Pay, thus making your web/mobile payment system more robust.
For recurring payments feature, it supports seating plans, provisioning for discounts/addons, dashboard metrics, etc.
Their web app console is far better and more useful compared to Paypal.


### Instructions:

1. Link BrainTree (sandbox) to the Paypal (sandbox) developer account
   -  If you dont have a Paypal sandbox account yet, refer to https://github.com/richmondu/libpypaypal
   -  The transaction histories will appear on both Braintree and Paypal accounts.

2. Create plans in Braintree (Seating plan)
   -  Ex. Basic10, Pro30, Enterprise50 

3. Copy the Braintree configuration in braintree_config.py

4. Run braintee_manager.bat
   -  This will open up a Google Chrome browser running index.html and run braintree_manager.py application

5. Note: When a customer buys a plan for a device, <b>2 BrainTree subscriptions are created</b> both pointing to one of the 3 plans above:
   -  <b>1 for the prorated current month</b> , charged immediately, one cycle only, same plan but with discount based on the remaining days of the month
   -  <b>1 for succeeding recurring months</b>, charged every 1st day of the month, infinite cycle



### Basic Flow:

0. Frontend uses Drop-in UI (copy paste code for UI) provided by BrainTree
   - https://developers.braintreepayments.com/start/hello-client/javascript/v3
   - https://developers.braintreepayments.com/start/hello-client/android/v3
   - https://developers.braintreepayments.com/start/hello-client/ios/v4

1. Frontend gets client_token authorization from backend
   - Paypal - approval url; Braintree - client_token 

2. Backend retrieves client_token authorization from BrainTree and returns it to frontend

3. Frontend uses client_token to redirect to Paypal page for user consent

4. Customer approves payment

5. Frontend retrieves a NONCE from the dropin UI 
   - Paypal - payer ID; Braintree - nonce

6. Frontend passes NONCE to backend (together with payer details)

7. Backend creates 2 subscriptions pointing to the same plan (using the NONCE)
   -  <b>1 for the prorated current month</b> , charged immediately, one cycle only, same plan but with discount based on the remaining days of the month
      same plan but with discount, used discounts to subtract the prorated_amount = plan_amt - plan_amt*(total_days-remaining_days)/total_days
   -  <b>1 for succeeding recurring months</b>, charged every 1st day of the month, infinite cycle
   
   - For Paypal, we use <b>setup_fee for prorated month</b>
   - For Braintree, we use <b>another subscription for prorated month</b>



### Backend/Frontend Changes:

To transition from Paypal library to Braintree library, most of the changes are in the backend.

For the frontend, the only risk is integrating the Braintree DropIn UI.
How easy or difficult it is to integrate Braintree DropIn UI in Android or IOS apps is the major concern.
For web app, its really simple as in copy-paste.

Braintree changes in the frontend:
1. Frontend needs to add some Braintree DropIn UI, to display the various payment options and direct the user to corresponding payment page.
   - https://developers.braintreepayments.com/start/hello-client/android/v3 
   - https://developers.braintreepayments.com/start/hello-client/ios/v4
2. For Braintree, we retrieve client_token instead of approval url.
   - Paypal - approval url, payment id; Braintree - client_token
3. Then once user completes the payment, frontend sends NONCE string instead of payerID
   - Paypal - payer id, payment id; Braintree - nonce



### Screenshots

<img src="./_images/braintree_paypal.png" width="1000"/>

<img src="./_images/braintree_paypal_1.png" width="1000"/>

<img src="./_images/braintree_paypal_2.png" width="1000"/>

<img src="./_images/braintree_paypal_3.png" width="1000"/>

<img src="./_images/braintree_paypal_4.png" width="1000"/>

<img src="./_images/braintree_paypal_5.png" width="1000"/>



### Resources:

1. Braintree https://www.braintreepayments.com/
2. Braintree Paypal payment https://developers.braintreepayments.com/guides/paypal/overview
3. Braintree recurring billing https://developers.braintreepayments.com/guides/recurring-billing/overview

