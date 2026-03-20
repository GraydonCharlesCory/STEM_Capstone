import cv2
import threading
import time

class camera:
    def __init__(self, camera_index=0):
        # 0 is usually the built-in webcam
        self.cap = cv2.VideoCapture(camera_index)
        self.latest_frame = None
        self.stopped = False
        
        if not self.cap.isOpened():
            print("Error: Could not open laptop camera.")
            return

        # Start the background thread
        threading.Thread(target=self.update, daemon=True).start()

    def update(self):
        while not self.stopped:
            ret, frame = self.cap.read()
            if ret:
                self.latest_frame = frame
            else:
                print("Failed to grab frame from laptop camera.")
            
            # Webcams have a hardware limit (usually 30fps)
            # A tiny sleep keeps the CPU from spinning too fast
            time.sleep(1/30)

    def get_image(self):
        return self.latest_frame

    def stop(self):
        self.stopped = True
        self.cap.release()

