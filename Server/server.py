# Echo server program
import socket
import threading
import sys
import json


class Server:
    """docstring for Server"""
    # Создаём соккет
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conections = []  # наш пулл подключений, поменять на DB
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

                # преобразуем тест в json
                message = self.message(message_type='message', from_id=adr, message_text=data)
                # находим индекс отправителя и отпрвялем не ему
                for connect in self.conections:
                    if connect == conn:
                        pass
                    else:
                        connect.send(bytes(message, 'utf-8'))

                # index = self.conections.index(conn)
                # adres = self.conections[len(self.conections) - index - 1]

                # преобразуем тест в json
                # message = self.message(message_type='message', from_id=adr, message_text=data)
                # adres.send(bytes(message, 'utf-8'))

                # отправляем системную информацию по типу True
                system_msg = self.message(message_type='system')
                conn.send(bytes(system_msg, 'utf-8'))



                if not data:
                    # просто рисуем крисивый вывод
                    text = 'Disconnetcted'
                    print(
                        ' ' * (len(text) + len(str(adr[0])) // 2),
                        'ip  ', ' ' * (len(str(adr[1])) // 2), 'port')

                    print(f'[{text}: {adr[0]} : {adr[1]}]')
                    self.conections.remove(conn)
                    conn.close()
                    break

            except ConnectionResetError as erore:
                self.sock.close()
                self.kill_treads = True
                print(f'[{erore}]: { self.conections}')
                continue
        # sys.exit(1)

    def run(self):
        while not self.kill_treads:
            try:
                conn, adr = self.sock.accept()
                cTread = threading.Thread(target=self.heandler, args=(conn, adr))
                cTread.demon = True
                cTread.start()
                self.conections.append(conn)
                data = self.conections

                # adr это tuple, adr[0] -ip, adr[1] - port
                # просто рисуем крисивый вывод
                text = 'Connetcted'
                print(' ' * (len(text) + len(str(adr[0])) // 2),
                      'ip  ', ' ' * (len(str(adr[1])) // 2), 'port')

                print(f'[{text}: {adr[0]} {adr[1]}]')
            except OSError as erore:
                print(erore)
        sys.exit(1)

    def dict_to_json(self, data):
        '''
 dict_to_json =
 {
     'message_type' : 'message' / 'sistem',
     'message_info' : true / false,
     'sistem_code' : '/stop' / '/users' / '/history',
     'from_id' : 123456 / none,
     'message_text' : 'text' / none
 }
 '''

        bytes_text = json.dumps(data)
        return bytes_text

    def byte_to_json(self, data):


        '''
        b'{"message_type": "system", "message_info": true, "sistem_code": null, "from_id": null, "message_text": null}'
        '''

        byte_to_str = str(data, 'utf-8')

        # Load the JSON to a Python list & dump it back out as formatted JSON
        jsonText = json.loads(byte_to_str)

        if jsonText['message_type'] == 'message':
            return jsonText['message_text'], jsonText['from_id']

        elif jsonText['message_type'] == 'system':
            return jsonText["message_info"]


    def message(self, message_type='system',
                message_info=True,
                sistem_code=None,
                from_id=None,
                message_text=None):
        '''

        :param self:
        :param message_type: можкт быть 'message' / 'sistem'
            'message' - означает что передаётся тестовое соощение
            'sistem' - костыль, передаёт True

        :param message_info: - если message_type -'sistem', то предаёт True
        :param sistem_code: - если message_type -'sistem',
            то несёт управляющие команды

        :param from_id: - от кого сообщение если message_type -'message',
            если'system' то None

        :param message_text: - текст сообщения если message_type -'message',
            если'system' то None

        :return: возвращает словарь который можно преобразовать в
        '''

        '''
         messege =
         {
             'message_type' : 'message' / 'sistem',
             'message_info' : true / false,
             'sistem_code' : '/stop' / '/users' / '/history',
             'from_id' : 123456 / none,
             'message_text' : 'text' / none
         }
         '''

        messege = {
            'message_type': 'system',
            'message_info': True,
            'sistem_code': None,
            'from_id': None,
            'message_text': None
        }

        if message_type == 'system':
            return  self.dict_to_json(messege)

        elif message_type == 'message':
            messege['message_type'] = message_type
            messege['from_id'] = f'{from_id[0]}:{from_id[1]}'
            messege['message_text'] = str(message_text, 'utf-8')

            return self.dict_to_json(messege)


if __name__ == '__main__':
    server = Server()
    server.run()
