from dragon import Dragon


SERVER = "52.79.237.101"


def main():
    sock = Dragon(SERVER, 6000)
    sock.bind(('', 7000))

    data = b''

    while True:
        try:
            tmp = sock.recv(1500)
        except KeyboardInterrupt:
            open("dragon_recv_frame", "wb").write(data)
            break
        if not tmp:
            break
        data += tmp

    # sock.send(b'Hello world!')

    sock.close()


if __name__ == "__main__":
    main()
