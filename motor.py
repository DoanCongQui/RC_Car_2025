import constants as constant
import time
import serial

"""Khởi tạo port cho raspberry kết nối vs Arduino"""
ser = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)

def handle_motor_operations(roi_center, roi_lane_center):

    """
    Hiển thị các thông báo hương lái 

    Trả về:
        - direction: Trái, Phải, Đi thẳng
    """
    roi_center_x = roi_center[0]
    roi_lane_center_x = roi_lane_center[0]
    center_difference = roi_center_x - roi_lane_center_x

    direction = 'Stop'
    direction_keys = constant.DIRECTION_THRESHOLDS.keys()

    for direction_key in direction_keys:
        if center_difference in constant.DIRECTION_THRESHOLDS.get(direction_key):
            direction = direction_key
            break

    return direction

"""Mở comment để điều khiển motor"""
def send_command(command):
   ser.write((command + '\n').encode())

def motor(speed):
   if speed > 25:
        speed = (speed / 318) * 400
        send_command(f"R {int(speed)}")
        # send_command(f"S")
   elif speed < -25:
        speed = (abs(speed) / 318) * 400
        send_command(f"L {int(speed)}")
   else:
        send_command(f"F")

def run_motor(speed):
   send_command(f"C {int(speed)}")

def stop():
   send_command(f"S")

if __name__ == '__main__':
    run_motor(150)
    time.sleep(2)
    stop()




