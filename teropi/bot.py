import zmq
import time
import random


context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt_string(zmq.SUBSCRIBE, "")

socket.connect('tcp://127.0.0.1:2122')


while True:
    topic = random.randrange(9999, 10005)
    message = socket.recv_string()
    print('Obtengo: %s' % message)
    time.sleep(1)
