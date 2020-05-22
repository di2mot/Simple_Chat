# Echo client program
import socket
import threading
import sys
import time


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self):
        while True:

            if threading.currentThread().getName() == 'MainThread':
                # если  текущий поток главный, то выходим
                print('Exit')
                self.sock.close()   # закрываем соединение
                sys.exit(1)         # выходим из скрипта

            try:

                # print('Send message: ', end='')
                message = input()
                if message == '/stop':          # для выхода из программы
                    self.kill_treads = True     # выключает главный цикл
                else:
                    self.sock.send(bytes(message, 'utf-8'))


            except EOFError:
                print('[Something gona wrong. Connection lost]')
                self.kiil_treads = True




    def __init__(self):
        self.kill_treads = False
        # запускаем сервер, заставляя слушать локалхост
        self.sock.connect(('localhost', 4242))
        print('Соединение активированно\n')
        thread = threading.Thread(target=self.send_message)
        thread.daemon = True
        thread.start()


        while not self.kill_treads:

            data = self.sock.recv(1024)
            if not data:
                break
            print(str(data, 'utf-8'))



if __name__ == '__main__':
    client = Client()
    client.send_message()