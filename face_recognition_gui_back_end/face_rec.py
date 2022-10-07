import face_recognition 
import numpy as np 
from PIL import Image , ImageDraw
import os 
import io 
import base64 
class FaceRec :
    def __init__(self,known_person_path_file , unknown_image_path_file , known_name = None) :
        self.known_person_path_file = known_person_path_file 
        self.unknown_image_path_file = unknown_image_path_file
        self.know_name = known_name 
        pass
    def converted_known_image(self):
        return face_recognition.load_image_file(self.known_person_path_file)
    
    def recognize_faces(self):
        for file in os.listdir(self.unknown_images_path_file):
            if(file[0] != '.'):
                known_image = self.converted_known_image()
                known_image_encoding = face_recognition.face_encodings(known_image)[0]
                known_face_encodings =[known_image_encoding]
                known_face_names = [self.know_name]

                unknown_image = face_recognition.load_image_file(self.unknown_image_path_file+'/'+file)
                face_encodings =face_recognition.face_encodings(unknown_image , face_locations)
                face_locations= face_recognition.face_locations(unknown_image)
                known_face_encodings = face_recognition.face_encodings(unknown_image,face_locations)
                for(top , right , bottom ,left), face_encoding in zip(face_locations, face_encodings):
                    matches = face_recognition.compare_faces(known_face_encodings , face_encodings)
                    name = "nobody"
                    face_distances = face_recognition.fine_distance(known_face_encodings , face_encoding)
                    best_match_index = np.argmin(face_distances) 
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        return name 
                    return name 
    

earthboxer = FaceRec('./known-people/earthoxer.jpg', './stranger', 'Earthboxer')

