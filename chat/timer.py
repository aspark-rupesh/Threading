import asyncio
import threading
import time

from chat.models import RoomClock
class Timer:
    def __init__(self,clock):
        print("*******init called*******")
        self.clock = clock 
        # self.thread = threading.Thread(target=self.start_clock)
        self.run_clock = True
        # self.clock_running = False
        # self.thread.start()

    
    async def say_hi(self,name=None):
        print(f"Hello {name}" if name else "Hello there.")
        # self.start_timer()

    # async def start_timer(self):
    #     while True:
    #         await asyncio.sleep(1)
    #         self.clock +=1
    #         print(self.clock)

            # print("1 sec elapsed")

        

    def display_time(self):
        # self.clock += 1
        print(self.clock)  
    
    def play_clock(self,room_clock_id):
        if room_clock_id:
            room_clock_id = room_clock_id
            room_clock_instance= RoomClock.objects.get(id=room_clock_id)
            while self.run_clock:
                room_clock_instance= RoomClock.objects.get(id=room_clock_id)

                # await asyncio.sleep(1)
                time.sleep(1)
                self.clock +=1
                if room_clock_instance:
                    room_clock_instance.clock = self.clock
                    if room_clock_instance.is_on_hold:
                        self.run_clock = False
                    room_clock_instance.save()
                    

                print(self.clock)
        else:
            while self.run_clock:
                # await asyncio.sleep(1)
                time.sleep(1)
                self.clock +=1
                if room_clock_id:
                    room_clock_id.clock = self.clock
                    room_clock_id.save()

                print(self.clock)

        

    def start_clock(self,room_clock_id=None):
        print("*******Clock Sarted*******")
        self.thread = threading.Thread(target=self.play_clock,args=(room_clock_id,))
        self.thread.start()
        return self.thread

        
    
    def stop_clock(self):
        print(self.thread.is_alive())
        self.run_clock = False
        print(self.thread.is_alive())

    
    def get_clock(self):
        return self.clock





# a=Timer()


# a.say_hi()
