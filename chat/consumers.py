# chat/consumers.py
# import json

# from channels.generic.websocket import WebsocketConsumer


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         self.send(text_data=json.dumps({"message": message}))


import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer

from chat.models import RoomClock
from .timer import Timer
from channels.db import database_sync_to_async
import threading

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connected----------------->>>>>>>>>>>>>>>")
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        # params = urlparse.parse_qs(message.content['query_string'])
        


        # Join room group
        # async_to_sync(self.channel_layer.group_add)(    
        #     self.room_group_name, self.channel_name
        # )
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        self.room_clock = await self.get_or_create_room_clock(self.room_name)
        self.timer = Timer(clock=self.room_clock.clock)

        t=threading.Timer(10,self.say_hi,[self.room_clock])
        t.start()
        # if self.user_type == "lawyer":
        #     self.timer.start_clock(self.room_clock)


    async def disconnect(self, close_code):
        # Leave room group
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.room_group_name, self.channel_name
        # )
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("receive triggered!!!")
        # print(text_data)
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json["message"]


        if message == "hello":
            await self.timer.say_hi()
            print("i said hi")
    
        # Send message to room group
            await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )
            
        elif message == "sync":
            await self.channel_layer.group_send(
            self.room_group_name, {"type": "timer.message", "message": message }
        )

                 
        elif message == "hi":
              await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message ,"get_timer":True }
        )
              
        elif message == "stop":
            self.timer.stop_clock()
            await self.channel_layer.group_send(
            self.room_group_name, {"type": "clock.message", "message": message + " --> stopped clock."}
        )
        
        elif message == "start":
            user_type= await self.get_user_type()
            if user_type == "lawyer":
                self.timer.run_clock = True
                my_thread = self.timer.start_clock(self.room_clock.id)
                print(my_thread)

                print("<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>")
                await self.channel_layer.group_send(
                self.room_group_name, {"type": "clock.message", "message": message + " --> started clock."}
            )
            else:
                self.timer.run_clock = True
                my_thread = self.timer.start_clock()
                await self.channel_layer.group_send(
                self.room_group_name, {"type": "clock.message", "message": "client cant start the timer"}
            )

        elif message == "time":
            await self.channel_layer.group_send(
            self.room_group_name, {"type": "timer.message", "message": message}
        )   


        else:
            await self.channel_layer.group_send(
            self.room_group_name, {"type": "timer.message", "message": message }
        )
       

        # print("done")

    # Receive message from room group
    async def chat_message(self, event):
        # print("message triggered!!!")
        # print(event)
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    async def clock_message(self,event):
        print("clock message triggered!!")
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))


    async def timer_message(self,event):
        message = event["message"]
        if message == "sync":
            data = {"message": self.timer.clock}
        elif message == "time":
            # clock =await  self.get_room_time(self.room_name)
            clock = self.timer.clock
            data = {"message": clock}
        else:
            data = {"message": message}
        
        await self.send(text_data=json.dumps(data))
    
    def say_hi(self,room_clock):
        print("This function is executed by thread")
        print("Hiii")
        print(room_clock)
        room_clock_instance= RoomClock.objects.get(id=room_clock.id)
        print(room_clock_instance.is_on_hold)

        room_clock_instance.is_on_hold = True
        room_clock_instance.save()
        print("adter saving")
        print(room_clock_instance.is_on_hold)

        print("done")

    
    @database_sync_to_async
    def get_or_create_room_clock(self,room_code):
        print("getr or cresate room clock")
        room_clock, created =RoomClock.objects.get_or_create(room_code=room_code)
        return room_clock
    
    @database_sync_to_async
    def get_room_time(self,room_code):
        print("getr or cresate room clock")
        room_clock =RoomClock.objects.get(room_code=room_code)
        return room_clock.clock
    
    @database_sync_to_async
    def get_user_type(self):
        # print("getr or cresate room clock")
        user = self.scope["user"]
        print(user.username)
        if user.username == "admin":
            return "lawyer"
        return "client"
    

    
