import requests, json

def request_blockchain():
    blockchain = requests.get('http://127.0.0.1:5000/get_chain').text
    blockchain = json.loads(blockchain)
    blockchain = blockchain['blockchain']
    length=len(blockchain)-11
    if len(blockchain) < 11:
        length = -1
    return [blockchain[i] for i in range(len(blockchain)-1, length, -1)]

def get_blockchain():
    blockchain = request_blockchain()
    for block in blockchain:
        if block['previous_hash'].__len__() > 16:
            block['previous_hash'] = block['previous_hash'][:8]+'...'+block['previous_hash'][-8:]
        block['nbtransac']=len(block['transaction'])
    return blockchain

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

def lenghtByte(block):
    return block.__len__()*8

def block():
    Blockchain = requests.get('http://127.0.0.1:5000/get_chain').text
    Blockchain = json.loads(Blockchain)
    Blockchain = Blockchain['blockchain']
    index = 1
    for block in Blockchain:
        block['nbtransac']=len(block['transaction'])
        if int(block['index']) == int(index):
            return block

print(block())