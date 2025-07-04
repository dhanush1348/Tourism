import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(
                f"user_{self.scope['user'].id}",
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        if not self.scope["user"].is_anonymous:
            await self.channel_layer.group_discard(
                f"user_{self.scope['user'].id}",
                self.channel_name
            )

    async def receive(self, text_data):
        pass  # Notifications are sent from the server only

    async def notification(self, event):
        await self.send(text_data=json.dumps(event['data']))

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope["user"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user.get_full_name(),
                'timestamp': timezone.now().isoformat()
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

class BookingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.tour_id = self.scope['url_route']['kwargs']['tour_id']
        self.tour_group_name = f'tour_{self.tour_id}'

        await self.channel_layer.group_add(
            self.tour_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.tour_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle seat availability updates
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')
        
        if action == 'check_availability':
            availability = await self.get_tour_availability()
            await self.send(text_data=json.dumps({
                'type': 'availability_update',
                'available_seats': availability
            }))

    async def booking_update(self, event):
        # Send booking updates to connected clients
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_tour_availability(self):
        from bookings.models import TourDate
        try:
            tour_date = TourDate.objects.get(
                tour_id=self.tour_id,
                start_date__gte=timezone.now()
            )
            return tour_date.available_seats
        except TourDate.DoesNotExist:
            return 0 