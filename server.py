from dragon import Dragon
import time
from utils import Generator


def main():
    sock = Dragon('localhost', 7000)

    generator = Generator()
    fake_frame = bytearray(614400)
    sock.bind(('', 6000))
    sock.send(fake_frame)

    open("dragon_send_frame","wb").write(fake_frame)

    print(f"CLEAN")
    time.sleep(3)
    sock.close()


if __name__ == '__main__':
    main()

