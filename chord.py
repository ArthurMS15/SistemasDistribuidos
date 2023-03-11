from hashlib import sha1 #importa o módulo de hash SHA1

class Node:
    def __init__(self, id, address):
        self.id = id  #hash SHA-1 do endereço)
        self.address = address  #string no formato "ip:porta")
        self.data = {}  #dicionário que guarda os dados armazenados no nó

    #insere um par chave-valor no dicionário de dados
    def insert_data(self, key, value):
        self.data[key] = value

    #busca valor associado a uma chave no dicionário de dados
    def lookup_data(self, key):
        return self.data.get(key)

class Chord:
    def __init__(self, n_bits):
        self.n_bits = n_bits  #número de bits dos identificadores de nó
        self.nodes = []  #lista que guarda os nós na rede

    def add_node(self, address):
        # Calcula o identificador do nó como o hash SHA-1 do endereço
        id = int(sha1(address.encode()).hexdigest(), 16) % (2 ** self.n_bits)
        node = Node(id, address)
        self.nodes.append(node)
        self.nodes.sort(key=lambda n: n.id)  #ordena a lista de nós pelo id
        return node
