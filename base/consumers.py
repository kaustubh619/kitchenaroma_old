import json
from channels.generic.websocket import WebsocketConsumer
from .models import OrderTotal, CustomUser
from asgiref.sync import async_to_sync, sync_to_async


class OrderConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = 'user_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        
        orders = OrderTotal.objects.filter(user=user)
        status_dict = {}
        for order in orders:
            status_dict[order.id] = order.status
        self.send(text_data=json.dumps({
            "order_status": status_dict
        }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'order_status',
                "payload": text_data
            }
        )

    def order_status(self, event):
        status = json.loads(event['value'])
        user = self.scope['user']
        orders = OrderTotal.objects.filter(user=user)
        status_dict = {}
        for order in orders:
            status_dict[order.id] = order.status
            
        self.send(text_data=json.dumps({
            "order_status": status_dict
        }))