import grpc
from concurrent import futures
import quiz_pb2
import quiz_pb2_grpc
import sys

students = {
    "12345": "senha123",
    "67890": "senha456"
}

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

class QuizServiceServicer(quiz_pb2_grpc.QuizServiceServicer):
    def Authenticate(self, request, context):
        student_id = request.id
        password = request.password
        authenticated = student_id in students and students[student_id] == password
        return quiz_pb2.AuthResponse(authenticated=authenticated)

    def GetQuestion(self, request, context):
        for question in questions:
            yield quiz_pb2.Question(question=question["question"], options=question["options"])

    def SubmitAnswer(self, request, context):
        student_answer = request.answer
        question_index = self.question_counter
        self.question_counter += 1
        correct = student_answer == questions[question_index]["answer"]
        if correct:
            self.correct_answers += 1
        return quiz_pb2.Result(correct=correct)

    def GetFinalResult(self, request, context):
        return quiz_pb2.FinalResult(total_questions=len(questions), correct_answers=self.correct_answers)

def serve():
    if len(sys.argv) != 2:
        print("Uso: python server.py <porta>")
        sys.exit(1)

    port = int(sys.argv[1])
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    quiz_pb2_grpc.add_QuizServiceServicer_to_server(QuizServiceServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Servidor escutando na porta {port}...")

    try:
        while True:
            time.sleep(60 * 60 * 24)  # Serve por um dia
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()

