import hashlib #importa o módulo de hash SHA1

class ChordNode: #para criação do nodo
    def __init__(self, id, address):
        self.id = id
        self.address = address
        self.predecessor = None
        self.successor = self
        self.data = {}