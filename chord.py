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
