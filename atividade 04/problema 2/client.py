import socket #criar um cliente de rede e se comunicar com o servidor.
import json #codificar e decodificar objetos JSON.
import sys #acessar argumentos da linha de comando e sair do programa.

def main():
    if len(sys.argv) != 3:
        print("Uso: python client.py <ip_servidor> <porta>")    #quantidade correta de argumentos fornecido
        sys.exit(1)

    server_ip = sys.argv[1]                                     #armazena o primeiro argumento da linha de comando
    server_port = int(sys.argv[2])

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #cria um novo objeto de socket para o cliente
    client.connect((server_ip, server_port))                    #conecta-se ao servidor no IP e porta especificados
    print("Conectado ao servidor")

    # Autenticação do aluno
    authenticated = False
    while not authenticated:
        student_id = input("Digite sua matrícula: ")
        password = input("Digite sua senha: ") #Lida com a autenticação do aluno.

        client.send(student_id.encode())
        client.send(password.encode())

        response = client.recv(1024).decode() 
        if response == "AUTHENTICATED":
            authenticated = True
        else:
            print("Matrícula ou senha incorretos. Tente novamente.")

    # Receber questões e enviar respostas
    while True:
        question_data = client.recv(4096).decode() #inicia o loop principal para receber questões e enviar respostas, recebe dados da questão do servidor e os decodifica em uma string
        if not question_data:
            break
        question = json.loads(question_data)
        print(f"\n{question['question']}") #converte os dados da questão em um objeto JSON.

        for idx, option in enumerate(question["options"]): #exibe o enunciado da questão e as opções de resposta.
            print(f"{idx}. {option}")

        student_answer = int(input("Digite o número da resposta correta: ")) #solicita ao aluno que digite o número da resposta correta e armazena na variável student_answer.
        client.send(str(student_answer).encode())

        response = client.recv(1024).decode() #recebe a resposta do servidor sobre a correção da resposta do aluno.
        if response == "CORRECT":
            print("Resposta correta!")
        else:
            print("Resposta incorreta.")

    # Receber resultado final
    result = json.loads(client.recv(4096).decode()) #Recebe o resultado final do servidor e o converte em um objeto JSON.
    print(f"\nTotal de questões: {result['total_questions']}")
    print(f"Total de acertos: {result['correct_answers']}")

    client.close()

if __name__ == "__main__":
    main()

#python client.py 127.0.0.1 1234