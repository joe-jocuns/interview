from flask import Flask, request, jsonify, render_template
import random
import datetime
import string

app = Flask(__name__)

payments = []

characters = string.ascii_letters + string.digits

def random_date_string():
    start = datetime.datetime(2025, 1, 1)
    end = datetime.datetime.now()
    delta = end - start;
    seconds = random.randint(0, int(delta.total_seconds()))
    random_date = start + datetime.timedelta(seconds=seconds)
    return random_date.isoformat()

def seed_data():
    for i in range(1,100):
        payments.append({
            "transactionId": f"{i}_{''.join(random.choice(characters) for _ in range(4))}",
            "memo": ''.join(random.choice(characters) for _ in range(10)),
            "amount": random.randint(200, 1000),
            "status": random.choice(["Success", "Declined"]),
            "timestamp": random_date_string()
        })



seed_data()


def add_payment_record(amount, memo):
    payments.append({
        "transactionId": f"{len(payments)}_{''.join(random.choice(characters) for _ in range(4))}",
        "memo": memo,
        "amount": amount,
        "status": "Success",
        "timestamp": datetime.datetime.now().isoformat()
    })
    print("Added Payment")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/payments', methods=['POST'])
def add_payment_route():
    amount = request.form.get("amount")
    memo = request.form.get("memo")

    if not amount or not memo:
        return jsonify({"error": "Amount and memo required"}), 400

    add_payment_record(amount, memo)

    return jsonify({"message": "Payment added"}), 201


@app.route('/payments', methods=['GET'])
def list_payments():
    return jsonify(payments)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
