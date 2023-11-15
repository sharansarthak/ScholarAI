# Handling recording on client side now so won't be needing this
import cv2
import datetime

def record_video(filename, duration=10):
    # Initialize the video capture object
    cap = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'MP4V') # Using MP4 format
    out = cv2.VideoWriter(filename, fourcc, 30.0, (640, 480)) # Adjusted to 30 fps

    start_time = datetime.datetime.now()
    print("Recording video...")

    while (datetime.datetime.now() - start_time).seconds < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            cv2.imshow('Recording...', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything
    cap.release()
    out.release()
    cv2.destroyAllWindows()