import hashlib

class Node:
    def __init__(self, address):
        self.address = address
        self.id = int(hashlib.sha1(address.encode('utf-8')).hexdigest(), 16)
        self.data = {}
        self.finger_table = [None] * 160
        self.successor = None
        self.predecessor = None

    def join(self, ring):
        if not ring:
            self.successor = self
            self.predecessor = self
        else:
            self.successor = ring.find_successor(self.id)
            self.predecessor = self.successor.predecessor
            self.successor.predecessor = self
            self.predecessor.successor = self
        self.build_finger_table()

    def leave(self):
        self.successor.predecessor = self.predecessor
        self.predecessor.successor = self.successor
        for key in self.data.keys():
            self.successor.data[key] = self.data[key]

    def build_finger_table(self):
        for i in range(160):
            self.finger_table[i] = self.find_successor((self.id + 2**i) % 2**160)

    def find_successor(self, key):
        if self.successor.id == self.id or (self.id < key <= self.successor.id):
            return self.successor
        else:
            node = self.closest_preceding_node(key)
            return node.find_successor(key)

    def closest_preceding_node(self, key):
        for i in range(159, -1, -1):
            if self.finger_table[i] and (self.id < self.finger_table[i].id < key):
                return self.finger_table[i]
        return self

    def put(self, key, value):
        node = self.find_successor(key)
        node.data[key] = value

    def get(self, key):
        node = self.find_successor(key)
        return node.data.get(key)

    def remove(self, key):
        node = self.find_successor(key)
        del node.data[key]

    def print_ring(self):
        current_node = self
        print("Ring:")
        while True:
            print(current_node.address)
            current_node = current_node.successor
            if current_node == self:
                break

# Criação dos nós
node1 = Node("192.168.0.1:5000")
node2 = Node("192.168.0.2:5000")

# Junção dos nós na rede
node1.join(None)
node2.join(node1)

# Inserção de um par chave-valor na rede
node1.put(1, "valor 1")

# Busca do valor associado à chave 1
print(node1.get(1)) # deve imprimir "valor 1"
print(node2.get(1)) # deve imprimir "valor 1"

# Remoção do par chave-valor da rede
node2.remove(1)

# Busca do valor associado à chave 1 após remoção
print(node1.get(1)) # deve imprimir None
print(node2.get(1)) # deve imprimir None

# Impressão da lista de nós na rede
node1.print_ring() # deve imprimir "192.168.0.1:5000" e "192.168.0.2:5000"
