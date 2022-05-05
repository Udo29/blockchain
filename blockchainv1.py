import datetime, hashlib, json
from flask import Flask, jsonify

class Blockchain:
    # fonction qui initialise la blockchain et le premier block
    def __init__(self):
        self.blockchain = []
        self.create_block(nonce=1, previous_hash='0')

    # fonction qui crée un block
    def create_block(self, nonce, previous_hash):
        # création des paramètres d'un block
        block = {
                'blockNb': len(self.blockchain) + 1,
                'timestamp': str(datetime.datetime.now()),
                'nonce' : nonce,
                'previous_hash' : previous_hash
                }
        # ajout du block a la blockchain
        self.blockchain.append(block)
        return block

    # fonction qui hash le block passé en paramètre
    def hash(self, block):
        # passe le block json en string pour pouvoir avoir le hash
        hash_block = hashlib.sha256(json.dumps(block).encode('utf-8')).hexdigest()
        return hash_block

    # fonction utilisé pour le proof of work et pour miner le block
    def mining(self, previous_nonce):
        # nouveau nonce
        new_nonce = 1
        # variable bool qui va determiner quand le block va etre valide
        check_nonce = False

        # tant que le hash n'a pas x fois 0 au debut, on continue
        # exemple de hash: 0x0000[a-f0-9]
        # on augmente le nonce de 1 et on revérifie
        while check_nonce == False:
            hash_op =  hashlib.sha256(
                            # methode basique pour creer un hash et on le met en hexa
                            str(new_nonce**2 - previous_nonce**2).encode('utf-8')).hexdigest()
            # verification du hash
            # si les deux premiers char du hash sont '00' alors le nonce est valide
            if hash_op[:2] == '00':
                check_nonce = True
            else:
                new_nonce += 1

        # return le nonce qui a miner le block
        return new_nonce

    # fonction qui retourne le block precédent
    def previous_block(self):
        # [-1] sur une liste retourne le dernier élément
        return self.blockchain[-1]

    # fonction qui valide toute la blockchain
    def valid_blockchain(self, blockchain):
        # on commence la validation au premier block
        previous_block = blockchain[0]
        block_index = 1

        # iteration sur la blockchain
        while block_index < len(blockchain):
            block = blockchain[block_index]
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
    previous_block = blockchain.previous_block()
    previous_nonce = previous_block['nonce']
    nonce = blockchain.mining(previous_nonce)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(nonce, previous_hash)
     
    response = {'message': 'A block is MINED',
                'blockNb': block['blockNb'],
                'timestamp': block['timestamp'],
                'nonce': block['nonce'],
                'previous_hash': block['previous_hash']}
     
    return jsonify(response), 200
 
# affiche la blockchain
@app.route('/get_chain', methods=['GET'])
def display_chain():
    response = {'blockchain': blockchain.blockchain,
                'length': len(blockchain.blockchain)}
    return jsonify(response), 200
 
# verifie la validité de la blockchain
@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.valid_blockchain(blockchain.blockchain)
     
    if valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200
 
 
# lance le serveur flask localement
app.run(host='127.0.0.1', port=5000)

            
