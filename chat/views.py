from django.shortcuts import render

from chat.models import RoomClock
import threading

# Create your views here.

def say_hi(room_clock):
    print("This function is executed by thread")
    print("Hiii")
    print(room_clock)


def index(request):
    room_clock = RoomClock.objects.get(room_code="rupesh")
    t=threading.Timer(10,say_hi,[room_clock])
    t.start()


    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})