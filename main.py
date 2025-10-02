import cv2
from directkeys import PressKey, ReleaseKey, space_pressed
import time
import numpy as np
import webbrowser  # For opening Chrome

# Automatically open Chrome
webbrowser.open('https://www.google.com')  # Opens Google, navigate to chrome://dino/ manually
time.sleep(3)  # Wait for page to load and manual navigation

# Video capture
cap = cv2.VideoCapture(0)  # Try 1 if 0 fails
if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

current_action = set()
lower_skin = np.array([0, 0, 0], dtype=np.uint8)  # Widest skin range
upper_skin = np.array([50, 255, 255], dtype=np.uint8)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break
    
    # Convert to HSV for skin detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Debug all contours
    if contours:
        largest_area = 0
        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            print(f"Contour {i} area: {area}")
            if area > largest_area:
                largest_area = area
            if area > 50:  # Low threshold for hand
                print(f"Hand detected, area: {area}")
                cv2.putText(frame, 'Action: Jump!', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                cv2.putText(frame, 'Hand Detected', (420, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                if space_pressed not in current_action:
                    PressKey(space_pressed)
                    current_action.add(space_pressed)
                    time.sleep(0.5)
                    ReleaseKey(space_pressed)
        print(f"Largest contour area this frame: {largest_area}")
    else:
        print("No contours detected")
        cv2.putText(frame, 'Action: None', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        cv2.putText(frame, 'No Hand', (420, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        if space_pressed in current_action:
            ReleaseKey(space_pressed)
            current_action.remove(space_pressed)
    
    # Display with status boxes
    cv2.rectangle(frame, (0, 480), (300, 425), (50, 50, 255), -2)  # Blue status box
    cv2.rectangle(frame, (400, 480), (640, 425), (50, 50, 255), -2)  # Blue status box
    cv2.imshow("Dino Gesture Controller", frame)
    cv2.imshow("Mask", mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Script ended")