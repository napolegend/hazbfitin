"""
В этом файле реализована логика работы клиента
"""
import threading
import grpc
import messenger_pb2_grpc
import messenger_pb2
import aes
import exceptions


class Client:
    """
    Экземпляры этого класса хранят все данные важные клиенту - адрес сервера, ник пользователя,
    метка последнего сообщения
    """

    def __init__(self, nickname, ip, key):
        for l in nickname:
            if l.lower() not in "abcdefghijklmnopqrstuvwxyz0123456789-_":
                raise exceptions.InvalidNickname(f"Nickname has invalid symbols: {l}")
        self.nickname = nickname
        for l in ip:
            if l.lower() not in "abcdefghijklmnopqrstuvwxyz0123456789-_.":
                raise exceptions.InvalidIP(f"IP address is invalid: {l}")
        self.ip = ip
        self.stub = messenger_pb2_grpc.ChattingStub(grpc.insecure_channel(f"{self.ip}:50051"))
        self._mark = 0
        self.cryptor = aes.CryptoAES(key=key)

    def SendMessage(self):
        """
        Это функция отправляет на сервер вызов удаленной процедуры gRPC, в котором содержится зашифрованное
        сообщение итд, а также в бесконечном цикле функция ждет ввода от пользователя, чтобы отправить его на сервер
        """
        message = messenger_pb2.Message()
        message.nickname = self.nickname
        while True:
            try:
                text_to_encrypt = input()
                message.cipher_text, message.tag, message.nonce = self.cryptor.encrypt(text_to_encrypt)
                self.stub.SendMessage(message)
                self._mark += 1
            except grpc.RpcError as e:
                print(e)

    def ChatStream(self):
        """
        Эта функция запускается в отдельном потоке для того, чтобы сканировать поток сообщений поступающих от сервера,
        Функция выводит эти сообщения на экран
        """
        responses = self.stub.ChatStream(messenger_pb2.Authorize(nickname=self.nickname, mark=self._mark))
        for response in responses:
            # При подключении из потока из ChatStream проверяем, пришло ли особое сообщение о том, что ник занят
            if response.cipher_text != b'Already taken':
                # Если нет, то начинаем слушать этот поток
                break
            else:
                raise exceptions.NicknameAlreadyTaken("Nickname already taken")
        for response in responses:
            self._mark += 1
            print(
                f"{response.nickname}: {self.cryptor.decrypt(response.cipher_text, response.tag, response.nonce).decode('utf-8')}")


def run_client(c):
    """
    Получив экземпляр класса Client, функция запускает сканер потока сообщений и функцию отправки сообщений
    """
    th = threading.Thread(target=c.ChatStream, daemon=True)
    th.start()
    c.SendMessage()
