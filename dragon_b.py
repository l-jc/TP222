import dragon
import time

print("sender")
sock = dragon.Dragon('localhost', 7000)
sock.bind(('', 6000))
sock.send(b'123')

time.sleep(1)

sock.close()
