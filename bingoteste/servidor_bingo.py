import grpc
from concurrent import futures
import sys
import random
import time
from collections import defaultdict
import bingo_pb2
import bingo_pb2_grpc

authenticated_users = set()
ready_users = set()
user_boards = {}
drawn_numbers = []

def generate_board():
    board = []
    for _ in range(5):
        row = random.sample(range(1, 76), 5)
        board.extend(row)
    return board

class BingoService(bingo_pb2_grpc.BingoServiceServicer):
    def Authenticate(self, request, context):
        authenticated_users.add(request.user_name)
        return bingo_pb2.AuthenticateResponse(authenticated=True)

    def Ready(self, request, context):
        ready_users.add(context.peer())
        return bingo_pb2.ReadyResponse()

    def GetUserBoard(self, request, context):
        if context.peer() not in ready_users:
            return bingo_pb2.UserBoard()

        if context.peer() not in user_boards:
            board = generate_board()
            user_boards[context.peer()] = board

        return bingo_pb2.UserBoard(numbers=user_boards[context.peer()])

    def SubmitMarkedNumbers(self, request, context):
        if context.peer() not in user_boards:
            return bingo_pb2.MarkedNumbersResponse(valid=False, winner=False)

        marked_board = set(request.marked_numbers)
        actual_board = set(user_boards[context.peer()])
        valid = marked_board.issubset(actual_board) and marked_board.issubset(drawn_numbers)

        if valid and len(marked_board) == len(actual_board):
            winner = True
        else:
            winner = False

        return bingo_pb2.MarkedNumbersResponse(valid=valid, winner=winner)

    def GetDrawnNumber(self, request, context):
        return bingo_pb2.DrawnNumber(number=drawn_numbers[-1])

def main():
    if len(sys.argv) != 2:
        print("Uso: python servidor_bingo.py <porta>")
        sys.exit(1)

    port = int(sys.argv[1])
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bingo_pb2_grpc.add_BingoServiceServicer_to_server(BingoService(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Servidor gRPC escutando na porta {port}...")
    time.sleep(15)
    while len(ready_users) < len(authenticated_users):
        time.sleep(1)

    while True:
        drawn_number = random.randint(1, 75)
        if drawn_number not in drawn_numbers:
            drawn_numbers.append(drawn_number)
            print(f"Número sorteado: {drawn_number}")
            time.sleep(20)

if __name__ == "__main__":
    main()

