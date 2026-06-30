import cv2
import mediapipe as mp

# =====================================
# MediaPipe Initialization
# =====================================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# =====================================
# Finger Detection Functions
# =====================================

def is_thumb_open(landmarks):
    return (
        landmarks[4].x < landmarks[3].x
        and landmarks[3].x < landmarks[2].x
    )


def is_index_open(landmarks):
    return (
        landmarks[8].y < landmarks[6].y
        and landmarks[6].y < landmarks[5].y
    )


def is_middle_open(landmarks):
    return (
        landmarks[12].y < landmarks[10].y
        and landmarks[10].y < landmarks[9].y
    )


def is_ring_open(landmarks):
    return (
        landmarks[16].y < landmarks[14].y
        and landmarks[14].y < landmarks[13].y
    )


def is_pinky_open(landmarks):
    return (
        landmarks[20].y < landmarks[18].y
        and landmarks[18].y < landmarks[17].y
    )


# =====================================
# Gesture Recognition
# =====================================

def detect_gesture(landmarks):

    thumb = is_thumb_open(landmarks)
    index = is_index_open(landmarks)
    middle = is_middle_open(landmarks)
    ring = is_ring_open(landmarks)
    pinky = is_pinky_open(landmarks)

    if thumb and index and middle and ring and pinky:
        return "HELLO"

    elif thumb and not index and not middle and not ring and not pinky:
        return "YES"

    elif not thumb and not index and not middle and not ring and not pinky:
        return "STOP"

    elif not thumb and index and not middle and not ring and not pinky:
        return "ONE"

    elif not thumb and index and middle and not ring and not pinky:
        return "VICTORY"

    elif not thumb and index and middle and ring and not pinky:
        return "THREE"

    elif not thumb and index and middle and ring and pinky:
        return "FOUR"

    return "No Gesture"


# =====================================
# Camera Initialization
# =====================================

camera = cv2.VideoCapture(0)

window_name = "Sign Language Translator v4.0"
# =====================================
# Main Loop
# =====================================

while True:

    success, frame = camera.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    gesture = "No Gesture"
    status = "No Hand Detected"

    finger_count = 0

    if results.multi_hand_landmarks:

        status = "Hand Detected"

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            landmarks = hand_landmarks.landmark

            thumb = is_thumb_open(landmarks)
            index = is_index_open(landmarks)
            middle = is_middle_open(landmarks)
            ring = is_ring_open(landmarks)
            pinky = is_pinky_open(landmarks)

            finger_count = sum([
                thumb,
                index,
                middle,
                ring,
                pinky
            ])

            gesture = detect_gesture(landmarks)

    # =====================================
    # UI
    # =====================================

    cv2.rectangle(frame, (0, 0), (640, 150), (35, 35, 35), -1)

    cv2.putText(
        frame,
        "SIGN LANGUAGE TRANSLATOR",
        (70, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    status_color = (0, 255, 0) if status == "Hand Detected" else (0, 0, 255)

    cv2.putText(
        frame,
        f"Status : {status}",
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        status_color,
        2
    )

    cv2.putText(
        frame,
        f"Gesture : {gesture}",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Open Fingers : {finger_count}",
        (20, 135),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 0),
        2
    )

    cv2.putText(
        frame,
        "Press Q to Exit",
        (430, 135),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (180, 180, 180),
        1
    )

    cv2.imshow(window_name, frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# =====================================
# Cleanup
# =====================================

camera.release()
cv2.destroyAllWindows()