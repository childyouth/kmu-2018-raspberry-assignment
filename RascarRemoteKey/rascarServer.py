# -*- coding: utf-8 -*-
import socket


class rascarKeyServer:
    def run_server(self, port=4000):
        host = ''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))

            s.listen(5)
            print("server:신호 대기중~ 듣고 있어유~")

            conn, addr = s.accept()
            msg = conn.recv(1024).decode('utf8')
            print("server:메시지가 도착했어유~")
            print("수신한 메시지 : ", msg)
            conn.close()
        return msg


if __name__ == '__main__':
    keyServer = rascarKeyServer()
    keyServer.run_server()

