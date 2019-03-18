import shrimp
import time

print("receiver")
sock = shrimp.Shrimp('localhost', 6000)
sock.bind(('', 7000))


d = sock.recv(1024)
print(d)

# time.sleep(1)
sock.close()
