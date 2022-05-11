import datetime, hashlib, json
from flask import Flask, jsonify, request
from random import randrange

class Blockchain:
    # fonction qui initialise la blockchain et le premier block
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(nonce=1, previous_hash='0')

    # fonction qui crée un block
    def create_block(self, nonce, previous_hash):
        block = {
                'index': len(self.chain),
                'timestamp': str(datetime.datetime.now()),
                'nonce' : nonce,
                'previous_hash' : previous_hash,
                'transaction': self.current_transactions
                }

        self.current_transactions = []
        
        self.chain.append(block)

        return block

    # fonction qui ajoute les transactions dans le dernier block
    def add_transactions(self, sender, receiver, amount):
        self.current_transactions.append({
            'amount': amount,
            'receiver': receiver,
            'sender': sender,
            'hash': self.hash(self.current_transactions),
            'timestamp': str(datetime.datetime.now())
        })
        return self.last_block['index'] + 1

    # fonction qui hash le block passé en paramètre
    def hash(self, block):
        # passe le block json en string pour pouvoir avoir le hash
        hash_block = hashlib.sha256(json.dumps(block, sort_keys=True).encode('utf-8')).hexdigest()
        return hash_block

    # fonction qui valide le block
    def valid_mining(self, index, nonce, previous_hash, transactions):
        # calcule le hash du contenu du block
        content_block = f'{index}{nonce}{previous_hash}{transactions}'.encode()
        hashed_block = hashlib.sha256(content_block).hexdigest()
        # ici on check si le hash correspond a la difficulté souhaité ('00' en début de hash par exemple)
        if hashed_block[:2] == '00':
            return True
        else:
            return False

    # fonction utilisé pour le proof of work et pour miner le block
    def mining(self, index, previous_hash, transactions):
        nonce = 0
        # tant que le nonce du hash ne correspond pas a la difficulté souhaité on continue
        while self.valid_mining(index, nonce, previous_hash, transactions) is False:
            nonce += 1
        return nonce

    # getters and setters
    @property
    def last_block(self):
        return self.chain[-1]

    # fonction qui valide entierement la blockchain
    def valid_blockchain(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            # si le previous hash du block de la boucle est different
            # du hash du previous block alors on sort de la boucle
            # et on invalide la blockchain
            if block['previous_hash'] != self.hash(previous_block):
                return False

            # on recalcule le hash du block comme avec la fonction mining
            previous_nonce = previous_block['nonce']
            nonce = block['nonce']
            hash_op =  hashlib.sha256(
                            # methode basique pour creer un hash et on le met en hexa
                            str(nonce**2 - previous_nonce**2).encode('utf-8')).hexdigest()

            # si le hash est différent de ce qu'on spécifie
            # ici le '00' en début de hash
            # on invalide la blockchain
            if hash_op[:2] != '00':
                return False

            # on augmente l'index du block et on passe le previous block au block actuel
            previous_block = block
            block_index += 1

        # on valide la blockchain si on a passé toutes les conditions
        return True
        

# crée le site web
app = Flask(__name__)
 
# crée la blockchain
blockchain = Blockchain()
 
# mine un block et le met dans la blockchain
@app.route('/mine_block', methods=['GET'])
def mine_block():

    blockchain.add_transactions(
        sender='0',
        receiver=str(randrange(1073741824, 4294967297)),
        amount=1
    )

    previous_block_hash = blockchain.hash(blockchain.last_block)
    index = len(blockchain.chain)
    nonce = blockchain.mining(index, previous_block_hash, blockchain.current_transactions)
    block = blockchain.create_block(nonce, previous_block_hash)
    
    response = {'message': 'A block is MINED',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'nonce': block['nonce'],
                'previous_hash': block['previous_hash'],
                'transaction': block['transaction']}

     
    return jsonify(response), 200
 
# affiche la blockchain
@app.route('/get_chain', methods=['GET'])
def display_chain():
    response = {'blockchain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# verifie la validité de la blockchain
@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.valid_blockchain(blockchain.chain)
     
    if valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200
 
# ajoute des transactions 
@app.route('/transactions', methods=['GET'])
def new_transactions():

    index = blockchain.add_transactions(
        sender= str(randrange(1073741824, 4294967297)),
        receiver= str(randrange(1073741824, 4294967297)),
        amount= str(randrange(10, 100))
    )

    response = {'message': f'Transaction is added to the block {index}'}
    return jsonify(response), 200

# lance le serveur flask localement
app.run(host='127.0.0.1', port=5000)

        
