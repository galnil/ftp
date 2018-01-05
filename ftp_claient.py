# packet stracture - dict with the following keys and values:
# type - the type of the request. can be one of:
# i - input request - the user need to input answer for the request
# m - message
# d - data
# c - command request - which will be answered by input from the user
# a - acknowlegment


import socket
import pickle
import sys
import pdb
from ftp_constants import *

class Ftp():
    """
    start socket connection
    """
    def __init__(self, ip, port, data_dict):
        self._ip = ip
        self._port = port
        self._data_dict = data_dict
        self.__dict__.update(self._data_dict) # add the data dict content to the attributes dicionary
        try:
            self._my_socket = socket.socket()
            self._my_socket.connect((self._ip, self._port))
        except (ConnectionRefusedError, OSError):
            print('can not connect to the servere\npls check your conectaion')
            sys.exit(1)

    def send_header(self):
        """
        send the connection data dict to the server
        and check if acknolgment packet has arrived
        """
        self._my_socket.send(pickle.dumps(self._data_dict))

    def recive_from_server(self):
        packet = pickle.loads(self._my_socket.recv(self.recv_len))
        print(packet)
        self.__dict__.update(packet)

    def display_server_data(self):
        print(self.data)

    def send_packet(self, type, data, params=''):
        packet  = {}
        packet['type'] = type
        packet['lentgh'] = sys.getsizeof(data)
        packet['data'] = data
        packet['params'] = params
        pdb.set_trace()
        self._my_socket.send(pickle.dump(packet))

    def send_user_input(self):
        user_input = input("")
        try:
            user_input_list = user_input.split(' ')
            command = user_input_list[0]
            params = user_input_list[1]
        except TypeError:
            print('invalid input')
        try:
            self.send_packet('c', user_input, params)
        except ConnectionRefusedError:
            print('connection error accured')

    def download(self, file_name):
        downloaded_file = open('file_name', 'wb')
        data = self._my_socket.recv(self.recv_len)
        while data:
            downloaded_file.write(data)
            data = self._my_socket.recv(self.recv_len)

    def upload(self, file_name):
        self.send_packet('d', file_name)
        uploaded_file = open(file_name, 'rb')
        data = uploaded_file.read(self.rcv_len)
        while data:
            self._my_socket.send(data)
            data = uploaded_file.read(self.rcv_len)

    def listen(self):
        """
        the prefix can be one of the following:
        i - input request
        d - data packet
        m - message
        a - acnolgment
        :return:
        """
        while True:
            self.recive_from_server()
            if 'c' in self.type:
                self.display_server_data()
                self.send_user_input()
            if 'm' in self.type:
                self.display_server_data()
            if  self.type == 'd':
                self.download()
            #if 'e'

class packet():
    def __init__(self):
        self.sperator = seprator


def main():
    ftp = Ftp(IP, PORT, DATA_DICT)
    ftp.send_header()
    ftp.recive_from_server()
    ftp.display_server_data()
    ftp.send_user_input()
    #ftp.listen()


if __name__=='__main__':
    main()