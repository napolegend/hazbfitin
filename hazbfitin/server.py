"""
В этом файле реализована логика работы сервера
"""
import grpc
from concurrent import futures
import messenger_pb2_grpc
import messenger_pb2


class ChattingServicer(messenger_pb2_grpc.ChattingServicer):
    """
    Этот класс реализует процедуры ChatStream и SendMessage со стороны сервера
    """

    def __init__(self):
        self._history = []
        self._user_list = []

    def ChatStream(self, request, context):
        """
        Получаем запрос содержащий ник и последнюю метку,
        отправляем в поток сообщения только начиная с метки
        """
        last_read = request.mark - 1
        if request.nickname in self._user_list:
            # Возвращаем особое сообщение, если ник уже занят
            yield messenger_pb2.Message(nickname="System", cipher_text=b'Already taken', tag=b'00', nonce=b'00')
            return
        self._user_list.append(request.nickname)
        # Бесконечно отправляем сообщения, пока соединение активно
        while context.is_active():
            # Отправляем все сообщения из очереди неотправленных
            while last_read < len(self._history) - 1:
                last_read += 1
                message = self._history[last_read]
                if message.nickname != request.nickname:
                    yield message

    def SendMessage(self, request, context):
        """
        Эта функция добавляет все поступающие зашифрованные сообщения, откуда дальше их распределяет ChatStream
        """
        self._history.append(request)
        return messenger_pb2.Empty()


def run_server():
    """
     Эта функция запускает сервер и включает прослушивание порта 50051
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=int(input("Максимальное количество участников: "))))
    messenger_pb2_grpc.add_ChattingServicer_to_server(ChattingServicer(), server)
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    print('Listening on port 50051')
    server.wait_for_termination()


if __name__ == '__main__':
    run_server()
