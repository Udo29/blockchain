#######################################
# Projet fil rouge labo cryptomonnaie #
#######################################
from flask import Flask, request, redirect, render_template
import requests, json
app = Flask(__name__)

def get_blockchain():
    blockchain = request_blockchain()
    for block in blockchain:
        if block['previous_hash'].__len__() > 16:
            block['previous_hash'] = block['previous_hash'][:8]+'...'+block['previous_hash'][-8:]
        block['nbtransac']=len(block['transaction'])
    return blockchain

def request_blockchain():
    blockchain = requests.get('http://127.0.0.1:5000/get_chain').text
    blockchain = json.loads(blockchain)
    blockchain = blockchain['blockchain']
    length=len(blockchain)-11
    if len(blockchain) < 11:
        length = -1
    return [blockchain[i] for i in range(len(blockchain)-1, length, -1)]

def lenghtByte(block):
    return block.__len__()*8

def get_transactions():
    blockchain = request_blockchain()
    transactions = []
    for block in reversed(blockchain):
        for i in range(len(block['transaction'])-1, -1, -1):
            transactions.append(block['transaction'][i])
            if len(transactions) == 10:
                return transactions

def transactions():
    transactions = get_transactions()
    for i in range(len(transactions)):
        if transactions[i]['hash'].__len__() > 16:
            transactions[i]['hash'] = transactions[i]['hash'][:8]+'...'+transactions[i]['hash'][-8:]
    return transactions



@app.route("/", methods=['GET'])
def init():
    Blockchain = get_blockchain()
    return render_template('index.html', chain=Blockchain, transaction=transactions())

@app.route("/search", methods=['POST'])
def search():
    Blockchain = requests.get('http://127.0.0.1:5000/get_chain').text
    Blockchain = json.loads(Blockchain)
    Blockchain = Blockchain['blockchain']
    search = request.form['search']
    i = len(search)
    hash = [val for val in Blockchain if val['previous_hash'][:i] == search[:i]]
    for block in hash:
        block['nbtransac']=len(block['transaction'])
    return render_template('search.html',search=hash)

@app.route("/block", methods=['POST'])
def block():
    Blockchain = requests.get('http://127.0.0.1:5000/get_chain').text
    Blockchain = json.loads(Blockchain)
    Blockchain = Blockchain['blockchain']
    index = request.form['index']
    for block in Blockchain:
        if int(block['index']) == int(index):
            block['nbtransac']=len(block['transaction'])
            return render_template('block.html', block=block, length=lenghtByte(block))

@app.route("/transaction", methods=['POST'])
def transaction():
    Blockchain = requests.get('http://127.0.0.1:5000/get_chain').text
    Blockchain = json.loads(Blockchain)
    Blockchain = Blockchain['blockchain']
    hash = request.form['hash']
    for block in Blockchain:
        for i in range(len(block['transaction'])):
            if str(block['transaction'][i]['hash'][:8]) == str(hash[:8]):
                return render_template('transaction.html', transac=block['transaction'][i])

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)