# TEST accuracy only

from shrimp import Shrimp
import time


def main():
    sock = Shrimp('34.210.120.119', 7000)
    sock.bind(('', 6000))

    fake_frame = bytearray(921600)
    print(time.time())
    sock.send(fake_frame)

    open("shrimp_send_frame", "wb").write(fake_frame)

    # time.sleep(3)
    sock.close()


if __name__ == '__main__':
    main()

