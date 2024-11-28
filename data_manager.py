import os
import json
import cv2
import face_recognition

class DataManager:
    def __init__(self, data_file):
        self.data_file = data_file
        self.data = self.load_data()
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {}

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def resize_and_format_image(self, image, size=(640, 480)):
        resized_image = cv2.resize(image, size)
        return resized_image

    def add_student(self, roll_number, name, image):
        if roll_number in self.data:
            return False
        if not os.path.exists('images'):
            os.makedirs('images')
        img_filename = os.path.join('images', f"{roll_number}_{name}.png")
        
        formatted_image = self.resize_and_format_image(image)
        cv2.imwrite(img_filename, formatted_image)
        
        self.data[roll_number] = {
            'name': name,
            'image_path': img_filename
        }
        self.save_data()
        self.load_known_faces()  
        return True

    def remove_student(self, roll_number):
        if roll_number in self.data:
            image_path = self.data[roll_number]['image_path']
            if os.path.exists(image_path):
                os.remove(image_path)
            del self.data[roll_number]
            self.save_data()
            self.load_known_faces()  
            return True
        return False

    def clear_data(self):
        image_folder = 'images'
        for filename in os.listdir(image_folder):
            file_path = os.path.join(image_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        self.data = {}
        self.save_data()
        self.load_known_faces()

    def get_students(self):
        return self.data

    def load_known_faces(self):
        self.known_face_encodings = []
        self.known_face_names = []
        for roll_number, details in self.data.items():
            image_path = details['image_path']
            if os.path.exists(image_path):
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    self.known_face_encodings.append(encodings[0])
                    self.known_face_names.append(roll_number)
        print("Known face encodings loaded:", self.known_face_encodings)
        print("Known face names loaded:", self.known_face_names)
