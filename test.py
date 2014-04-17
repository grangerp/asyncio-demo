from autobahn.asyncio.websocket import (WebSocketServerProtocol,
    WebSocketServerFactory)
import asyncio


clients = set()


class ChatProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print (request)
        clients.add(self)
        print('connect')

    def onMessage(self, msg, *args):

        print(msg)
        print(args)

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

    asyncio.Task(loop.create_server(factory, '0.0.0.0', 8080))

    loop.run_forever()
