import shrimp
import time

print("receiver")
sock = shrimp.Shrimp('localhost', 6000)
sock.bind(('', 7000))

for i in range(3):
    d = sock.recv(1024)
    print(d)

# time.sleep(1)
sock.close()
