# SistemasDistribuidos

Desenvolver o Algoritmo Chord utilizado em redes P2P estruturadas.

O algoritmo deve permitir:

- montar um nova rede

- inserir dados nos nós da rede

- inserir novos nós

- retirar nós

O algoritmo Chord é usado em redes P2P estruturadas para permitir o armazenamento e recuperação de dados em um conjunto de nós interconectados. 

Ele usa um sistema de identificação de nós baseado em hash para garantir que cada nó possa encontrar rapidamente os dados armazenados em outros nós na rede.

# Definir o tamanho da rede: 

determinado pelo número de bits usados para gerar as chaves de hash, se usarmos 32 bits, a rede poderá conter até 2^32 nós.

# Inicializar a rede: 

selecione um nó aleatório para ser o nó de partida e atribua uma chave de hash de 0. Cada nó que se juntar à rede será atribuído uma chave de hash única de acordo com sua posição na rede.

# Adicionar nós: 

quando um nó se juntar à rede, ele deve primeiro encontrar um nó existente na rede. O novo nó terá atribuído uma chave de hash única e será adicionado à tabela de nós da rede. Em seguida, ele deve atualizar a tabela de sucessores e predecessores de cada nó da rede para refletir sua presença.

# Inserir ou Buscar dados: 

o nó deve primeiro calcular a chave de hash correspondente ao dado. Em seguida, ele deve enviar uma mensagem ao nó cuja chave de hash é a maior chave menor ou igual à chave do dado.

# Remover nós: 

é necessário atualizar as tabelas de sucessores e predecessores dos nós adjacentes ao nó que está sendo removido. Se um nó for removido, seus dados também devem ser.

