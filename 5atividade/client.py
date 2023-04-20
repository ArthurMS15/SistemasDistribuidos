import grpc
import sys
import quiz_pb2
import quiz_pb2_grpc

def main():
    if len(sys.argv) != 3:
        print("Uso: python client.py <ip_servidor> <porta>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    channel = grpc.insecure_channel(f'{server_ip}:{server_port}')
    stub = quiz_pb2_grpc.QuizServiceStub(channel)
    print("Conectado ao servidor")

    authenticated = False
    while not authenticated:
        student_id = input("Digite sua matrícula: ")
        password = input("Digite sua senha: ")

        response = stub.Authenticate(quiz_pb2.Student(id=student_id, password=password))
        authenticated = response.authenticated

        if not authenticated:
            print("Matrícula ou senha incorretos. Tente novamente.")

    question_stream = stub.GetQuestion(quiz_pb2.Empty())
    correct_answers = 0
    for question in question_stream:
        print(f"\n{question.question}")
        for idx, option in enumerate(question.options):
            print(f"{idx}. {option}")

        student_answer = int(input("Digite o número da resposta correta: "))
        result = stub.SubmitAnswer(quiz_pb2.Answer(answer=student_answer))
        if result.correct:
            print("Resposta correta!")
            correct_answers += 1
        else:
            print("Resposta incorreta.")

    final_result = stub.GetFinalResult(quiz_pb2.Empty())
    print(f"\nTotal de questões: {final_result.total_questions}")
    print(f"Total de acertos: {final_result.correct_answers}")

if __name__ == "__main__":
    main()
