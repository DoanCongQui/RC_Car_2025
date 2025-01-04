import cv2

# Kh?i d?ng camera
cap = cv2.VideoCapture(0)  # S? d?ng camera m?c d?nh (0)

# Ki?m tra camera có m? du?c không
if not cap.isOpened():
    print("Không th? m? camera.")
    exit()

# Ð?c liên t?c t? camera
while True:
    # Ð?c m?t frame t? camera
    ret, frame = cap.read()
    
    # Ki?m tra frame có du?c d?c thành công không
    if not ret:
        print("Không th? nh?n frame.")
        break

    # Chuy?n sang ?nh xám (grayscale)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Áp d?ng Canny Edge Detection
    edges = cv2.Canny(gray, 50, 150)  # Tham s? 50 và 150 là ngu?ng du?i và ngu?ng trên

    # Hi?n th? video g?c và video v?i c?nh
    cv2.imshow("Camera - Original", frame)
    cv2.imshow("Camera - Canny Edges", edges)

    # Thoát khi nh?n phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Gi?i phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
