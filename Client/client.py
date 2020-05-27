# Echo client program
import socket
import threading
import sys
import time
import json


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    status = None
    login_pass = []

    def send_message(self):
        while True:

            if threading.currentThread().getName() == 'MainThread':
                # если  текущий поток главный, то выходим
                print('Exit')
                # self.sock.close()   # закрываем соединение
                sys.exit(1)         # выходим из скрипта

            try:
                '''
                Что тут происходит: если статуc reg - т.е. предлагаем человеку зарегестрироваться
                Просим ввести логин, пароль, доавляем это в login_pass, а потом отправляем на сервер
                '''

                if self.status == 'reg':
                    print('Введите логин')
                    message = input(f'[{time.strftime("%X")}] ')
                    self.login_pass.append(messege)
                    print('Введите ')
                    message = input(f'[{time.strftime("%X")}] ')
                    self.login_pass.append(messege)

                    messege = self.message(message_type='reg', message_text=self.login_pass)

                    self.sock.send(bytes(message, 'utf-8'))

                    self.status = None

                    continue

                # print('Send message: ', end='')
                message = input(f'[{time.strftime("%X")}] ')

                if message == '/stop':          # для выхода из программы
                    self.kill_treads = True     # выключает главный цикл
                    self.sock.close()           # закрывает сокет. В читающем потоке будет брошено исключение
                else:
                    self.sock.send(bytes(message, 'utf-8'))

            except EOFError:
                print('[Something gona wrong. Connection lost]')
                self.kiil_treads = True

    def __init__(self):
        self.kill_treads = False
        # запускаем сервер, заставляя слушать локалхост
        self.sock.connect(('localhost', 4242))

        print('Соединение установленно\n')

        thread = threading.Thread(target=self.send_message)
        thread.daemon = True
        thread.start()

        while not self.kill_treads:
            try:
                data = self.sock.recv(1024)
            except:
                break

            if not data:
                break

            print(self.byte_to_json(data))
            message, from_id, info = self.byte_to_json(data)

            if message == None:
                pass

            else:
                print(f'[{from_id}]=> {message}')

    def byte_to_json(self, data):
        '''
        принимает байтовый формат и конвертирует в json
        :param data: - bytes
        :return: message_text', 'from_id' / message_info
        '''

        '''
        b'{"message_type": "system", "message_info": true, "sistem_code": null,
         "from_id": null, "message_text": null}'
        '''

        byte_to_str = str(data, 'utf-8')

        # Load the JSON to a Python list & dump it back out as formatted JSON
        jsonText = json.loads(byte_to_str)

        if jsonText['message_type'] == 'message':
            return jsonText['message_text'], jsonText['from_id'], jsonText["message_info"]

        elif jsonText['message_type'] == 'reg':
            self.status = 'reg'
            return jsonText['message_text'], jsonText['from_id'], jsonText["message_info"]

        elif jsonText['message_type'] == 'sing_in':
            self.status = 'login'
            return True

    def dict_to_json(self, data):
        '''
        Преобразует словарь в json формат
        :param data: словарь
        :return: bytes_text
        '''

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

    def message(self, message_type='system',
                message_info=True,
                sistem_code=None,
                from_id=None,
                message_text=None):
        '''

        :param self:
        :param message_type: можкт быть 'message' / 'sistem' / 'reg'
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
            messege['from_id'] = from_id
            messege['message_text'] = str(message_text, 'utf-8')

            return self.dict_to_json(messege)


if __name__ == '__main__':
    client = Client()
    client.send_message()
