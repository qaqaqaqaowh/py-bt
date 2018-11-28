import braintree
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.environ.get("MERCHANT_ID"),
        public_key=os.environ.get("PUBLIC_KEY"),
        private_key=os.environ.get("PRIVATE_KEY")
    )
)


@app.route("/", methods=["GET"])
def index():
    client_token = gateway.client_token.generate()
    return render_template("index.html", token=client_token)


@app.route("/pay", methods=["POST"])
def pay():
    nonce = request.form.get("bt-nonce")
    result = gateway.transaction.sale({
        "amount": "10.00",
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        }
    })
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
