from flask import Flask, request, render_template,redirect
from pymongo import MongoClient
app = Flask(__name__, template_folder="templates")

client = MongoClient("mongodb+srv://doddavaramsn27:fbaj1zCmrRBQCtxM@cluster0.howrb.mongodb.net/")
db = client["hackathon"]


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/adduser", methods=["GET", "POST"])
def add_user():
    if request.method == "GET":
        return render_template("users.html")
    if request.method == "POST":
        collection = db["user"]

        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        credit_limit = request.form.get("credit_limit")
        due = request.form.get("due")

        collection.insert_one({
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "credit_limit": credit_limit,
            "due": due
        })


        return "User Added"

@app.route("/addmerchant", methods=["GET", "POST"])
def add_merchant():
    if request.method == "GET":
        return redirect("merchants.html")
    if request.method == "POST":
        collection = db["merchants"]
        pay_app = request.form.get("pay_app")
        txn_rate = request.form.get("txn_rate")

        collection.insert_one({
            "pay_app": pay_app,
            "txn_rate": txn_rate
        })

        return "Merchant Added"

@app.route("/makepayment", methods=["GET", "POST"])
def make_payment():
    if request.method == "GET":
        return render_template("payment.html")
    if request.method == "POST":
        name = request.form.get("name")
        item = request.form.get("item")
        price = int(request.form.get("price"))
        pay_app = request.form.get("pay_app")
        collection = db["user"]

        user_credit = collection.find({"name": name}, {"_id": 0, "credit_limit": 1})
        amount = int(user_credit.get("credit_limit"))
        credit = amount - price

        if credit < 0:
            return "Insufficient Amount!!!"

        collection = db["merchants"]

        rate = collection.find({"pay_app": pay_app}, {"_id": 0, "txn_rate": 1})
        tx_rate = int(rate.get("txn_rate"))

        fee = (tx_rate / 100) * amount 
        to_merchant = amount - fee

        collection = db["order"] 
        collection.insert_one({
            "user_name": name,
            "item": item,
            "price": price,
            "app": pay_app, 
        })

        collection = db["user"]
        collection.update_many({"name": name}, {"$set": {
            "credit_amount": credit
        }})

        return "Paymment Successfull!!!"

@app.route("/viewusers")
def view_users():
    collection = db["user"]
    users = list(collection.find({}, {"_id": 0}))

    return render_template("viewusers.html", users=users)

app.run(debug=True)