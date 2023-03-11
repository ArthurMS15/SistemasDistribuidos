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
        #calcula o identificador do nó como o hash SHA-1 do endereço
        id = int(sha1(address.encode()).hexdigest(), 16) % (2 ** self.n_bits)
        node = Node(id, address)
        self.nodes.append(node)
        self.nodes.sort(key=lambda n: n.id)  #ordena a lista de nós pelo id
        return node
    
    def remove_node(self, address):
        #encontra o nó correspondente ao endereço e o remove da lista de nós
        node = next((n for n in self.nodes if n.address == address), None)
        if node:
            self.nodes.remove(node)

    #encontra nó responsável por uma chave na rede
    def find_successor(self, key):
        #calcula o identificador da chave como o hash SHA-1 da chave
        id = int(sha1(key).hexdigest(), 16)
        #procura o nó responsável por essa chave na lista ordenada de nós
        for i, node in enumerate(self.nodes):
            if node.id >= id:
                return self.nodes[i % len(self.nodes)] # busca circular
        # se nenhum nó encontrado, retorna primeiro nó da lista
        return self.nodes[0]
    
    #insere um par chave-valor na rede
    def insert_data(self, address, key, value):
        node = self.find_successor(key)
        if node.address == address:
            node.insert_data(key, value)
        else:
            #encaminha inserção para o nó responsável
            node.insert_data(key, value)
