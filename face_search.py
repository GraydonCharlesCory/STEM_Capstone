import face_recognition
import cv2
import numpy as np
import os
import mediapipe as mp

class face_scanner:
    def __init__(self,downscale = 2):
        self.known_encodings = np.empty((0, 128)) #max of 128 face encodings, can add more later
        self.known_names = np.array([])
        self.scale_factor = downscale

        
    
    def add_reference_face(self, image_path, name):
        image = face_recognition.load_image_file(image_path)
        if len(face_recognition.face_encodings(image)) == 0:
            return
        encoding = face_recognition.face_encodings(image)[0] # assume one face per reference image
        self.known_encodings = np.vstack([self.known_encodings, encoding])
        self.known_names = np.append(self.known_names, name)

    def add_unknown(self, image, location):
        (top, right, bottom, left) = location
        num_unknown = len(os.listdir("faces/unsorted"))

        height, width, _ = image.shape
        padding = int((bottom - top) * 0.3)# add padding around face
        y1 = max(0, top - padding)
        y2 = min(height, bottom + padding)
        x1 = max(0, left - padding)
        x2 = min(width, right + padding)

        face_crop = image[y1:y2, x1:x2]
        cv2.imwrite(f"faces/unsorted/{num_unknown}.jpg", face_crop)
        self.add_reference_face(f"faces/unsorted/{num_unknown}.jpg", f"Unsorted")
    
    def scan(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=1/self.scale_factor, fy=1/self.scale_factor)
        
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB) # Convert from BGR to RGB

        # Find all faces in the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        found_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face
            matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(self.known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index] == True:
                name = self.known_names[best_match_index] #gets the name of the best match, not the first match
            
            found_names.append(name)

        scaled_locations = [(top*self.scale_factor, right*self.scale_factor, bottom*self.scale_factor, left*self.scale_factor) for (top, right, bottom, left) in face_locations] # in case we need to add unknown face
        return  scaled_locations, found_names