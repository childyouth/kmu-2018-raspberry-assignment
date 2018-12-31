#########################################################################
# Date: 2018/10/02
# file name: 3rd_assignment_main.py
# Purpose: this code has been generated for the 4 wheel drive body
# moving object to perform the project with line detector
# this code is used for the student only
#########################################################################

from car import Car
import time


class myCar(object):
    def __init__(self, car_name):
        self.car = Car(car_name)

        self.rear = self.car.accelerator
        self.front = self.car.steering

    def drive_parking(self):
        self.car.drive_parking()

    # =======================================================================
    # 3RD_ASSIGNMENT_CODE
    # Complete the code to perform Third Assignment
    # =======================================================================
    def car_startup(self):
        # implement the assignment code here
        self.is_in_guideLine = False
        front_wheel_func = [self.car.steering.center_alignment,
                            self.car.steering.turn_right,
                            self.car.steering.turn_left]
        trace_order = [3, 1, 4, 0]

        cur_func = 0

        line_trace = self.car.line_detector
        front_wheel = self.car.steering

        line_status = line_trace.read_digital()
        current_line_status = line_status
        steer_angle = 90
        last_angle = steer_angle

        self.car.accelerator.go_forward(50)
        flag_cnt = False
        while True:
            distance = self.car.distance_detector.get_distance()
            if distance != -1 and distance <= 25 and not self.is_in_guideLine:
                print("detected")
                # self.front.turn_left(40)
                # time.sleep(0.8)
                # self.front.center_alignment()
                # self.is_in_guideLine = True
                # while not line_trace.is_in_line():
                #     continue
                # time.sleep(0.2)
                # self.is_in_guideLine = False
                # self.front.turn_right(140)
                # time.sleep(1)
                # self.front.center_alignment()
                # while not line_trace.is_in_line():
                #     continue
                # self.front.turn_left(40)
                # time.sleep(0.2)
                self.front.turn_left(40)
                time.sleep(0.8)
                self.front.turn_right(100)
                print("go to guideline")
                while not line_trace.is_in_line():
                    continue
                self.front.turn_right(140)
                print("im in guideline")
                while line_trace.is_in_line():
                    continue
                time.sleep(0.94)
                self.front.center_alignment()
                print("go to line")
                while not line_trace.is_in_line():
                    continue
#                self.rear.stop()
#                self.front.turn_left(40)
#                time.sleep(0.2)

            steer_angle = 90
            line_status = line_trace.read_digital()

            if not line_trace.is_in_line():
                #                if self.is_in_guideLine:
                #                    self.is_in_guideLine = False
                #                    self.front.turn_right(140)
                #                    if line_status[1]:
                #                        time.sleep(1)
                #                    elif line_status[3]:
                #                        time.sleep(1.3)
                #                    elif line_status[2]:
                #                        time.sleep(1)
                #                    self.front.center_alignment()
                #                    while not line_trace.is_in_line():
                #                        continue
                #                    time.sleep(0.2)

                #                else:
                if cur_func == 0:
                    self.car.steering.center_alignment()
                elif cur_func == 1:
                    cur_func = 2
                    front_wheel_func[cur_func](70)
                elif cur_func == 2:
                    cur_func = 1
                    front_wheel_func[cur_func](110)

                self.rear.go_backward(30)
                while not line_trace.is_in_line():
                    # time.sleep(0.1)
                    continue
                time.sleep(0.53)
                self.rear.go_forward(50)

            elif line_status == [1, 1, 1, 1, 1]:
                if flag_cnt:
                    if current_line_status == line_status:
                        continue
                    print("bye bye")
                    break
                flag_cnt = True
                print("we are in the end game now")
            elif line_status == [0, 0, 1, 0, 0] or line_status == [0, 1, 1, 1, 0]:
                cur_func = 0
                steer_angle = 90
                front_wheel_func[cur_func]()
            else:
                if line_status[1]:
                    steer_angle -= 10
                elif line_status[3]:
                    steer_angle += 10
                if line_status[0]:
                    if line_status[1]:
                        steer_angle -= 10
                    else:
                        steer_angle -= 30
                elif line_status[4]:
                    if line_status[3]:
                        steer_angle += 10
                    else:
                        steer_angle += 30
                if steer_angle > 90:
                    cur_func = 1
                elif steer_angle < 90:
                    cur_func = 2
                else:
                    cur_func = 0
                if cur_func == 0:
                    front_wheel_func[cur_func]()
                else:
                    front_wheel_func[cur_func](steer_angle)
#                time.sleep(0.01)
            current_line_status = line_status
            last_angle = steer_angle

        self.drive_parking()


if __name__ == "__main__":
    try:
        myCar = myCar("CarName")
        myCar.car_startup()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        myCar.drive_parking()
