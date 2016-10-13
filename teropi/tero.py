#!/usr/bin/env python
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed
import zmq
import os


context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:2122")
HOST = '0.0.0.0'
PORT = 2121
ZMQ_PORT = 2122
USERNAME = 'john'
PASSWORD = 'snow'
HOMEDIR = os.path.expanduser('~/.config/tero')  # only Linux 


class FTPAuthorizer(DummyAuthorizer):

    user_table = {}

    def validate_authentication(self, username, password, handler):
        if not (username == USERNAME and password == PASSWORD):
            raise AuthenticationFailed
        perm = 'elradfmwM'  # CWD, LIST and STOR
        homedir = HOMEDIR 
        if not os.path.exists(homedir):
            os.makedirs(homedir)
        msg_login = 'Welcome aboard user!'
        msg_quit = 'See you soon!'
        dic = {'home': homedir,
               'perm': perm,
               'operms': {},
               'msg_login': str(msg_login),
               'msg_quit': str(msg_quit)
               }
        self.user_table[username] = dic


class MyFTPHandler(FTPHandler):

    def publish_event(self, topic, message):
        socket.send_string("%s %s" % (topic, message))

    def on_file_received(self, filepath):
        topic = 'ftpd_file_received'
        self.publish_event(topic, filepath)

    def on_incomplete_file_received(self, filepath):
        topic = 'ftpd_file_received'
        self.publish_event(topic, filepath)


def main():
    authorizer = FTPAuthorizer()
    handler = MyFTPHandler
    handler.authorizer = authorizer
    server = FTPServer((HOST, PORT), handler)
    server.serve_forever()


if __name__ == '__main__':
    main()
