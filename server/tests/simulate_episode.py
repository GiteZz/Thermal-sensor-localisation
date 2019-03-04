import threading

def test_print():
    print("Hello World!")

timer = threading.Timer(2.0, test_print)
timer.start()
print("exit")