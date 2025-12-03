from flask import Flask, request, jsonify, render_template
import random
import datetime
import string
import requests
import uuid

app = Flask(__name__)

payments = []

characters = string.ascii_letters + string.digits

def callMockBank(amount, memo):
    try:
        response = requests.post("http://localhost:5002/process", json={"amount": amount, "memo": memo})
        print("Called mock bank")
        return response.json()
    except Exception as e:
        print("Error contacting mock bank:", e)
        return {"status": "declined", "transactionId": None}
    


def randomDateString():
    start = datetime.datetime(2025, 1, 1)
    end = datetime.datetime.now()
    delta = end - start
    seconds = random.randint(0, int(delta.total_seconds()))
    randomDate = start + datetime.timedelta(seconds=seconds)
    return randomDate.isoformat()

def seedData():
    for i in range(1, 101):
        payments.append({
            "transactionId": str(uuid.uuid4()),
            "memo": ''.join(random.choice(characters) for _ in range(10)),
            "amount": random.randint(200, 1000),
            "status": random.choice(["success", "declined"]),
            "timestamp": randomDateString()
        })

seedData()

def addPaymentRecord(amount, memo):
    payments.append({
        "transactionId": f"{len(payments)}_{''.join(random.choice(characters) for _ in range(4))}",
        "memo": memo,
        "amount": amount,
        "status": random.choice(["success", "declined"]),
        "timestamp": datetime.datetime.now().isoformat()
    })
    print("Added payment")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/payments', methods=['POST'])
def add_payment_route():
    amount = request.form.get("amount")
    memo = request.form.get("memo")

    if not amount or not memo:
        return jsonify({"error": "Amount and memo required"}), 400

    bank_result = callMockBank(amount, memo)

    payments.append({
        "transactionId": bank_result["transactionId"],
        "memo": memo,
        "amount": amount,
        "status": bank_result["status"],
        "timestamp": datetime.datetime.now().isoformat()
    })

    print(f"Payment attempt: {memo}, {amount}, status: {bank_result['status']}")
    return jsonify(bank_result), 201


@app.route('/payments', methods=['GET'])
def listPayments():
    return jsonify(payments)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
