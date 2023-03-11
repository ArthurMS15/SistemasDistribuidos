import hashlib #importa o módulo de hash SHA1

class Node: #para criação do nodo
    def __init__(self, node_id, address):
        self.node_id = node_id
        self.address = address
        self.predecessor = None
        self.successor = None
        self.data = {}
    
    def find_successor(self, key):
        if self.successor.node_id == self.node_id or self.successor.node_id >= key:
            return self.successor
        else:
            node = self.closest_preceding_node(key)
            return node.find_successor(key)
    
    def closest_preceding_node(self, key):
        for i in range(len(self.node_id)-1, -1, -1):
            if self.node_id[i] < key[i]:
                return self.successor if self.successor.node_id != self.node_id else self
        return self