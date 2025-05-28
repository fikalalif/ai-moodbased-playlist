import cv2
from fer import FER

def detect_emotion_from_webcam():
    detector = FER()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        result = detector.top_emotion(frame)
        if result:
            emotion, score = result
            cap.release()
            cv2.destroyAllWindows()
            return emotion

        cv2.imshow('Webcam - Tekan Q untuk capture', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None
