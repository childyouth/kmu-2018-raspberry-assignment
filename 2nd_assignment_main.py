#########################################################################
# Date: 2018/10/02
# file name: 2nd_assignment_main.py
# Purpose: this code has been generated for the 4 wheel drive body
# moving object to perform the project with line detector
# this code is used for the student only
#########################################################################

from car import Car
import time


class myCar(object):

    def __init__(self, car_name):
        self.car = Car(car_name)

    def drive_parking(self):
        self.car.drive_parking()

    # =======================================================================
    # 2ND_ASSIGNMENT_CODE
    # Complete the code to perform Second Assignment
    # =======================================================================
    def car_startup(self):
        # implement the assignment code here
        front_wheel_func = [self.car.steering.center_alignment,
                            self.car.steering.turn_right,
                            self.car.steering.turn_left]
        trace_order = [2,3,1,4,0]
        angle_list = [90,100,80,100,80]
        
        cur_func = 0
        
        line_trace = self.car.line_detector
        front_wheel = self.car.steering
        
        line_status = line_trace.read_digital()
        
        current_angle = 90
        
        self.car.accelerator.go_forward(100)
        while True:
            if not line_trace.is_in_line():
                break
            
            else:
                line_status = line_trace.read_digital()
                if line_status == [0,0,0,0,0] or line_status == [1,1,1,1,1]:
                    break
                for i in trace_order:
                    if i == 1 or i == 3:
                        if line_status[1] & line_status[3]:
                            current_angle = 90
                            cur_func = 0
                            continue
                    if line_status[i]:
                        current_angle = angle_list[trace_order.index(i)]
                if current_angle > 90:
                    cur_func = 1
                elif current_angle < 90:
                    cur_func = 2
                else:
                    cur_func = 0
                if cur_func == 0:
                    front_wheel_func[cur_func]()
                else:
                    front_wheel_func[cur_func](current_angle)
        self.drive_parking()
        """self.car.steering.turn_left(70)
        time.sleep(1)
        self.car.steering.turn_right(110)
        time.sleep(1)"""


if __name__ == "__main__":
    try:
        myCar = myCar("CarName")
        myCar.car_startup()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        myCar.drive_parking()