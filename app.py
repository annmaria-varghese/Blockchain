from flask import Flask, render_template, request, redirect, jsonify
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html', chain=blockchain.chain)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    sender = request.form['sender']
    recipient = request.form['recipient']
    amount = request.form['amount']
    blockchain.add_new_transaction({
        'sender': sender,
        'recipient': recipient,
        'amount': float(amount)
    })
    return redirect('/')

@app.route('/mine', methods=['POST'])
def mine():
    blockchain.mine()
    return redirect('/')

@app.route('/get_chain', methods=['GET'])
def get_chain():
    chain_data = [block.__dict__ for block in blockchain.chain]
    return jsonify(chain_data)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
