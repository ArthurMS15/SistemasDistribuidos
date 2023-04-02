import socket
import json
import sys

def main():
    if len(sys.argv) != 3:
        print("Uso: python client.py <ip_servidor> <porta>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    print("Conectado ao servidor")

    # Autenticação do aluno
    authenticated = False
    while not authenticated:
        student_id = input("Digite sua matrícula: ")
        password = input("Digite sua senha: ")

        client.send(student_id.encode())
        client.send(password.encode())

        response = client.recv(1024).decode()
        if response == "AUTHENTICATED":
            authenticated = True
        else:
            print("Matrícula ou senha incorretos. Tente novamente.")

    # Receber questões e enviar respostas
    while True:
        question_data = client.recv(4096).decode()
        if not question_data:
            break
        question = json.loads(question_data)
        print(f"\n{question['question']}")

        for idx, option in enumerate(question["options"]):
            print(f"{idx}. {option}")

        student_answer = int(input("Digite o número da resposta correta: "))
        client.send(str(student_answer).encode())

        response = client.recv(1024).decode()
        if response == "CORRECT":
            print("Resposta correta!")
        else:
            print("Resposta incorreta.")

    # Receber resultado final
    result = json.loads(client.recv(4096).decode())
    print(f"\nTotal de questões: {result['total_questions']}")
    print(f"Total de acertos: {result['correct_answers']}")

    client.close()

if __name__ == "__main__":
    main()
