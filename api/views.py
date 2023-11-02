from rest_framework.decorators import api_view
from rest_framework.response import Response
from asgiref.sync import sync_to_async
import asyncio 
import threading

from chat.models import RoomClock


def say_hi(room_clock):
    print("This function is executed by thread")
    print("Hiii")
    print(room_clock)
    room_clock_instance= RoomClock.objects.get(id=room_clock.id)
    room_clock_instance.is_on_hold = True
    room_clock_instance.save()
    print("done")

# @sync_to_async
@api_view(['GET'])
def async_index_api(request):
    # Your asynchronous code here
    print("hello from the async view")
    print("done sleeping")
    room_clock = RoomClock.objects.get(room_code="rupesh")

    t=threading.Timer(10,say_hi,[room_clock])
    t.start()
    return Response({"message": "This is an async response."})