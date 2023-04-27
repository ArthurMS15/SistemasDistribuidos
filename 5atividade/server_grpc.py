import grpc
from concurrent import futures
import sys
import json
import quiz_pb2
import quiz_pb2_grpc

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
        "question": "Quanto é 3*3?",
        "options": ["16", "6", "9", "27"],
        "answer": 2
    }
]

class QuizService(quiz_pb2_grpc.QuizServiceServicer):
    def Authenticate(self, request, context):
        authenticated = request.student_id in students and students[request.student_id] == request.password
        return quiz_pb2.AuthenticationResponse(authenticated=authenticated)

    def GetQuestion(self, request, context):
        question = questions[request.question_index]
        return quiz_pb2.Question(question_index=request.question_index, question=question["question"], options=question["options"])

    def SubmitAnswer(self, request, context):
        question = questions[request.question_index]
        correct = request.answer == question["answer"]
        return quiz_pb2.AnswerResult(correct=correct)

    def GetFinalResult(self, request, context):
        return quiz_pb2.FinalResult(total_questions=len(questions), correct_answers=sum(1 for q in questions if q.get("correct")))

def main():
    if len(sys.argv) != 2:
        print("Uso: python server_grpc.py <porta>")
        sys.exit(1)

    port = int(sys.argv[1])
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    quiz_pb2_grpc.add_QuizServiceServicer_to_server(QuizService(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Servidor gRPC escutando na porta {port}...")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    main()

