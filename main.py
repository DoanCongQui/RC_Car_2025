import numpy as np
import cv2 as cv
import constants as constant
import roi_operations as ro
import motor as mt
import time

def initialize_camera():
    """
    Khởi tạo kết nối với camera raspberry 

    Return: // Trả về 
    - cap: khung hình được đọc từ camera  
    """
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print('Cannot open camera')
        exit()
    return cap


def process_frame(frame):
    """

    Lọc nhiễu và khởi tạo các frame

    Trả về:
        - roi: vùng quan tâm
        - frame: khunh ảnh 
        - edges: Khung ảnh canny 
    """
    # Loc nhieu
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    colored_blur = cv.GaussianBlur(frame, (5, 5), 0)
    hsv = cv.cvtColor(colored_blur, cv.COLOR_BGR2HSV)

    # Màu lane trên đường - Lane nào thì tắt coment lane còn lại và chỉnh sửa ==> [make]
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 50, 255])
    #  lower_yellow = np.array([0, 0, 200])
    #  upper_yellow = np.array([180, 25, 255])

    mask = cv.inRange(hsv, lower_white, upper_white)

    roi = mask[constant.ROI_HEIGHT_LOWER_BOUND:constant.ROI_HEIGHT_UPPER_BOUND,
               constant.ROI_WIDTH_LOWER_BOUND:constant.ROI_WIDTH_UPPER_BOUND]

    edges = cv.Canny(blur, 200, 400)

    return roi, frame

def main():
    cap = initialize_camera()

    while True:
        ret, frame = cap.read()
        if not ret:
            print('Can\'t receive frame. Exiting ...')
            break

        # Copy frame 
        frame_original = frame.copy()
        frame_hough = frame.copy()

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        edges = cv.Canny(gray, 50, 150)

        """Khỏi tạo các function"""
        roi, processed_frame= process_frame(frame)

        ro.draw_legend(processed_frame)
        roi_center = ro.find_roi_center()
        ro.draw_roi_center(processed_frame, roi_center)

        roi_lane_center = ro.find_roi_lane_center(roi, roi_center)

        # Khiển tra xem có lane hay không rồi vẽ 
        if roi_lane_center is None:
            direction = "Khong co lane"
        else:
            ro.draw_roi_lane_center(processed_frame, roi_lane_center)
            direction = mt.handle_motor_operations(roi_center, roi_lane_center)

        # khởi tạo hàm hiện thi thông báo bên góc khung hình
        ro.draw_direction_text(processed_frame, direction)

        # Khởi tạo hàm hough_transfrom
        line = ro.hough_transfrom(edges, frame_hough)

        # Tính giá trị lệch và điều khiển động cơ

        mt.run_motor(180)

        if roi_lane_center is not None:
            x, y = roi_lane_center        
            print("Do lech", x-318)
            mt.motor(x-318)
            mt.run_motor(150)
        else:
            mt.send_command("F")
            mt.run_motor(130)
            print(" ")
        # time.sleep(0.1)
        all_frame = ro.stack_images(0.7, ([frame_original, processed_frame], [edges, line]))
        
        # Show khung ảnh
        cv.imshow('All_Frame', all_frame)

        key = cv.waitKey(1)
        if key == ord('q'):
            mt.send_command("S")
            break
        elif key == ord(' '):
            while cv.waitKey(0) != ord(' '):
                pass

    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
