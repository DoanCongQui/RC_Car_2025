"""Khung ảnh vùng quan tâm ROI"""
ROI_WIDTH_LOWER_BOUND = 0
ROI_WIDTH_UPPER_BOUND = 637
ROI_HEIGHT_LOWER_BOUND = 400
ROI_HEIGHT_UPPER_BOUND = 480

""" Màu sắc """
RED_COLOR = [0, 0, 255] 
GREEN_COLOR = [0, 255, 0]  
WHITE_COLOR = [255, 255, 255]
BLACK_DARK = [46, 52, 54]
DARK_BLUE = [78, 154, 6]

"""Hiển thị các thông báo hướng lái"""
DIRECTION_THRESHOLDS = {
    'Di thang': range(-20, 20),
    'Phai': range(-ROI_WIDTH_UPPER_BOUND, -20),
    'Trai': range(20, ROI_WIDTH_UPPER_BOUND)
}
