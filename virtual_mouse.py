import cv2
import mediapipe as mp
import pyautogui
import time

pyautogui.FAILSAFE = False

# Screen resolution for cursor mapping
screen_width, screen_height = pyautogui.size()

# MediaPipe Hands setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Webcam capture
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Smoothing variables (reduce jitter)
prev_x, prev_y = 0, 0
smoothening = 5

# Click cooldown (avoid multiple clicks per pinch)
last_click_time = 0
click_cooldown = 0.5

print("Virtual Mouse started. Press 'q' to quit.")

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)  # Mirror view
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    frame_height, frame_width, _ = frame.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark

            # Landmark 8 = index finger tip, Landmark 4 = thumb tip
            index_finger = landmarks[8]
            thumb = landmarks[4]

            # Convert normalized coordinates to pixel coordinates
            index_x = int(index_finger.x * frame_width)
            index_y = int(index_finger.y * frame_height)
            thumb_x = int(thumb.x * frame_width)
            thumb_y = int(thumb.y * frame_height)

            # Map index finger position to screen coordinates with margin
            frame_margin = 100
            mapped_x = max(frame_margin, min(index_x, frame_width - frame_margin))
            mapped_y = max(frame_margin, min(index_y, frame_height - frame_margin))

            screen_x = int((mapped_x - frame_margin) / (frame_width - 2 * frame_margin) * screen_width)
            screen_y = int((mapped_y - frame_margin) / (frame_height - 2 * frame_margin) * screen_height)

            # Smoothen cursor movement (reduces jitter/shaking)
            curr_x = prev_x + (screen_x - prev_x) / smoothening
            curr_y = prev_y + (screen_y - prev_y) / smoothening

            pyautogui.moveTo(curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

            # Draw circle on index finger tip
            cv2.circle(frame, (index_x, index_y), 10, (0, 255, 0), cv2.FILLED)

            # Calculate distance between thumb and index finger (pinch detection)
            distance = ((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2) ** 0.5

            # If fingers are close together = pinch = click
            if distance < 30:
                cv2.circle(frame, (index_x, index_y), 15, (0, 0, 255), cv2.FILLED)
                current_time = time.time()
                if current_time - last_click_time > click_cooldown:
                    pyautogui.click()
                    last_click_time = current_time

    cv2.imshow("Virtual Mouse", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()