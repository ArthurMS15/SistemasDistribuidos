from hashlib import sha1 #importa o módulo de hash SHA1

class Node:
    def __init__(self, id, address):
        self.id = id  #hash SHA-1 do endereço)
        self.address = address  #string no formato "ip:porta")
        self.data = {}  #dicionário que guarda os dados armazenados no nó