# TEST accuracy only

from shrimp import Shrimp
import time


def main():
    sock = Shrimp('localhost', 6000)
    sock.bind(('', 7000))

    fake_frame = bytearray(921600)
    sock.send(fake_frame)

    open("shrimp_send_frame", "wb").write(fake_frame)

    # time.sleep(3)
    sock.close()


if __name__ == '__main__':
    main()

