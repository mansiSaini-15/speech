import cv2
import pyttsx3
from hand_sign_recognition import HandSignRecognition

def start_recognition():
    cap = cv2.VideoCapture(0)
    recognizer = HandSignRecognition()
    engine = pyttsx3.init()

    # Setup full screen OpenCV window
    window_name = "Hand Sign Recognition"
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def mouse_callback(event, x, y, flags, param):
        # Exit button click detection
        if event == cv2.EVENT_LBUTTONDOWN:
            if button_x < x < button_x + button_width and button_y < y < button_y + button_height:
                print("Exit button clicked")
                cap.release()
                cv2.destroyAllWindows()

    cv2.setMouseCallback(window_name, mouse_callback)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Perform hand sign recognition
        detected_vowel = recognizer.detect_hand_sign(frame)

        # Display recognized vowel on screen
        if detected_vowel:
            engine.say(f"The detected vowel is {detected_vowel}")
            engine.runAndWait()

            cv2.putText(frame, f"Detected: {detected_vowel}", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

        # Draw exit button on the frame
        frame_height, frame_width, _ = frame.shape
        button_width, button_height = 120, 50
        button_x = frame_width - button_width - 20
        button_y = frame_height - button_height - 20

        # Draw button background (flat, no outline)
        cv2.rectangle(frame, (button_x, button_y),
                      (button_x + button_width, button_y + button_height), (30, 30, 30), -1)

        # Draw button text
        cv2.putText(frame, "Exit", (button_x + 20, button_y + 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Show the frame
        cv2.imshow(window_name, frame)

        # Press 'q' to quit
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_recognition()
