# Echo client program
import socket
import threading
import sys
import time


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self):
        while True:

            try:
                # print('Send message: ')
                message = input('Send message: ')
                self.sock.send(bytes(message, 'utf-8'))
                # time.sleep(0.1)
            except EOFError:
                print('Something gona wrong.')
                sys.exit(1)



    def __init__(self):
        # запускаем сервер, заставляя слушать локалхост
        self.sock.connect(('localhost', 4242))
        thread = threading.Thread(target=self.send_message)
        thread.daemon = True
        thread.start()


        while True:
            print(threading.active_count())
            data = self.sock.recv(1024)
            if not data:
                break
            print(str(data, 'utf-8'))



if __name__ == '__main__':
    client = Client()
    client.send_message()