import camera_server, laptop_camera, face_search
import time
import cv2
import os
import pyttsx3
import threading
tts = pyttsx3.init()


face_removal_frames = 300
ip = "172.20.10.12" #esp32 cam ip address
cam = camera_server.camera("http://" + ip + ":81/stream")
# cam = laptop_camera.camera(0)
time.sleep(0.5) 

scanner = face_search.face_scanner(downscale=1 )
# Load reference faces
for directory in os.listdir("faces"):
    if directory == "unsorted":
        continue
    for filename in os.listdir(f"faces/{directory}"):
        scanner.add_reference_face(f"faces/{directory}/{filename}", directory)

faces_in_frame = [] #so that it doesn't keep announcing every frame
face_last_seen = {}


def face_recognition_loop():
    locations, names = scanner.scan(image)
    
    for location, name in zip(locations, names):
        if name != "Unknown" and name not in faces_in_frame:
            faces_in_frame.append(name)
            print(f"{name} detected!")
            if "Unsorted" not in name:
                tts.say(name)
                threading.Thread(target=tts.runAndWait).start() # run in separate thread so it doesn't block the main loop
                # tts.runAndWait() 
        elif name == "Unknown":
            tts.say("Unknown person detected")
            threading.Thread(target=tts.runAndWait).start() # run in separate thread so it doesn't block the main loop
            # tts.runAndWait()
            print("Unknown face detected.")
            scanner.add_unknown(image, location)
            

    # check for face that aren't there anymore, and remove them after a certain number of frames
    for face in faces_in_frame[:]:
        if face not in names:
            face_last_seen[face] = face_last_seen.get(face, 0) + 1
            if face_last_seen[face] > face_removal_frames:
                print(f"{face} left the frame.")
                faces_in_frame.remove(face)
                del face_last_seen[face]

while True:
    # print("getting image")
    image = cam.get_image() 
    if image is None: continue

    image = cv2.rotate(image,cv2.ROTATE_180) #for esp32 cam orientation
    cv2.imshow("graydon's capstone project", image)

    # threading.Thread(target=face_recognition_loop).start() # run face recognition in separate thread so it doesn't block the main loop
    face_recognition_loop()

    
    # print("image got")
    cv2.waitKey(10)
    if cv2.getWindowProperty("graydon's capstone project", cv2.WND_PROP_VISIBLE) < 1:
        break

    if 0xFF == ord('q'):
        break

cam.stop()
cv2.destroyAllWindows()
