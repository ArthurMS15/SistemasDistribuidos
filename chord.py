import hashlib

class Node:
    def __init__(self, id):
        self.id = id
        self.isActive = False
        self.predecessor = None
        self.successor = None
        self.assignedNodes = []
        self.data = {}

#import hashlib
#
#message = "Hello World"
#sha1_hash = hashlib.sha1(message.encode()).hexdigest()
#
#print(sha1_hash)
#
#from Node import Node
# código que utiliza a classe Node
