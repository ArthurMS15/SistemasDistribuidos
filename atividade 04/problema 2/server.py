import socket
import json
import sys

# Alunos e senhas
students = {
    "12345": "senha123",
    "67890": "senha456"
}

# Questões de múltipla escolha
questions = [
    {
        "question": "Qual é a capital da França?",
        "options": ["Paris", "Londres", "Berlim", "Madri"],
        "answer": 0
    },
    {
        "question": "Qual é a moeda do Japão?",
        "options": ["Dólar", "Euro", "Iene", "Libra"],
        "answer": 2
    }
]

def main():
    if len(sys.argv) != 2:
        print("Uso: python server.py <porta>")
        sys.exit(1)

    port = int(sys.argv[1])

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', port))
    server.listen(1)
    print(f"Servidor escutando na porta {port}...")

    while True:
        conn, addr = server.accept()
        print(f"Conexão estabelecida com {addr}")

        # Autenticação do aluno
        authenticated = False
        while not authenticated:
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
            conn.send(json.dumps(question_data).encode())
            student_answer = int(conn.recv(1024).decode())

            if student_answer == question["answer"]:
                correct_answers += 1
                conn.send("CORRECT".encode())
            else:
                conn.send("INCORRECT".encode())

        # Enviar resultado final
        result = {
            "total_questions": len(questions),
            "correct_answers": correct_answers
        }
        conn.send(json.dumps(result).encode())
        conn.close()

if __name__ == "__main__":
    main()
