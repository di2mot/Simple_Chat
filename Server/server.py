# Echo server program
import socket
import threading


class Server:
    """docstring for Server"""
    # Создаём соккет
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conections = [] # наш пулл подключений, поменять на DB

    def __init__(self):

        # запускаем сервер, заставляя слушать локалхост
        self.sock.bind(('localhost', 4242))
        # сервер ждёт
        self.sock.listen(1)
        print('[Server is working...]')

    def heandler(self, conn, adr):
        while True:
            data = conn.recv(1024)
            for connection in self.conections:
                connection.send(data)
            if not data:
                # просто рисуем крисивый вывод
                text = 'Disconnetcted'
                print(' ' * (len(text) + len(str(adr[0])) // 2), 'ip  ', ' ' * (len(str(adr[1])) // 2), 'port')
                print(f'[{text}: {adr[0]} : {adr[1]}]')
                self.conections.remove(conn)
                conn.close()
                break

    def run(self):
        while True:
            conn, adr = self.sock.accept()
            cTread = threading.Thread(target=self.heandler, args=(conn, adr))
            cTread.demon = True
            cTread.start()
            self.conections.append(conn)
            data = self.conections

            # adr это tuple, adr[0] -ip, adr[1] - port
            # просто рисуем крисивый вывод
            text = 'Connetcted'
            print(' ' * (len(text) + len(str(adr[0])) // 2), 'ip  ', ' ' * (len(str(adr[1])) // 2), 'port')
            print(f'[{text}: {adr[0]} {adr[1]}]')


if __name__ == '__main__':
    server = Server()
    server.run()

