import grpc
import messenger_pb2
import messenger_pb2_grpc
from concurrent import futures


class MainServicer(messenger_pb2_grpc.MainServicer):
    def __init__(self) -> None:
        pass

    def SendMessage(self, request, context):
        print(f"New message: \n {request.nickname}: {request.encrypted_text.decode('utf-8')}")
        return messenger_pb2.Empty()

    def GetMessages(self, request, context):
        pass


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    messenger_pb2_grpc.add_MainServicer_to_server(MainServicer(), server)
    print("Server started on port 50051")
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
