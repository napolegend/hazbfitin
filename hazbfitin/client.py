import threading

import grpc
import messenger_pb2
import messenger_pb2_grpc


def main():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = messenger_pb2_grpc.MainStub(channel)
        while True:
            try:
                stub.SendMessage(
                    messenger_pb2.Message(nickname="napolegend", datetime="Дыгъуасэ",
                                          encrypted_text=input("Введите сообщение: ").encode('utf-8')))
            except Exception as e:
                print(e)


if __name__ == '__main__':
    main()
