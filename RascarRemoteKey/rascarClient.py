# -*- coding: utf-8 -*-
import socket
import sys
# import RPi.GPIO as GPIO
import time


class rascarKeyClient:
    def __init__(self, host, port=4000):
        # self.GPIO_PIN_NUMBER = 36
        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(self.GPIO_PIN_NUMBER, GPIO.IN)
        self.host = host
        self.port = port

    def send_data_to_server(self, data):
        ADDR = (self.host, self.port)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            #buttonState = GPIO.input(self.GPIO_PIN_NUMBER)
            buttonState = True
            print(buttonState)
            if buttonState:
                try:
                    client_socket.connect(ADDR)
                    client_socket.send(bytes(data, 'utf8'))
                    print("client:정보보냈구유~")
                except Exception as e:
                    print("client:뭔가 잘못됬어유..", e)
                except KeyboardInterrupt:
                    print("client:종료신호 받았으유~")
                finally:
                    break
            time.sleep(0.05)


if __name__ == '__main__':
    try:
        host = input("Input Host IP : ")
        print(host)
        keyClient = rascarKeyClient(host)
        keyClient.send_data_to_server("start to drive")

    except Exception as e:
        print(e)



