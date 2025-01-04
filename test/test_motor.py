"""
Ham nay de test motor kho moi cam vao

"""

import serial
import time

# Connect Serial Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600)  

time.sleep(2)

default_speed = 400

def send_command(command):
    ser.write((command + '\n').encode())

def move_forward(speed=default_speed):
    send_command(f"R {speed}")
    # send_command(f"R {int(speed)}")

def move_backward(speed=default_speed):
    send_command(f"L {speed}")
    # send_command(f"L {int(speed)}")

def stop_motor():
    send_command("S")

def set_default_speed(speed):
    global default_speed
    default_speed = speed
    print(f"Default speed set to {default_speed}")

def control_motor():
    print("Enter commands to control the motor:")
    print("F [speed] - Move forward with specified speed (default if not specified)")
    print("B [speed] - Move backward with specified speed (default if not specified)")
    print("S - Stop the motor")
    print("D [speed] - Set default speed")
    print("Q - Quit the program")

    while True:
        command = input("Enter command: ").strip().upper()
        if command.startswith('R'):
            parts = command.split()
            if len(parts) == 1:
                move_forward()
            elif len(parts) == 2 and parts[1].isdigit() and 0 <= int(parts[1]) <= 255:
                move_forward(int(parts[1]))
            else:
                print("Invalid speed. Please enter a value between 0 and 255.")
        elif command.startswith('L'):
            parts = command.split()
            if len(parts) == 1:
                move_backward()
            elif len(parts) == 2 and parts[1].isdigit() and 0 <= int(parts[1]) <= 255:
                move_backward(int(parts[1]))
            else:
                print("Invalid speed. Please enter a value between 0 and 255.")
        elif command == 'S':
            stop_motor()
        elif command.startswith('D'):
            parts = command.split()
            if len(parts) == 2 and parts[1].isdigit() and 0 <= int(parts[1]) <= 255:
                set_default_speed(int(parts[1]))
            else:
                print("Invalid speed. Please enter a value between 0 v� 255.")
        elif command == 'Q':
            break
        else:
            print("Invalid command. Please enter F, B, S, D or Q.")

try:
    control_motor()
except KeyboardInterrupt:
    print("Program terminated.")
finally:
    ser.close()
