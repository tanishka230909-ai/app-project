import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7
)

# Drawing utility
mp_draw = mp.solutions.drawing_utils

# Open webcam
camera = cv2.VideoCapture(0)

while True:
    success, frame = camera.read()

    if not success:
        break

    # Mirror image
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands
    results = hands.process(rgb)

    # Draw landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            landmarks = hand_landmarks.landmark

            # Check thumb (right hand)
            thumb_open = landmarks[4].x < landmarks[3].x

            # Check other fingers
            index_open = landmarks[8].y < landmarks[6].y
            middle_open = landmarks[12].y < landmarks[10].y
            ring_open = landmarks[16].y < landmarks[14].y
            pinky_open = landmarks[20].y < landmarks[18].y

            # Open Palm -> HELLO
            if index_open and middle_open and ring_open and pinky_open:
                cv2.putText(
                    frame,
                    "Gesture: HELLO",
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

            # Thumbs Up -> YES
            elif (
                thumb_open
                and not index_open
                and not middle_open
                and not ring_open
                and not pinky_open
            ):
                cv2.putText(
                    frame,
                    "Gesture: YES",
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    2
                )

    cv2.imshow("Sign Language Translator", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()