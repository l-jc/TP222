import dragon
import time

print("receiver")
sock = dragon.Dragon('localhost', 6000)
sock.bind(('', 7000))

for i in range(3):
    d = sock.recv(1024)
    print(d)

# time.sleep(1)
sock.close()
