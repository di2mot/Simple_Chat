# Echo server program
import socket
import threading
import sys

class Server:
    """docstring for Server"""
    # Создаём соккет
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conections = [] # наш пулл подключений, поменять на DB
    kill_treads = False

    def __init__(self):


        # запускаем сервер, заставляя слушать локалхост
        self.sock.bind(('localhost', 4242))
        # сервер ждёт
        self.sock.listen(1)
        print('[Server is working...]')

    def heandler(self, conn, adr):
        while not self.kill_treads:
            try:
                data = conn.recv(1024)

                # находим индекс отправителя и отпрвялем не ему
                index = self.conections.index(conn)
                adres = self.conections[len(self.conections) - index - 1]

                message = f'[{adr[0]}:{adr[1]}] => '
                adres.send(bytes(message, 'utf-8') + data)
                conn.send(adr)
                print(message)



                if not data:
                    # просто рисуем крисивый вывод
                    text = 'Disconnetcted'
                    print(' ' * (len(text) + len(str(adr[0])) // 2), 'ip  ', ' ' * (len(str(adr[1])) // 2), 'port')
                    print(f'[{text}: {adr[0]} : {adr[1]}]')
                    self.conections.remove(conn)
                    conn.close()
                    break

            except ConnectionResetError:
                self.kill_treads = True
                print('[Errore]: ', self.conections)
        sys.exit(1)

    def run(self):
        while not self.kill_treads:
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
        sys.exit(1)


if __name__ == '__main__':
    server = Server()
    server.run()

