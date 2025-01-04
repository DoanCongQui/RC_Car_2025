import cv2 as cv
import constants as constant
import numpy as np

def find_roi_center():
    """
    Tính toán tọa độ tâm của ROI (vùng quan tâm).
    
    Trả về:
    - x, y: Tọa độ trung tâm của ROI.
    """
    width = constant.ROI_WIDTH_UPPER_BOUND - constant.ROI_WIDTH_LOWER_BOUND
    height = constant.ROI_HEIGHT_UPPER_BOUND - constant.ROI_HEIGHT_LOWER_BOUND
    x, y = int(width/2), int(height/2)

    return x, y

def draw_roi_center(frame, roi_center):
    """
    Vẽ trung tâm của ROI trên khung hình gốc.[Chấm màu đỏ]
    
    Tham số:
    - frame: Khung hình gốc.
    - roi_center: Tọa độ trung tâm của ROI (x, y).
    """
    x = roi_center[0]
    y = roi_center[1] + constant.ROI_HEIGHT_LOWER_BOUND

    cv.circle(frame, (x, y), 4, constant.RED_COLOR, -1)

def draw_roi_lane_center(frame, roi_lane_center):
    """
    Vẽ trung tâm của lane đường trên. [Chấm màu xanh]
    
    Tham số:
    - frame: Khung hình gốc.
    - roi_lane_center: Tọa độ trung tâm của lane đường trong ROI (x, y).
    """
    x = roi_lane_center[0]
    y = roi_lane_center[1] + constant.ROI_HEIGHT_LOWER_BOUND

    cv.circle(frame, (x, y), 5, constant.GREEN_COLOR, 2)

def find_roi_lane_center(roi, roi_center):
    """
    Thuật toán tìm đường cho xe 

    Trả về:
    - roi_lane_center: Giá trị tâm của làn đường đường 
    - left_lane_x: là số dương di chuyển tâm sang phải 
                   là số âm di chuyển tâm sang trái 
    """

    roi_center_x, roi_center_y = roi_center

    # Đặt móc quan tâm cho trái và phải
    right_lane_x = constant.ROI_WIDTH_UPPER_BOUND
    left_lane_x = constant.ROI_WIDTH_LOWER_BOUND

    is_right_lane_detected = False
    is_left_lane_detected = False

    is_stepped = False

    #  Ktra xem xe có nằm trên làn đường hay không
    # if roi[roi_center_y, roi_center_x] == 255:
    #     is_stepped = True
    #     print('stepped on the lane')

    try:
        if roi[roi_center_y, roi_center_x] == 255:
            is_stepped = True
            print('Đã phát hiện xe nằm trên làn đường.')
    except IndexError:
        print("Tâm ROI nằm ngoài giới hạn.")
        return roi_center  # Trả về tâm ROI mặc định
    #  Tìm làn đường bên phải: duyệt từ tâm roi đi về phía bên phải
    for i in range(roi_center_x, constant.ROI_WIDTH_UPPER_BOUND - 1):
        # Tính toán độ rộng của làn bên phải so với tâm roi 
        if is_stepped and roi[roi_center_y, i] != 255:
            lane_width_from_right = i - roi_center_x
            break

        if not is_stepped and roi[roi_center_y, i] == 255:
            is_right_lane_detected = True
            right_lane_x = i
            break

    #  Tìm làn đường bên trai: duyệt từ tâm roi đi về phía bên trai
    for i in range(roi_center_x, constant.ROI_WIDTH_LOWER_BOUND, -1):
        # Tính toán độ rộng của làn bên trai so với tâm roi 
        if is_stepped and roi[roi_center_y, i] != 255:
            lane_width_from_left = roi_center_x - i
            break

        if not is_stepped and roi[roi_center_y, i] == 255:
            is_left_lane_detected = True
            left_lane_x = i
            break

    """ Xác định hướng đi của xe trên làn đường """
    if is_stepped:
        if lane_width_from_right >= lane_width_from_left:
            # Rẽ trái maximum 
            is_right_lane_detected = True
            right_lane_x = roi_center_x
        else:
            # Rẽ phải maximum
            is_left_lane_detected = True
            left_lane_x = roi_center_x

    # Nếu chỉ phát hiện đường bên trái thì + thêm vị trí đường bên phải
    if is_left_lane_detected and not is_right_lane_detected:
        right_lane_x += left_lane_x

    # Ngược lại 
    if not is_left_lane_detected and is_right_lane_detected:
        left_lane_x = -(constant.ROI_WIDTH_UPPER_BOUND - right_lane_x)

    # Nếu không có thấy lane trái hoặc phải = none
    if not is_left_lane_detected and not is_right_lane_detected:
        return None

    half_distance_between_lanes = int((right_lane_x - left_lane_x) / 2)
    roi_lane_center = left_lane_x + half_distance_between_lanes, roi_center_y

    return roi_lane_center

# Hàm trả về frame chứa các đường hough 
def hough_transfrom(edges, frame):
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=50, maxLineGap=150)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return frame

def stack_images(scale, imgArray):
    """
    Hàm nối các khung ảnh lại với nhau 

    Trả về:
    - ver: khung ảnh chứa các khung ảnh khi thêm vào
    """    
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(rows):
            for y in range(cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv.cvtColor(imgArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        for x in range(rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

"""
Thông báo dòng chữ lên phía trên góc trái khung hình thứ 2 [Khung hình điều khiển xe]
"""
def draw_direction_text(frame, direction):
    cv.putText(frame, text='Huong: ' + direction, org=(10, 40), fontFace=cv.FONT_HERSHEY_SIMPLEX,
               fontScale=0.8, color=constant.WHITE_COLOR, thickness=2)

def draw_legend(frame):
    center_circle = cv.circle(frame, (16, 60), 4, constant.RED_COLOR, -1)
    cv.putText(frame, text='- Tam khung hinh', org=(30, 67), fontFace=cv.FONT_HERSHEY_SIMPLEX,
               fontScale=0.8, color=constant.WHITE_COLOR, thickness=2)

    lane_center_circle = cv.circle(frame, (16, 85), 5, constant.GREEN_COLOR, 2)
    cv.putText(frame, text='- Tam lan duong', org=(30, 93), fontFace=cv.FONT_HERSHEY_SIMPLEX,
               fontScale=0.8, color=constant.WHITE_COLOR, thickness=2)
