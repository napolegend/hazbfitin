import threading
import grpc
import messenger_pb2_grpc
import messenger_pb2


class Client:
    def __init__(self, nickname, ip):
        self.nickname = nickname
        self.ip = ip
        self.stub = messenger_pb2_grpc.ChattingStub(grpc.insecure_channel(f"{self.ip}:50051"))
        self._mark = 0

    def SendMessage(self):
        message = messenger_pb2.Message()
        message.nickname = self.nickname

        while True:
            try:
                message.data = input().encode('utf-8')
                self.stub.SendMessage(message)
                self._mark += 1
            except grpc.RpcError as e:
                print(e)

    def ChatStream(self):
        responses = self.stub.ChatStream(messenger_pb2.Authorize(nickname=self.nickname, mark=self._mark))
        for response in responses:
            self._mark += 1
            print(f"{response.nickname}: {response.data.decode('utf-8')}")


def main():
    c = Client(input("Nickname: "), input("IP: "))
    th = threading.Thread(target=c.ChatStream, daemon=True)
    th.start()
    c.SendMessage()


if __name__ == '__main__':
    main()
