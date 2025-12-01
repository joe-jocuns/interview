from flask import Flask, request
import random
import datetime
import string
payments = []

app = Flask(__name__)

iterator = 100

characters = string.ascii_letters + string.digits


for i in range(iterator):
 
    payments.append({

        "transactionId": f"{i}_{''.join(random.choice(characters) for _ in range(4))}",
        "memo" : ''.join(random.choice(characters) for letters in range(10)),
        "amount": random.randint(200, 1000),
        "status": random.choice(["Success", "Declined"]),
        "timestamp" :  f"{random.randint(0,23)}:{random.randint(0,59)}"
    })

for payment in payments:
    print(payment)
    print("\n")