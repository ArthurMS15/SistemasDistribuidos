from hashlib import sha1 #função iportada para calcular ua hash de uma mensagem que vai ser usada para verificar a integridade da mensagem
from typing import Dict, List, Optional, Tuple, Union
#importando tipos de dados definidos: Esses tipos são usados para definir o tipo de entrada e saída das funções e métodos, o que ajuda a tornar o código mais legível e compreensível. Os tipos incluem dicionários (Dict), listas (List), tuplas (Tuple), tipos de dados opcionais (Optional) e tipos de dados unificados (Union).

class Node:
    def __init__(self, id: int): #construtor
        self.id = id                # identificador único para o nó.
        self.isActive = False       # indicador de se o nó está ativo ou não.
        self.predecessor = None     # referência ao nó predecessor.
        self.successor = None       # referência ao nó sucessor.
        self.assignedNodes = []     # lista de nós que estão atribuídos a este nó.
        self.data = {}              # dicionário vazio que pode ser usado para armazenar qualquer outra informação associada a este nó. # imutável

class Chord:
    def __init__(self, n: int):         #criado para gerenciar um anel chord (pesquisar e recuperar info de sistemas distribuídos P2P)
        self.n = n                                  #número de nós no anel
        self.nodes = [Node(i) for i in range(n)]    #lista que contém os objetos "Node", criando a lista com ids sequênciais

    def print(self):                    #imprimir informações sobre todos os nós
        for i, node in enumerate(self.nodes):       #for itera sobre todos os nós e usa a função enumerate para ter tanto o índice quando o opróprio objeto do nó
            print(f"Node {i}:")
            print(f"  Predecessor: {node.predecessor.id if node.predecessor else None}")
            print(f"  Successor: {node.successor.id if node.successor else None}")
            print(f"  Assigned nodes: {len(node.assignedNodes)}")
            for assigned_node in node.assignedNodes:
                print(f"    {assigned_node.id}")
            print(f"  Data: {len(node.data)}")
            for key, value in node.data.items():
                print(f"    {key}: {value}")

    #A função insert recebe como entrada o índice do nó que deve ser usado como ponto de partida para a busca do nó responsável por armazenar a chave key e seu valor value. A busca é realizada de forma circular, verificando se o hash da chave está entre o nó predecessor e o nó atual. Quando o nó responsável é encontrado, o valor é adicionado à sua estrutura de dados.
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
    #A função get é similar à insert, mas é usada para recuperar o valor associado a uma chave key. A busca é realizada de forma circular, verificando se o hash da chave está entre o nó predecessor e o nó atual. Quando o nó responsável é encontrado, a função verifica se a chave está presente em sua estrutura de dados, e retorna seu valor caso esteja presente. Caso contrário, retorna None.
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

    def addNode(self, id: int):         # adiciona um novo nó à rede, marcando-o como ativo e definindo seu predecessor e sucessor. Se o predecessor e o sucessor existirem, eles também atualizarão seus respectivos ponteiros. Em seguida, a lista de nós atribuídos de cada nó na rede é atualizada.
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

    def removeNode(self, id: int):          #remove um nó da rede, marcando-o como inativo e atualizando os ponteiros de seu predecessor e sucessor. Em seguida, a lista de nós atribuídos de cada nó na rede é atualizada.
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

    def updateAssignedNodes(self):  #percorre todos os nós da rede e identifica quais estão ativos e quais estão inativos.  Aqueles que estão ativos recebem uma lista de nós atribuídos que inclui os nós que estão inativos, mas que têm uma posição circular menor na rede. 
        remainingInactiveNodes = []
        for curr in self.nodes:
            if curr.isActive:
                curr.assignedNodes = remainingInactiveNodes
                remainingInactiveNodes = []
            else:
                remainingInactiveNodes.append(curr)
        firstActiveNode = self.findSuccessor(self.n) #Em seguida, o método encontra o primeiro nó ativo na rede que segue o nó n (o último nó na rede). Esse nó é então atribuído à lista de nós atribuídos do primeiro nó ativo encontrado.
        if firstActiveNode:
            firstActiveNode.assignedNodes = remainingInactiveNodes

    def findPredecessor(self, id: int) -> Optional[Node]:     #itera em sentido anti horário pelos nós da rede, começando pelo nó anterior ao id informado, retorna o primeio nó ativo 
        for i in range(id - 1, id - self.n, -1):
            index = self.circleIndex(i)
            if self.nodes[index].isActive:
                return self.nodes[index]
        return None

    def findSuccessor(self, id: int) -> Optional[Node]:       ##itera em sentido horário pelos nós da rede, começando pelo nó posterior ao id informado, retorna o primeio nó ativo    
        for i in range(id + 1, id + self.n):
            index = self.circleIndex(i)
            if self.nodes[index].isActive:
                return self.nodes[index]
        return None

    def isBetweenCircular(self, num: int, start: int, end: int) -> bool:    #verifica se num está entre o intervalo entre start e end A função retorna True se num estiver dentro do intervalo e False caso contrário.
        if start < end:
            return num > start and num <= end
        else:
            return num > start or num <= end

    def circleIndex(self, i: int) -> int:       #recebendo um índice e retorna o novo índice calculado, garante que o índice resultante esteja dentro do intervalo de índices possíves para a classe chord [0, self.n-1]
        return (i % self.n + self.n) % self.n

    def hash(self, key: str) -> int:            #implementa um sistema de hash distribuído, recebendo uma chave retorna um inteiro que é o resultado da aplicação da função hash SHA1
        hash_object = sha1(key.encode('utf-8'))
        hash_hex = hash_object.hexdigest()
        hash_int = int(hash_hex[:12], 16)       #o código converte o resultado hexadecimal para um número inteiro usando a função int() e, em seguida, retorna apenas os primeiros 12 dígitos do número inteiro usando a notação de fatiamento de strings em Python [:12].
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