import grpc
import sys
import quiz_pb2
import quiz_pb2_grpc
from server_grpc import questions

def main():
    if len(sys.argv) != 3:
        print("Uso: python client_grpc.py <ip_servidor> <porta>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    channel = grpc.insecure_channel(f"{server_ip}:{server_port}")
    stub = quiz_pb2_grpc.QuizServiceStub(channel)
    print("Conectado ao servidor gRPC")

    authenticated = False
    while not authenticated:
        student_id = input("Digite sua matrícula: ")
        password = input("Digite sua senha: ")

        response = stub.Authenticate(quiz_pb2.AuthenticationRequest(student_id=student_id, password=password))
        authenticated = response.authenticated
        if not authenticated:
            print("Matrícula ou senha incorretos. Tente novamente.")

    for question_index in range(len(questions)): #len(questions)
        question = stub.GetQuestion(quiz_pb2.QuestionRequest(question_index=question_index))
        print(f"\n{question.question}")

        for idx, option in enumerate(question.options):
            print(f"{idx}. {option}")

        student_answer = int(input("Digite o número da resposta correta: "))
        answer_result = stub.SubmitAnswer(quiz_pb2.AnswerSubmission(student_id=student_id, question_index=question_index, answer=student_answer))

        if answer_result.correct:
            print("Resposta correta!")
        else:
            print("Resposta incorreta.")

    final_result = stub.GetFinalResult(quiz_pb2.FinalResultRequest(student_id=student_id))
    print(f"\nTotal de questões: {final_result.total_questions}")
    print(f"Total de acertos: {final_result.correct_answers}")

if __name__ == "__main__":
    main()