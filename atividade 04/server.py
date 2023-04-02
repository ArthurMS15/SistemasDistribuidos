import socket
import sys
import os

def main():
    if len(sys.argv) != 3:
        print("Uso: python server.py <porta> <diretorio>")
        sys.exit(1)

    port = int(sys.argv[1])
    directory = sys.argv[2]

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', port))
    server.listen(1)
    print(f"Servidor escutando na porta {port}...")

    while True:
        conn, addr = server.accept()
        print(f"Conexão estabelecida com {addr}")
        filename = conn.recv(1024).decode()
        filepath = os.path.join(directory, filename)

        if os.path.isfile(filepath):
            conn.send(b"EXIST " + str(os.path.getsize(filepath)).encode())
            user_response = conn.recv(1024).decode()

            if user_response == "OK":
                with open(filepath, "rb") as f:
                    bytes_read = f.read(4096)
                    while bytes_read:
                        conn.send(bytes_read)
                        bytes_read = f.read(4096)
                print("Arquivo enviado com sucesso.")
        else:
            conn.send(b"ERR")
        conn.close()

if __name__ == "__main__":
    main()
