import cv2
import urllib.request
import numpy as np
import threading
import time

class camera:
    def __init__(self, url):
        self.url = url
        self.stream = urllib.request.urlopen(url)
        self.bytes_data = b''
        self.latest_frame = None
        threading.Thread(target=self.update, daemon=True).start() #multithreading to keep getting frames in the background

    def connect(self):
        while True: # Keep trying until successful
            try:
                print("Attempting to connect to ESP32...")
                self.stream = urllib.request.urlopen(self.url, timeout=5)
                self.bytes_data = b''
                print("Connected!")
                break 
            except Exception as e:
                print(f"Connection failed: {e}. Retrying in 2 seconds...")
                time.sleep(2) #don't ddos the esp32
    
    
    def get_new_data(self):
        if len(self.bytes_data) > 1000000:
            print("buffer too full, clearing...")
            self.bytes_data = b''
        try:
            new_data = self.stream.read(1024)
            if not new_data: # If the stream is empty/closed
                self.connect()
            return new_data
        except:
            self.connect()
    
    def update(self):
        while True:
            start = self.bytes_data.rfind(b'\xff\xd8') #start of the last jpeg
            end = -1
            while start == -1:
                new_data = self.get_new_data()
                if new_data is None:
                    continue
                self.bytes_data += new_data
                start = self.bytes_data.rfind(b'\xff\xd8') 
            self.bytes_data = self.bytes_data[start:]
            start = 0

            while end == -1:
                new_data = self.get_new_data()
                if new_data is None:
                    continue
                self.bytes_data += new_data
                end = self.bytes_data.find(b'\xff\xd9', start)# end of the same jpeg
            # print("End: ", end)

            jpg = self.bytes_data[start:end+2]
            self.bytes_data = self.bytes_data[end+2:]
            self.latest_frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            time.sleep(1/30)# limit to 30 fps

    def get_image(self):
        return self.latest_frame
    
    def stop(self):
        pass# only used for laptop camera
