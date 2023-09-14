import socket

import argparse
import logging
import signal
import asyncio

HOST = '127.0.0.1'
PORT = 8888

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f'Server is listening at {HOST}:{PORT}')

while True:

    

    list = ['woodman', 'Alan', 'Bobo']
    for name in list:
        print(name)


    client_socket, client_address = server_socket.accept()
    print(f'Client connected from {client_address}')

    message = client_socket.recv(1024).decode('utf-8')
    print(f'Received message from client: {message}')

    response = 'Hello from server!'
    client_socket.send(response.encode('utf-8'))

    client_socket.close()