from autobahn.asyncio.websocket import (WebSocketServerProtocol,
    WebSocketServerFactory)
import asyncio


clients = set()


class ChatProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        clients.add(self)
        print('connect')

    def onMessage(self, msg):

        print(msg)

        for c in clients:
            if c is not self:
                c.sendMessage(msg)

    def onClose(self, *args):
        if self in clients:
            clients.remove(self)
        print("remove")


if __name__ == '__main__':
    factory = WebSocketServerFactory("ws://localhost:8080")
    factory.protocol = ChatProtocol

    loop = asyncio.get_event_loop()

    asyncio.Task(loop.create_server(factory, '127.0.0.1', 8080))

    loop.run_forever()
