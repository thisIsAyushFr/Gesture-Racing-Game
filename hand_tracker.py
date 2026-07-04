import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands=mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_draw = mp.solutions.drawing_utils

    def frame_processing(self,frame):
        rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)
        landmarks = []
        if result.multi_hand_landmarks:
            hand_marks = result.multi_hand_landmarks[0]
            self.mp_draw.draw_landmarks(frame,hand_marks,self.mp_hands.HAND_CONNECTIONS)

            for i in hand_marks.landmark:
                landmarks.append((i.x,i.y))
        return frame,landmarks
