import dragon
import time

print("sender")
sock = dragon.Dragon('localhost', 7000)
sock.bind(('', 6000))

for i in range(3):
    sock.send(b'Hello world')


time.sleep(1)
sock.close()
