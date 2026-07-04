def thumb_is_open(landmarks):
    thumb_tip = landmarks[4]
    thumb_joint = landmarks[3]
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