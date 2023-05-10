#!/usr/bin/env python
import threading
import time

def my_func(num):
    time.sleep(2)
    print(f"Thread {threading.current_thread().name} is running and recieved {num}")

# Create three thread objects

thread2 = threading.Thread(target=my_func, name="Thread 2")
thread3 = threading.Thread(target=my_func, name="Thread 3")

# Start the threads


# Run an infinite loop in the main thread
count=0
while True:
    print("Main thread is running")
    time.sleep(2)
    if (count % 3 == 0):
        thread1 = threading.Thread(target=my_func,args=(count,), name="Thread 1")
        thread1.start()
    if (count % 3 == 1):
        thread2 = threading.Thread(target=my_func,args=(count,), name="Thread 2")
        thread2.start()
    if (count % 3 == 2):
        thread3 = threading.Thread(target=my_func,args=(count,), name="Thread 3")
        thread3.start()
    count += 1

    

print("This code will never be reached")
