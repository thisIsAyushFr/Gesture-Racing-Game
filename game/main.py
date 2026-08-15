from hand_tracker import HandTracker
from gestures import fingers_up,action_detection,steer_value,hand_calibration
import cv2

tracking_object = HandTracker()
cam = cv2.VideoCapture(0)
while True:
    success,frame= cam.read()
    frame = cv2.flip(frame,1)
    frame,landmarks = tracking_object.frame_processing(frame)
    cv2.imshow("camera",frame)

    key = cv2.waitKey(1)& 0xFF
    if key == ord('q'):
        break
    if landmarks:
        fingers= fingers_up(landmarks)
        action = action_detection(fingers)

        if key == ord('c'):
            hand_calibration(landmarks)
            print("Calibration successful")

        steering = steer_value(landmarks)
        
        print(f"Steering: {steering:.2f} | Fingers: {fingers} | Action: {action}")