import math
def thumb_is_open(landmarks):
    thumb_tip = landmarks[4]
    thumb_joint = landmarks[3]
    index_knuckle=landmarks[5]
    pinky_knuckle=landmarks[17]
    #thumb side depends on which hand it is
    if index_knuckle[0]<pinky_knuckle[0]:
        if thumb_tip[0]<thumb_joint[0]:
            return True
    else:
        if thumb_tip[0]>thumb_joint[0]:
            return True
    return False

def fingers_up(landmarks):
    fingers=[]
    if thumb_is_open(landmarks):
        fingers.append(1)
    else:
        fingers.append(0)
    finger_ids=[8,12,16,20]

    for i in finger_ids:
        finger_tip = landmarks[i]
        finger_joint = landmarks[i-2]
        if finger_tip[1] < finger_joint[1]:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

def action_detection(fingers):
    total = sum(fingers)
    if total==5:
        return "ACCELERATE"
    elif total==0:
        return "BRAKE"
    else:
        return "NONE"

center_angle = None
def hand_calibration(landmarks):
    global center_angle
    middle_x=landmarks[12][0]
    middle_y=landmarks[12][1]
    wrist_x=landmarks[0][0]
    wrist_y=landmarks[0][1]

    dx = middle_x-wrist_x
    dy = middle_y-wrist_y

    center_angle=math.atan2(dy,dx)
    return center_angle

def steer_value(landmarks):
    if center_angle is None:
        return 0
    else:
        middle_x=landmarks[12][0]
        middle_y=landmarks[12][1]
        wrist_x=landmarks[0][0]
        wrist_y=landmarks[0][1]

        dx = middle_x-wrist_x
        dy = middle_y-wrist_y

        angle=math.atan2(dy,dx)
        steering=angle-center_angle

        #dead zone creation and clamping
        if steering > -0.30 and steering < 0.30:
            steering = 0
        elif steering >=0.30:
            steering=(steering-0.30)/(1-0.30) #starts from 0 at dead zone edge
        else:
            steering=(steering+0.30)/(1-0.30)
        if steering >=1:
            steering =1
        if steering <=-1:
            steering =-1
        return steering