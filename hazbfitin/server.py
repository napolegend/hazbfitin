import grpc
from concurrent import futures
import messenger_pb2_grpc
import messenger_pb2


class ChattingServicer(messenger_pb2_grpc.ChattingServicer):
    def __init__(self):
        self._history = []

    def ChatStream(self, request, context):
        last_read = request.mark - 1
        # Бесконечно отправляем сообщения, пока соединение активно
        while context.is_active():
            # Отправляем все сообщения из очереди неотправленных
            while last_read < len(self._history) - 1:
                last_read += 1
                message = self._history[last_read]
                # yield - это как бесконечный return.
                # Функция будет возвращать значения снова и снова, когда вызывается yield.
                # А с другой стороны мы сможем их получать просто циклом for in (вспоминаем итераторы в Python)
                if message.nickname != request.nickname:
                    yield message
            # Добавим маленький sleep, чтобы снизить нагрузку на сервер постоянными проверками новых сообщений

    def SendMessage(self, request, context):
        self._history.append(request)
        print(f"{request.nickname}: {request.data.decode('utf-8')}")
        return messenger_pb2.Empty()


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    messenger_pb2_grpc.add_ChattingServicer_to_server(ChattingServicer(), server)
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    print('Listening on port 50051')
    server.wait_for_termination()
