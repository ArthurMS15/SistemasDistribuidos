import socket #criar um servidor de rede e se comunicar com o cliente.
import json 
import sys #acessar argumentos da linha de comando e sair do programa.

# Alunos e senhas dicionário contendo matrículas e senhas dos alunos.
students = {
    "12345": "senha123",
    "67890": "senha456"
}

# Questões de múltipla escolha
questions = [
    {
        "question": "Quanto é 2+2?",
        "options": ["4", "5", "6", "3"],
        "answer": 0
    },
    {
        "question": "Qaunto é 3*3?",
        "options": ["16", "6", "9", "27"],
        "answer": 2
    }
]

def main():
    if len(sys.argv) != 2:
        print("Uso: python server.py <porta>") #verifica se a quantidade correta de argumentos foi fornecida
        sys.exit(1)

    port = int(sys.argv[1]) # pega a porta e converte para inteiro
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Cria um novo objeto de socket para o servidor.
    server.bind(('', port)) #Associa o servidor à porta especificada.
    server.listen(1)
    print(f"Servidor escutando na porta {port}...")

    while True:
        conn, addr = server.accept()    #retorna um novo objeto de socket e o endereço do cliente.
        print(f"Conexão estabelecida com {addr}")

        # Autenticação do aluno
        authenticated = False
        while not authenticated: # recebe a matrícula e a senha do aluno e verifica se estão corretas. 
            student_id = conn.recv(1024).decode()
            password = conn.recv(1024).decode()

            if student_id in students and students[student_id] == password:
                authenticated = True
                conn.send("AUTHENTICATED".encode())
            else:
                conn.send("FAILED".encode())

        # Enviar questões e receber respostas
        correct_answers = 0
        for index, question in enumerate(questions):
            question_data = {
                "question": question["question"],
                "options": question["options"]
            }
            serialized_question = json.dumps(question_data).encode().ljust(4096)
            conn.sendall(serialized_question)

            student_answer = int(conn.recv(1024).decode())
            if student_answer == question["answer"]:
                correct_answers += 1
                conn.sendall("CORRECT".encode())
            else:
                conn.sendall("INCORRECT".encode())

        # Enviar resultado final
        result = {
            "total_questions": len(questions),
            "correct_answers": correct_answers
        }
        conn.send(json.dumps(result).encode())
        conn.close()

if __name__ == "__main__":
    main()

#python server.py 1234
