from hashlib import sha1
from typing import Dict, List, Optional, Tuple, Union

class Node:
    def __init__(self, id: int):
        self.id = id
        self.isActive = False
        self.predecessor = None
        self.successor = None
        self.assignedNodes = []
        self.data = {}

class Chord:
    def __init__(self, n: int):
        self.n = n
        self.nodes = [Node(i) for i in range(n)]

    def print(self):
        for i, node in enumerate(self.nodes):
            print(f"Node {i}:")
            print(f"  Predecessor: {node.predecessor.id if node.predecessor else None}")
            print(f"  Successor: {node.successor.id if node.successor else None}")
            print(f"  Assigned nodes: {len(node.assignedNodes)}")
            for assigned_node in node.assignedNodes:
                print(f"    {assigned_node.id}")
            print(f"  Data: {len(node.data)}")
            for key, value in node.data.items():
                print(f"    {key}: {value}")

    def insert(self, startNodeIndex: int, key: str, value: str):
        if startNodeIndex < 0 or startNodeIndex >= self.n:
            raise ValueError("Node id out of range")
        currentNode = self.nodes[startNodeIndex]
        if not currentNode.isActive:
            raise ValueError("Inactive node")
        hashIndex = self.hash(key) % self.n

        for _ in range(self.n):
            if currentNode.predecessor and currentNode.successor:
                if self.isBetweenCircular(hashIndex, currentNode.predecessor.id, currentNode.id):
                    for node in currentNode.assignedNodes:
                        if node.id == hashIndex:
                            node.data[key] = value
                    break
                currentNode = currentNode.successor
            else:
                break

    def get(self, startNodeIndex: int, key: str) -> Optional[str]:
        if startNodeIndex < 0 or startNodeIndex >= self.n:
            raise ValueError("Node id out of range")
        currentNode = self.nodes[startNodeIndex]
        if not currentNode.isActive:
            raise ValueError("Inactive node")
        hashIndex = self.hash(key) % self.n

        for _ in range(self.n):
            if currentNode.predecessor and currentNode.successor:
                if self.isBetweenCircular(hashIndex, currentNode.predecessor.id, currentNode.id):
                    for node in currentNode.assignedNodes:
                        if node.id == hashIndex:
                            return node.data.get(key)
                    break
                currentNode = currentNode.successor
            else:
                break
        return None

    def addNode(self, id: int):
        if id < 0 or id >= self.n:
            raise ValueError("Node id out of range")
        node = self.nodes[id]
        node.isActive = True
        node.predecessor = self.findPredecessor(id)
        node.successor = self.findSuccessor(id)
        if node.predecessor:
            node.predecessor.successor = node
        if node.successor:
            node.successor.predecessor = node
        self.updateAssignedNodes()

    def removeNode(self, id: int):
        if id < 0 or id >= self.n:
            raise ValueError("Node id out of range")
        node = self.nodes[id]
        node.isActive = False
        if node.predecessor:
            node.predecessor.successor = node.successor
        if node.successor:
            node.successor.predecessor = node.predecessor
        node.predecessor = None
        node.successor = None
        self.updateAssignedNodes()

    def updateAssignedNodes(self):
        remainingInactiveNodes = []
        for curr in self.nodes:
            if curr.isActive:
                curr.assignedNodes = remainingInactiveNodes
                remainingInactiveNodes = []
            else:
                remainingInactiveNodes.append(curr)
        firstActiveNode = self.findSuccessor(self.n)
        if firstActiveNode:
            firstActiveNode.assignedNodes = remainingInactiveNodes

    def findPredecessor(self, id: int) -> Optional[Node]:
        for i in range(id - 1, id - self.n, -1):
            index = self.circleIndex(i)
            if self.nodes[index].isActive:
                return self.nodes[index]
        return None

    def findSuccessor(self, id: int) -> Optional[Node]:
        for i in range(id + 1, id + self.n):
            index = self.circleIndex(i)
            if self.nodes[index].isActive:
                return self.nodes[index]
        return None

    def isBetweenCircular(self, num: int, start: int, end: int) -> bool:
        if start < end:
            return num > start and num <= end
        else:
            return num > start or num <= end

    def circleIndex(self, i: int) -> int:
        return (i % self.n + self.n) % self.n

    def hash(self, key: str) -> int:
        hash_object = sha1(key.encode('utf-8'))
        hash_hex = hash_object.hexdigest()
        hash_int = int(hash_hex[:12], 16)
        return hash_int

#chord = Chord(16)
#
#chord.addNode(1)
#chord.addNode(6)
#chord.addNode(8)
#chord.addNode(11)
#chord.addNode(13)
#
#chord.removeNode(11)
#
#chord.insert(1, 'a', '1')
#chord.insert(1, 'b', '2')
#chord.insert(1, 'c', '3')
#
#chord.print()
#
#print(chord.get(1, 'a'))
#print(chord.get(1, 'b'))
#print(chord.get(1, 'c'))
#
#