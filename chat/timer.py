import asyncio
import threading
import time
class Timer:
    def __init__(self,clock):
        print("*******init called*******")
        self.clock = clock 
        # self.thread = threading.Thread(target=self.start_clock)
        self.run_clock = True
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
    
    def play_clock(self):
        while self.run_clock:
            # await asyncio.sleep(1)
            time.sleep(1)
            self.clock +=1
            print(self.clock)
        

    def start_clock(self):
        print("*******Clock Sarted*******")
        self.thread = threading.Thread(target=self.play_clock)
        self.thread.start()

        
    
    def stop_clock(self):
        print(self.thread.is_alive())
        self.run_clock = False
        print(self.thread.is_alive())

    
    def get_clock(self):
        return self.clock





# a=Timer()


# a.say_hi()
