from shrimp import Shrimp
import time


def main():
    sock = Shrimp('localhost', 7000)
    sock.bind(('', 6000))
    last_time = 0
    while True:
        data = sock.recv(921600)
        current_time = time.time()
        if current_time - last_time >= 1.0 / 25.0:
            print(f"{current_time}: {len(data)}")
            last_time = current_time


if __name__ == "__main__":
    main()

