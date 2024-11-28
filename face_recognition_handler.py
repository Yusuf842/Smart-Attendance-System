import face_recognition
import numpy as np

class FaceRecognitionHandler:
    def __init__(self, known_face_encodings, known_face_names):
        self.known_face_encodings = known_face_encodings
        self.known_face_names = known_face_names

    def recognize_faces(self, rgb_frame):
        if not self.known_face_encodings:
            print("No known face encodings available.")
            return []

        try:
            rgb_frame = np.ascontiguousarray(rgb_frame)

            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            print("Face locations:", face_locations)
            print("Face encodings:", face_encodings)

            recognized_faces = []
            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                print("Matches:", matches)
                if True in matches:
                    first_match_index = matches.index(True)
                    roll_number = self.known_face_names[first_match_index]
                    recognized_faces.append((roll_number, face_location))
            return recognized_faces
        except Exception as e:
            print(f"Error in face recognition: {str(e)}")
            return []
