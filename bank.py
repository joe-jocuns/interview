from flask import Flask, jsonify
import random
import uuid

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def processPayment():
    status = random.choice(["succeeded", "declined"])
    transaction_id = str(uuid.uuid4())
    return jsonify({
        "status": status,
        "transactionId": transaction_id
    })

if __name__ == "__main__":
    app.run(debug=True, port=5002)  
