# TEST accuracy only

from shrimp import Shrimp
import time


CLIENT = "34.210.120.119"
CPORT = 7000

def main():
    sock = Shrimp(CLIENT, CPORT)
    sock.bind(('', 6000))

    fake_frame = bytearray(921600)

    t = time.time()
    sock.send(fake_frame)

    open("shrimp_send_frame", "wb").write(fake_frame)
    print(t)
    # time.sleep(3)
    sock.close()


if __name__ == '__main__':
    main()

