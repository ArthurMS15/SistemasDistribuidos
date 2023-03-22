from hashlib import sha1 #calcular ua hash de uma mensagem que vai ser usada para verificar a integridade da mensagem

class Node:
    def _init_(self, id: int): #construtor
        self.id = id                # identificador único para o nó.
        self.estaAtivo = False       
        self.predecessor = None     
        self.sucessor = None       
        self.nodesAtribuidos = []     # lista de nós que estão atribuídos a este nó.
        self.dados = {}              # dicionário vazio que pode ser usado para armazenar qualquer outra informação associada a este nó. # imutável

class Chord:
    def _init_(self, n: int):         #cgerenciar o anel chord
        self.n = n                                  #número de nós no anel
        self.nodes = [Node(i) for i in range(n)]    #lista que contém os objetos "Node" (lista com ids sequenciais)

    def print(self):                    #imprimir informações sobre todos os nós
        for i, node in enumerate(self.nodes):       #for itera sobre todos os nós e usa a função enumerate para ter tanto o índice quando o opróprio objeto do nó
            print(f"Node {i}:")
            print(f"Predecessor: {node.predecessor.id if node.predecessor else None}")
            print(f"Sucessor: {node.sucessor.id if node.sucessor else None}")
            print(f"Nodes Atribuidos:")
            for assigned_node in node.nodesAtribuidos:
                print(f"    {assigned_node.id}")
            print(f"Dados: {len(node.dados)}")
            for key, value in node.dados.items():
                print(f"    {key}: {value}")

    #indice do nó: ponto de partida para a busca do nó responsável por armazenar a chave key e seu valor value. A busca é realizada de forma circular, verificando se o hash da chave está entre o nó predecessor e o nó atual. Quando o nó responsável é encontrado, o valor é adicionado à sua estrutura de dados
    def inserirDados(self, nodoInicial: int, key: str, value: str):
        if nodoInicial < 0 or nodoInicial >= self.n:
            raise ValueError("Node fora dos limites")
        nodeDeAgora = self.nodes[nodoInicial]
        if not nodeDeAgora.estaAtivo:
            raise ValueError("Nodo não ativado")
        hashIndex = self.hash(key) % self.n

        for _ in range(self.n):
            if nodeDeAgora.predecessor and nodeDeAgora.sucessor:
                if self.entreCircular(hashIndex, nodeDeAgora.predecessor.id, nodeDeAgora.id):
                    for node in nodeDeAgora.nodesAtribuidos:
                        if node.id == hashIndex:
                            node.dados[key] = value
                    break
                nodeDeAgora = nodeDeAgora.sucessor
            else:
                break
   
    #recupera o valor associado a uma chave key. A busca é realizada de forma circular, verificando se o hash da chave está entre o nó predecessor e o nó atual
    def buscar(self, startNodeIndex: int, key: str) -> str:
        if startNodeIndex < 0 or startNodeIndex >= self.n:
            raise ValueError("Node id out of range")
        currentNode = self.nodes[startNodeIndex]
        if not currentNode.estaAtivo:
            raise ValueError("Inactive node")
        hashIndex = self.hash(key) % self.n

        for _ in range(self.n):
            if currentNode.predecessor and currentNode.sucessor:
                if self.entreCircular(hashIndex, currentNode.predecessor.id, currentNode.id):
                    for node in currentNode.nodesAtribuidos:
                        if node.id == hashIndex:
                            return node.dados.get(key)
                    break
                currentNode = currentNode.sucessor
            else:
                break
        return None
    

    def adicionarNode(self, id: int):       #marca como ativo e definindo seu predecessor e sucessor. Se o predecessor e o sucessor existirem, eles também atualizarão seus respectivos ponteiros.
        if id < 0 or id >= self.n:
            raise ValueError("Node fora dos limites")
        node = self.nodes[id]
        node.estaAtivo = True
        node.predecessor = self.acharPredecessor(id)
        node.sucessor = self.acharSucessor(id)
        if node.predecessor:
            node.predecessor.sucessor = node
        if node.sucessor:
            node.sucessor.predecessor = node
        self.updateNodeAtribuidos()

    def removeNode(self, id: int):          #marca como inativo e atualizando os ponteiros de seu predecessor e sucessor. Em seguida, a lista de nós atribuídos de cada nó na rede é atualizada.
        if id < 0 or id >= self.n:
            raise ValueError("Node fora dos limites")
        node = self.nodes[id]
        node.estaAtivo = False
        if node.predecessor:
            node.predecessor.sucessor = node.sucessor
        if node.sucessor:
            node.sucessor.predecessor = node.predecessor
        node.predecessor = None
        node.sucessor = None
        self.updateNodeAtribuidos()

    def updateNodeAtribuidos(self):  #quais estão ativos e quais estão inativos. Aqueles que estão ativos recebem uma lista de nós atribuídos que inclui os nós que estão inativos, mas que têm uma posição circular menor na rede
        nodosRestantesInativos = []
        for curr in self.nodes:
            if curr.estaAtivo:
                curr.nodesAtribuidos = nodosRestantesInativos
                nodosRestantesInativos = []
            else:
                nodosRestantesInativos.append(curr)
        primeiroNodeAtivo = self.acharSucessor(self.n) #Em seguida, o método encontra o primeiro nó ativo na rede que segue o nó n (o último nó na rede). Esse nó é então atribuído à lista de nós atribuídos do primeiro nó ativo encontrado
        if primeiroNodeAtivo:
            primeiroNodeAtivo.nodesAtribuidos = nodosRestantesInativos

    def acharPredecessor(self, id: int) -> Node:     #itera em sentido anti horário pelos nós da rede, começando pelo nó anterior ao id informado, retorna o primeio nó ativo 
        for i in range(id - 1, id - self.n, -1):
            index = self.circuloIndex(i)
            if self.nodes[index].estaAtivo:
                return self.nodes[index]
        return None

    def acharSucessor(self, id: int) -> Node:       ##itera em sentido horário pelos nós da rede, começando pelo nó posterior ao id informado, retorna o primeio nó ativo    
        for i in range(id + 1, id + self.n):
            index = self.circuloIndex(i)
            if self.nodes[index].estaAtivo:
                return self.nodes[index]
        return None

    def entreCircular(self, num: int, inicio: int, final: int) -> bool:    #verifica se num está entre o intervalo entre inicio e final A função retorna True se num estiver dentro do intervalo e False caso contrário
        if inicio < final:
            return num > inicio and num <= final
        else:
            return num > inicio or num <= final

    def circuloIndex(self, i: int) -> int:       #recebendo um índice e retorna o novo índice calculado, garante que o índice resultante esteja dentro do intervalo de índices possíves para a classe chord [0, self.n-1]
        return (i % self.n + self.n) % self.n

    def hash(self, key: str) -> int:            #implementa um sistema de hash distribuído, recebendo uma chave retorna um inteiro que é o resultado da aplicação da função hash SHA1
        hash_object = sha1(key.encode('utf-8'))
        hash_hex = hash_object.hexdigest()
        hash_int = int(hash_hex[:12], 16)       #retorna apenas os primeiros 12 dígitos do número inteiro
        return hash_int

chord = Chord(16)

chord.adicionarNode(1)
chord.adicionarNode(6)
chord.adicionarNode(10)
chord.adicionarNode(11)
chord.adicionarNode(14)

chord.removeNode(11)

chord.inserirDados(1, '1', '7')
chord.inserirDados(1, '2', '12')
chord.inserirDados(1, '3', '10')

chord.print()

