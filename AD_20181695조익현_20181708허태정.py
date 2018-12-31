#########################################################################
# Date: 2018/11/09
# file name: 3rd_assignment_main.py
# Purpose: this code has been generated for the 4 wheel drive body
# moving object to perform the project with line detector
# this code is used for the student only
#########################################################################

from car import Car
import RPi.GPIO as GPIO
import threading
import time
import operator
import RascarRemoteKey.rascarServer as Server


class myCar(object):
    def __init__(self, car_name):
        self.car = Car(car_name)
        self.currentStat = ""
        self.currentSensorSet = [0, 0, 0, 0, 0]
        self.led_pinR = 37
        self.buzzer_pin = 8
        """
        음계별 표준 주파수
        [ 도, 레, 미, 파, 솔, 라 시, 도]
        """
        self.scale = [261.6, 293.6, 329.6, 349.2, 391.9, 440.0, 493.8, 523.2]
        GPIO.setup(self.led_pinR, GPIO.OUT)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)

        self.is_end_car_horn = False
        self.lock = threading.Lock()
        self.green_light = False
        self.yellow_light = False
        self.end_car = False
        self.time_check = 0  # 신호등 감지했을 때 그떄의 시간 저장

    def drive_parking(self):
        self.car.drive_parking()

    # =======================================================================
    # 3rd_ASSIGNMENT_CODE
    # Complete the code to perform Second Assignment
    # =======================================================================
    def turn_right(self, angle):
        self.car.steering.turn_right(89 + angle)

    def turn_left(self, angle):
        self.car.steering.turn_left(90 - angle)

    def car_horn(self):
        p = GPIO.PWM(self.buzzer_pin, 100)

        for i in range(3):
            p.start(5)  # start the PWM on 5% duty cycle
            p.ChangeFrequency(self.scale[0])
            time.sleep(0.5)
            p.stop()

        p.stop()
        self.lock.acquire()
        self.is_end_car_horn = True
        self.lock.release()

    def turning_signal(self):
        cnt = 0
        while cnt < 4:
            GPIO.output(self.led_pinR, True)
            time.sleep(0.5)
            GPIO.output(self.led_pinR, False)
            time.sleep(0.5)
            cnt += 1

    def traffic_light(self):
        while not self.end_car:
            time.sleep(0.3)
            rgb = dict()
            data = self.car.color_getter.get_raw_data()
            rgb['r'] = data[0]
            rgb['g'] = data[1]
            rgb['b'] = data[2]
            rgb = sorted(rgb.items(), key=operator.itemgetter(1), reverse=True)
            if max(rgb[0][1], rgb[1][1], rgb[2][1]) < 100:
                continue
            elif max(rgb[0][1], rgb[1][1]) > 800 and rgb[2][1] > 500:
                continue
            if rgb[0][0] == 'g' and max(rgb[1][1], rgb[2][1]) < 250 and rgb[0][1] > 250:
                print("green")
                self.lock.acquire()
                self.time_check = time.time()
                self.green_light = True
                self.lock.release()
            elif min(rgb[0][1], rgb[1][1]) > 750 and 550 > rgb[2][1]:
                if rgb[0][0] == 'r' and rgb[1][0] == 'g':
                    print("yellow")
                    self.lock.acquire()
                    self.time_check = time.time()
                    self.yellow_light = True
                    self.lock.release()

    def car_startup(self):
#        while True:
#            rawData = self.car.color_getter.get_raw_data()
#            print(rawData)
#            time.sleep(1)
        GPIO.output(self.led_pinR, False)
        status = [
            ("Big Left", [1, 0, 0, 0, 0]),
            ("Middle Left", [1, 1, 0, 0, 0]), ("Middle Left", [0, 1, 0, 0, 0]),
            ("Little Left", [0, 1, 1, 0, 0]),
            ("SuperLittle Left", [1, 1, 1, 0, 0]), ("SuperLittle Left", [1, 1, 1, 1, 0]),
            ("Center", [0, 0, 1, 0, 0]), ("Center", [0, 1, 1, 1, 0]),
            ("Big Right", [0, 0, 0, 0, 1]),
            ("Middle Right", [0, 0, 0, 1, 1]), ("Middle Right", [0, 0, 0, 1, 0]),
            ("Little Right", [0, 0, 1, 1, 0]),
            ("SuperLittle Right", [0, 0, 1, 1, 1]), ("SuperLittle Right", [0, 1, 1, 1, 1]),
            ("Check", [0, 0, 0, 0, 0]), ("Stop", [1, 1, 1, 1, 1])
        ]
        # angles
        big = 15
        mid = 10
        little = 5
        superlittle = 5
        back = 40

        lineTracker = self.car.line_detector
        distance = self.car.distance_detector.get_distance()
        obstacleCounter = 0
        t_color = threading.Thread(target=self.traffic_light)
        t_color.start()
        while True:
            self.car.accelerator.go_forward(40)
            if self.green_light:
                GPIO.output(self.led_pinR,True)
                if (time.time() - self.time_check) > 2:
                    self.green_light = False
                    GPIO.output(self.led_pinR,False)
                else:
                    self.car.accelerator.go_forward(50)
            elif self.yellow_light:
                GPIO.output(self.led_pinR,True)
                if (time.time() - self.time_check) > 2:
                    self.yellow_light = False
                    GPIO.output(self.led_pinR,False)
                else:
                    self.car.accelerator.go_forward(30)
            time.sleep(0.1)
            self.currentSensorSet = lineTracker.read_digital()
            angle = 90
            for stat in status:
                # print(stat[1])
                if self.currentSensorSet == stat[1]:
                    if "Check" in stat[0] and "Back" not in self.currentStat:
                        if "Left" in self.currentStat or 1 in self.currentSensorSet[:2]:  # is Left Side Sensor On?
                            self.currentStat = "Back Right "
                        else:
                            self.currentStat = "Back "
                    else:
                        self.currentStat = stat[0]
                    # print(self.currentStat, end=" distance = ")
                    break

            distance = self.car.distance_detector.get_distance()
            # print(distance)
            if distance <= 27 and distance != -1:
                obstacleCounter += 1
                self.turn_left(20)
                self.car.accelerator.stop()
                t1 = threading.Thread(target=self.car_horn)
                t1.start()
                t2 = threading.Thread(target=self.turning_signal)
                t2.start()
                while not self.is_end_car_horn:
                    continue
                self.lock.acquire()
                self.is_end_car_horn = False
                self.lock.release()
                self.car.accelerator.go_forward(40)
                # 장애물이 감지되면 현재 따라가던 라인을 벗어날떄까지 움직임
                while self.currentSensorSet != [0, 0, 0, 0, 0]:
                    self.currentSensorSet = lineTracker.read_digital()
                self.turn_left(20)
                # 라인을 벗어났다면 중앙의 가이드 라인을 찾을 때까지 움직임
                while self.currentSensorSet == [0, 0, 0, 0, 0]:
                    self.currentSensorSet = lineTracker.read_digital()
                self.turn_right(20)
                self.car.accelerator.go_forward(40)
                # 장애물이 감지되면 현재 따라가던 라인을 벗어날떄까지 움직임
                while self.currentSensorSet != [0, 0, 0, 0, 0]:
                    self.currentSensorSet = lineTracker.read_digital()
                # 라인을 벗어났다면 중앙의 가이드 라인을 찾을 때까지 움직임
                while self.currentSensorSet == [0, 0, 0, 0, 0]:
                    self.currentSensorSet = lineTracker.read_digital()
                self.car.steering.center_alignment()
                self.currentStat = "Left"
                time.sleep(0.55)

            if "superLittle" in self.currentStat:
                angle = superlittle
            elif "little" in self.currentStat:
                angle = little
            elif "Middle" in self.currentStat:
                angle = mid
            elif "Big" in self.currentStat:
                angle = big
            elif "Back" in self.currentStat:
                angle = 45

            if "Center" in self.currentStat:
                self.car.steering.center_alignment()
                continue
            elif "Right" in self.currentStat:
                self.turn_right(angle)
            elif "Left" in self.currentStat:
                self.turn_left(angle)
            if "Back" in self.currentStat:
                self.car.accelerator.go_backward(40)
                while self.currentSensorSet == [0, 0, 0, 0, 0]:
                    self.currentSensorSet = lineTracker.read_digital()
                    # time.sleep(0.01)
                time.sleep(0.25)
                self.car.steering.center_alignment()
                self.car.accelerator.go_forward(40)
                time.sleep(0.13)

            if obstacleCounter >= 2:
                if "Stop" in self.currentStat:
                    break
            time.sleep(0.03)
        self.car.accelerator.stop()
        try:
            self.lock.acquire()
            self.end_car = True
            self.lock.release()
            self.drive_parking()
        except:
            self.car.accelerator.stop()


if __name__ == "__main__":
    try:
        myCar = myCar("CarName")
        server = Server.rascarKeyServer()
        if server.run_server() == "start to drive":
            myCar.car_horn()
            myCar.is_end_car_horn = False
            time.sleep(1)
            myCar.car_startup()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        myCar.drive_parking()
