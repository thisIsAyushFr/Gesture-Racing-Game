import os
import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision,BaseOptions

MODEL_PATH=os.path.join(os.path.dirname(os.path.abspath(__file__)),"hand_landmarker.task")

class HandTracker:
    def __init__(self):
        options=vision.HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=MODEL_PATH),
            num_hands=1
        )
        self.hands=vision.HandLandmarker.create_from_options(options)

    def frame_processing(self,frame):
        rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB,data=rgb)
        result = self.hands.detect(image)
        landmarks = []
        if result.hand_landmarks:
            height,width=frame.shape[:2]
            for i in result.hand_landmarks[0]:
                landmarks.append((i.x,i.y))
                cv2.circle(frame,(int(i.x*width),int(i.y*height)),4,(0,255,0),-1)
        return frame,landmarks
