from dragon import Dragon
import time
# from utils import Generator

CLIENT = "34.210.120.119"
CPORT = 7000


def main():
    sock = Dragon(CLIENT, CPORT)

    # generator = Generator()
    fake_frame = bytearray(614400)
    sock.bind(('', 6000))
    sock.send(fake_frame)

    open("dragon_send_frame","wb").write(fake_frame)

    print(f"CLEAN")
    time.sleep(3)
    sock.close()


if __name__ == '__main__':
    main()

