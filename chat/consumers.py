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
from .timer import Timer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connected----------------->>>>>>>>>>>>>>>")
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.timer = Timer(clock=0)


        # Join room group
        # async_to_sync(self.channel_layer.group_add)(    
        #     self.room_group_name, self.channel_name
        # )
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

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

        # print("here-------------------")
        # print(message)
        # self.timer.display_time()

        # if text_data_json.get("get_timer"):
        #     print("get the timer")
        #     await self.channel_layer.group_send(
        #     self.room_group_name, {"type": "chat.message", "message": self.timer.clock }
        # )
        # else:
        #     print("no timer")



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
            self.room_group_name, {"type": "new.message", "message": message + " --> stopped clock."}
        )
        
        elif message == "start":
            self.timer.run_clock = True
            self.timer.start_clock()
            await self.channel_layer.group_send(
            self.room_group_name, {"type": "clock.message", "message": message + " --> started clock."}
        )
            


        else:
            await self.channel_layer.group_send(
            self.room_group_name, {"type": "clock.message", "message": message }
        )
       

        print("done")

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
        if message == "timer":
            data = {"message": message , "get_timer":True}
        else:
            data = {"message": message}
        
        await self.send(text_data=json.dumps(data))
