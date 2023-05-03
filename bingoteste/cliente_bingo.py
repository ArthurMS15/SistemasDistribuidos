import grpc
import sys
import time
import bingo_pb2
import bingo_pb2_grpc

def main():
    if len(sys.argv) != 3:
        print("Uso: python cliente_bingo.py <ip_servidor> <porta>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    channel = grpc.insecure_channel(f"{server_ip}:{server_port}")
    stub = bingo_pb2_grpc.BingoServiceStub(channel)

    authenticated = False
    while not authenticated:
        user_name = input("Digite seu nome: ")
        response = stub.Authenticate(bingo_pb2.AuthenticateRequest(user_name=user_name))
        authenticated = response.authenticated
        if not authenticated:
            print("Nome inválido. Tente novamente.")

    stub.Ready(bingo_pb2.ReadyRequest())
    print("Aguardando o início do jogo...")

    time.sleep(15)

    user_board = stub.GetUserBoard(bingo_pb2.UserBoardRequest())
    print("Sua tabela de bingo:")
    for i in range(0, 25, 5):
        print(user_board.numbers[i:i+5])

    while True:
        drawn_number = stub.GetDrawnNumber(bingo_pb2.DrawnNumberRequest())
        print(f"Número sorteado: {drawn_number.number}")

        marked_numbers = input("Digite os números marcados separados por espaço: ").split()
        marked_numbers = list(map(int, marked_numbers))

        response = stub.SubmitMarkedNumbers(bingo_pb2.MarkedNumbersRequest(marked_numbers=marked_numbers))
        if response.valid and response.winner:
            print("BINGO! Você ganhou!")
            break
        elif response.valid:
            print("Marcação válida.")
        else:
            print("Marcação inválida. Tente novamente.")

        time.sleep(20)

if __name__ == "__main__":
    main()
