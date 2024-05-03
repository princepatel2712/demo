import json
from time import sleep
from channels.generic.websocket import WebsocketConsumer
from random import randint


class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        for i in range(500):
            self.send(json.dumps({'message': randint(1, 100)}))
            sleep(2)
