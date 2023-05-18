import grpc
import bingo_pb2 as pb2
import bingo_pb2_grpc as pb2_grpc
import asyncio


PORT = 8000
PROTO_FILE = "./proto/bingo.proto"

channel = grpc.insecure_channel(f"172.16.1.15:{PORT}")
client = pb2_grpc.BingoStub(channel)

stage = 0
myToken = ""
myUserName = ""
myCard = [0]
sortedNumbers = []

def on_client_ready():
    global stage, myUserName, myToken, myCard, sortedNumbers

    while True:
        if stage == 0:
            myUserName = input().replace("\r\n", "")
            login = client.Login(pb2.LoginRequest(username=myUserName))
            response = login.next()
            
            if stage == 0 and response.status == 0:
                print(response)
                myToken = response.token
                print(response.message + "\nDo u wanna start?y/n")
                if input():
                    stage = 1                    
            elif response.status == 1:
                print(response.message + "\nRetype another:")
                
        elif stage == 1:
            response = client.Ready(pb2.ReadyRequest(token=myToken, username=myUserName))
            print(response.message)
            print("Your card is:")
            myCard = response.card
            print(myCard)
            print(type(myCard))
            stage = 2
            
            for chunk in client.Play(pb2.PlayRequest(token=myToken, username=myUserName)):
                print("The number is:" + str(chunk.number))
                sortedNumbers.append(chunk.number)
                print("The sorted numbers that u saw are:")
                print(sortedNumbers)
                print("Yours numbers are: ")
                print(myCard)
                print("Are u the winner? (Enter to continue, 'y' for testing )")
                if input().replace("\r\n", "") == "y":
                    print("****************************")
                    print("Checking...")
                    print("****************************")
                    response = client.CheckWin(pb2.WinCheckRequest(token=myToken, username=myUserName))
                    print(response.message)
    
        elif stage == 2:
            if input().replace("\r\n", "") == "y":
                print("****************************")
                print("Checking...")
                print("****************************")
                response = client.CheckWin(pb2.WinCheckRequest(token=myToken, username=myUserName))
                print(response.message)

try:
    on_client_ready()
except KeyboardInterrupt:
    pass
