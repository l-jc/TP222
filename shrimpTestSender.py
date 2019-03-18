import shrimp
import time

print("sender")
sock = shrimp.Shrimp('localhost', 7000)
sock.bind(('', 6000))

# t = bytes(f'{time.time()}', encoding='utf-8')

for i in range(3):
    sock.send(b'Hello world')


time.sleep(1)
sock.close()
