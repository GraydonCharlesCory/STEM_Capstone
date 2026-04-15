# Graydon's Capstone Project
The esp32_cam folder holds all the needed code for the esp32 side of things

In order to run the server run main.py, you may need to change the esp32's ip
### Camera
If using the esp32 make sure the ip,cam = camera_server..., and image rotation lines arent commented out, and the cam = laptop_camera is commented out

If using the laptop camera, make sure it is the opposite

# todo
 - [x] Get the images from esp32
 - [x] Implement facial recognition with the face_recognition library
 - [x] Add text to speech to read out names
 - [x] Add a way to walk the directory to add reference faces and people
 - [x] Clip unknown faces and add them to a directory
 - [x] Decrease video quality to increase streaming speed
 - [x] Add multithreading for facial recognition
 - [ ] Use mediapipe's more advanced facial detection
 - [ ] Add ui
 - [ ] Build bone conduction earpiece
 - [x] Build nametag houses
 - [ ] Port to phone
