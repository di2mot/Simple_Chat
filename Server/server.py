# Echo server program
import socket
import threading
import sys
import json
import time
import dbase as db


class Server:
    """docstring for Server"""
    # Создаём соккет
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conections = []  # наш пулл подключений
    users_dict = {}  # port : 'login'

    kill_treads = False

    def __init__(self):

        # запускаем сервер, заставляя слушать локалхост
        self.sock.bind(('localhost', 4242))
        # сервер ждёт
        self.sock.listen(1)
        print(f'[{time.strftime("%X")}][Server is working...]')

    def heandler(self, conn, adr):

        while not self.kill_treads:

            try:
                data = conn.recv(1024)

            except ConnectionResetError as errore:
                print(f'[{time.strftime("%X")}] ConnectionResetError: {errore}\n')
                self.conections.clear()
                return False

            if adr in self.users_dict:
                # ЕСли адрес человека в словаре users_dict то работаем

                id = self.users_dict[adr]  # id это ник пользователя

                # преобразуем тест в json
                message = self.message(
                    message_type='message', from_id=id, message_text=data)

                # находим индекс отправителя и отпрвялем не ему
                for connect in self.conections:
                    if connect == conn:
                        pass
                    else:
                        print(f'[{time.strftime("%X")}] connect: {connect}')
                        connect.send(bytes(message, 'utf-8'))

                # отправляем системную информацию по типу True
                system_msg = self.message(message_type='system')
                conn.send(bytes(system_msg, 'utf-8'))

            elif adr not in self.users_dict: # если нет в словаре то регистрация

                type = self.byte_to_json(data)

                if type['message_type'] == 'reg':

                    login_pass = type['message_text']

                    passwd = self.sql_get_pass(login_pass[0])

                    if passwd == login_pass[1]:
                        system_msg = self.message(
                            message_type='message', message_text='Регистрация прошла успешно')
                        conn.send(bytes(system_msg, 'utf-8'))

                        # добавляем чеовека в словарь
                        self.users_dict[adr] = login_pass[0]

                    elif passwd != login_pass[1]:
                        system_msg = self.message(
                            message_type='message', message_text='Неверный логин или пароль')
                        conn.send(bytes(system_msg, 'utf-8'))

                        system_msg = self.message(
                            message_type='sing_in', message_text='Неверный логин или пароль')
                        conn.send(bytes(system_msg, 'utf-8'))


                    system_msg = self.message(
                        message_type='reg', message_text='Регистрация прошла успешно')
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

    def run(self):
        while True:

            try:
                conn, adr = self.sock.accept()

            except Exception as erore:
                print(f'[{time.strftime("%X")}] OSError: {erore}\n')

            # self.kill_treads = False

            # adr это tuple, adr[0] -ip, adr[1] - port
            # просто рисуем крисивый вывод
            text = 'Connetcted'

            time.sleep(0.1)

            print(' ' * (len(text) + len(str(adr[0])) // 2),
                  'ip  ', ' ' * (len(str(adr[1])) // 2), 'port')

            print(f'[{text}: {adr[0]} {adr[1]}]')

            # если порт не в словаре то просим зарегестироваться
            if adr not in self.users_dict:
                text = bytes('Авторизируйтесь', 'utf-8')
                system_msg = self.message(message_type='reg', from_id=[
                                      'localhost', '4242'], message_text=text)

                print(system_msg)
                conn.send(bytes(system_msg, 'utf-8'))

            cTread = threading.Thread(target=self.heandler, args=(conn, adr))

            cTread.demon = True
            cTread.start()
            self.conections.append(conn)

        # sys.exit(1)

    def sql_get_pass(self, login):
        '''
        Я знаю пароль,
        я вижу ориентир,
        только дебаг
        спасёт этот мир

        :param login: строка
        :return: возвращает пароль в виде строки
        '''

        getUser = db.session.query(db.User).filter_by(login=login).first()
        #
        # print(f'getUser: {getUser.password}')
        passwrd = getUser.password
        return passwrd

    def sql_get_id(self, login):
        '''
        Запрос на получения id пользователя
        :param login: строка
        :return: строка
        '''

        getUser = db.session.query(db.User).filter_by(login=login).first()
        #
        # print(f'getUser: {getUser.password}')
        id = getUser.id
        return id

    def sql_add_user(self, login, password):
        '''
        Регистрация нового пользователя
        :param login: строка
        :param password: пароль
        :return: лучи радости
        '''

        newUser = db.User(login, password)
        db.session.add(newUser)
        db.session.commit()
        return True



    def dict_to_json(self, data):
        '''
    dict_to_json =
 {
     'message_type' : 'message' / 'sistem' / 'reg'
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
        b'{"message_type": "system", "message_info": true, "sistem_code": null,
         "from_id": null, "message_text": null}'
        '''

        byte_to_str = str(data, 'utf-8')

        # Load the JSON to a Python list & dump it back out as formatted JSON
        jsonText = json.loads(byte_to_str)

        if jsonText['message_type'] == 'message':
            return jsonText['message_text'], jsonText['from_id']

        elif jsonText['message_type'] == 'system':
            return jsonText["message_info"]

        elif jsonText['message_type'] == 'reg':
            return jsonText["message_text"]

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
            return self.dict_to_json(messege)

        elif message_type == 'message':
            messege['message_type'] = message_type
            messege['from_id'] = f'{from_id[0]}:{from_id[1]}'
            messege['message_text'] = str(message_text, 'utf-8')

            return self.dict_to_json(messege)

        elif message_type == 'reg':
            messege['message_type'] = message_type
            messege['from_id'] = f'{from_id[0]}:{from_id[1]}'
            messege['message_text'] = str(message_text, 'utf-8')
            return self.dict_to_json(messege)

    def draw_con(self, type, adr):

        time.sleep(0.1)
        print(' ' * (len(type) + len(str(adr[0])) // 2),
              'ip  ', ' ' * (len(str(adr[1])) // 2), 'port')

        print(f'[{type}: {adr[0]} {adr[1]}]')


if __name__ == '__main__':
    server = Server()
    server.run()
