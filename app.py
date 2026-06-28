import cv2
import mediapipe as mp

# ==============================
# Initialize MediaPipe Hands
# ==============================

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# ==============================
# Open Webcam
# ==============================

camera = cv2.VideoCapture(0)

while True:

    success, frame = camera.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    # Default values
    gesture = "No Gesture"
    status = "No Hand Detected"

    if results.multi_hand_landmarks:

        status = "Hand Detected"

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            landmarks = hand_landmarks.landmark

            # ==========================
            # Finger Detection
            # ==========================

            thumb_open = landmarks[4].x < landmarks[3].x

            index_open = landmarks[8].y < landmarks[6].y
            middle_open = landmarks[12].y < landmarks[10].y
            ring_open = landmarks[16].y < landmarks[14].y
            pinky_open = landmarks[20].y < landmarks[18].y

            # ==========================
            # Gesture Recognition
            # ==========================

            if index_open and middle_open and ring_open and pinky_open:
                gesture = "HELLO"

            elif (
                thumb_open
                and not index_open
                and not middle_open
                and not ring_open
                and not pinky_open
            ):
                gesture = "YES"

            elif (
                not thumb_open
                and not index_open
                and not middle_open
                and not ring_open
                and not pinky_open
            ):
                gesture = "STOP"

            elif (
                index_open
                and middle_open
                and not ring_open
                and not pinky_open
            ):
                gesture = "VICTORY"

    # ==============================
    # USER INTERFACE
    # ==============================

    cv2.rectangle(frame, (0, 0), (640, 120), (40, 40, 40), -1)

    cv2.putText(
        frame,
        "SIGN LANGUAGE TRANSLATOR",
        (50, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Status : {status}",
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Gesture : {gesture}",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.imshow("Sign Language Translator v2.0", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()