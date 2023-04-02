import socket #módulo necessário para ciraçaão da comunicação cliente-servidor
import sys
import os #manipulação de caminhos de arquivos e diretórios.

def main():
    if len(sys.argv) != 3:
        print("Uso: python server.py <porta> <diretorio>")
        sys.exit(1)                                         #verifica a quantidade correta de argumentos fornecida

    port = int(sys.argv[1])                                 #converte para inteiro o segundo argumento (porta)
    directory = sys.argv[2]

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cria um novo objeto de socket usando o protocolo IPv4 (AF_INET) e TCP (SOCK_STREAM). 
    server.bind(('', port))                                    #cincula o socket ao endereço e porta especificados
    server.listen(1)                                           #servidor em modo de escuta, aguardando conexões de clientes
    print(f"Servidor escutando na porta {port}...")

    while True:
        conn, addr = server.accept()                           #aceita uma conexão de cliente e retorna um novo objeto de socket (conn) e o endereço do cliente (addr).
        print(f"Conexão estabelecida com {addr}")
        filename = conn.recv(1024).decode()                    #recebe dados do cliente (tamanho máximo de 1024 bytes) e decodifica-os para obter o nome do arquivo.
        filepath = os.path.join(directory, filename)           #combina o diretório fornecido e o nome do arquivo para criar o caminho completo do arquivo.

        if os.path.isfile(filepath):                           #verifica se o arquivo existe no caminho especificado.
            conn.send(b"EXIST " + str(os.path.getsize(filepath)).encode()) #envia a mensagem "EXIST" e o tamanho do arquivo em bytes para o cliente.
            user_response = conn.recv(1024).decode()           #recebe a resposta do cliente e a decodifica

            if user_response == "OK":
                with open(filepath, "rb") as f:                #modo de leitura binária 
                    bytes_read = f.read(4096)
                    while bytes_read:
                        conn.send(bytes_read)                  #envia bytes lidos para o cliente
                        bytes_read = f.read(4096)
                print("Arquivo enviado com sucesso.")
        else:
            conn.send(b"ERR")
        conn.close()

if __name__ == "__main__":
    main()
