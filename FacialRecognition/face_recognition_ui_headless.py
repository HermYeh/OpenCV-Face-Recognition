'''
Headless Face Recognition Application
Command-line interface for face recognition and training
'''

import cv2
import numpy as np
import os
import time
import threading
import argparse

# Fix locale issues
os.environ['LC_ALL'] = 'C'
os.environ['LANG'] = 'C'

class HeadlessFaceRecognition:
    def __init__(self):
        self.camera = None
        self.is_capturing = False
        self.is_training = False
        self.recognizer = None
        self.face_cascade = None
        self.names = []
        self.current_user_id = 1
        self.capture_count = 0
        self.max_captures = 30
        
        # Create directories if they don't exist
        self.create_directories()
        
        # Initialize face recognition components
        self.initialize_face_recognition()
        
        # Start camera
        self.start_camera()
    
    def create_directories(self):
        """Create necessary directories"""
        directories = ['dataset', 'trainer']
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created {directory} directory")
    
    def initialize_face_recognition(self):
        """Initialize face recognition components"""
        try:
            # Load face detector
            cascade_path = "haarcascade_frontalface_default.xml"
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            
            if self.face_cascade.empty():
                print("Error: Could not load face detector cascade file.")
                return
            
            # Load recognizer if trainer exists
            if os.path.exists('trainer/trainer.yml'):
                try:
                    self.recognizer = cv2.face.LBPHFaceRecognizer_create()
                    self.recognizer.read('trainer/trainer.yml')
                    print("Loaded existing trainer model")
                except AttributeError:
                    print("Warning: OpenCV face recognition module not available. Install opencv-contrib-python")
                except Exception as e:
                    print(f"Error loading trainer: {e}")
            else:
                print("No trainer model found. Will create new one after training.")
                
        except Exception as e:
            print(f"Error: Failed to initialize face recognition: {e}")
    
    def start_camera(self):
        """Start the camera"""
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                self.camera = cv2.VideoCapture(1)
                if not self.camera.isOpened():
                    print("Error: Could not open camera")
                    return
            
            self.camera.set(3, 1280)  # set video width - increased for better quality
            self.camera.set(4, 720)   # set video height - increased for better quality
            print("Camera started successfully")
            
        except Exception as e:
            print(f"Error: Failed to start camera: {e}")
    
    def capture_faces(self, user_id):
        """Capture faces for training"""
        if self.camera is None:
            print("Error: Camera not available")
            return False
        
        self.current_user_id = user_id
        self.capture_count = 0
        self.is_capturing = True
        
        print(f"Starting face capture for User {user_id}")
        print("Look at the camera. Press Ctrl+C to stop early.")
        
        try:
            while self.capture_count < self.max_captures:
                ret, frame = self.camera.read()
                if not ret:
                    print("Error: Could not read frame from camera.")
                    break
                
                # Flip frame vertically
                frame = cv2.flip(frame, -1)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces
                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=5,
                    minSize=(30, 30)
                )
                
                for (x, y, w, h) in faces:
                    # Save face image
                    filename = f"dataset/User.{user_id}.{self.capture_count + 1}.jpg"
                    cv2.imwrite(filename, gray[y:y+h, x:x+w])
                    
                    self.capture_count += 1
                    print(f"Captured face {self.capture_count}/{self.max_captures}")
                    
                    if self.capture_count >= self.max_captures:
                        break
                
                # Small delay to avoid overwhelming the system
                time.sleep(0.5)
            
            self.is_capturing = False
            print(f"Capture complete! Captured {self.capture_count} faces for User {user_id}")
            return True
            
        except KeyboardInterrupt:
            print("\nCapture interrupted by user")
            self.is_capturing = False
            return False
        except Exception as e:
            print(f"Error during capture: {e}")
            self.is_capturing = False
            return False
    
    def train_model(self):
        """Train the face recognition model"""
        if self.is_training:
            print("Training already in progress...")
            return False
        
        self.is_training = True
        print("Starting model training...")
        
        try:
            # Get images and labels
            path = 'dataset'
            image_paths = [os.path.join(path, f) for f in os.listdir(path)]
            face_samples = []
            ids = []
            
            print(f"Found {len(image_paths)} images for training")
            
            for image_path in image_paths:
                try:
                    # Load image
                    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                    if img is None:
                        continue
                    
                    # Get user ID from filename
                    filename = os.path.basename(image_path)
                    user_id = int(filename.split('.')[1])
                    
                    face_samples.append(img)
                    ids.append(user_id)
                    
                except Exception as e:
                    print(f"Error processing {image_path}: {e}")
                    continue
            
            if len(face_samples) == 0:
                print("Error: No valid face images found for training")
                self.is_training = False
                return False
            
            # Create and train recognizer
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.train(face_samples, np.array(ids))
            
            # Save model
            recognizer.write('trainer/trainer.yml')
            
            print(f"Training complete! {len(face_samples)} faces from {len(set(ids))} users")
            
            # Refresh recognizer
            self.refresh_model()
            
            self.is_training = False
            return True
            
        except Exception as e:
            print(f"Training error: {e}")
            self.is_training = False
            return False
    
    def refresh_model(self):
        """Refresh the face recognition model"""
        try:
            if os.path.exists('trainer/trainer.yml'):
                self.recognizer = cv2.face.LBPHFaceRecognizer_create()
                self.recognizer.read('trainer/trainer.yml')
                print("Model refreshed successfully")
            else:
                print("No model to refresh")
        except Exception as e:
            print(f"Error refreshing model: {e}")
    
    def recognize_faces(self, duration=30):
        """Run face recognition for specified duration"""
        if self.camera is None:
            print("Error: Camera not available")
            return
        
        if self.recognizer is None:
            print("Error: No trained model available")
            return
        
        print(f"Starting face recognition for {duration} seconds...")
        print("Press Ctrl+C to stop early.")
        
        start_time = time.time()
        
        try:
           while True:
                ret, frame = self.camera.read()
                if not ret:
                    print("Error: Could not read frame from camera.")
                    break
                
                # Flip frame vertically
                frame = cv2.flip(frame, -1)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces
                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=5,
                    minSize=(30, 30)
                )
                
                for (x, y, w, h) in faces:
                    try:
                        face_roi = gray[y:y+h, x:x+w]
                        id, confidence = self.recognizer.predict(face_roi)
                        
                        if confidence < 100:
                            name = self.names[id] if id < len(self.names) else f"User_{id}"
                            confidence_text = f"{round(100 - confidence)}%"
                        else:
                            name = "Unknown"
                            confidence_text = f"{round(100 - confidence)}%"
                        
                        print(f"Detected: {name} (confidence: {confidence_text})")
                        
                    except Exception as e:
                        print(f"Recognition error: {e}")
                
                
                
        except KeyboardInterrupt:
            print("\nRecognition stopped by user")
        except Exception as e:
            print(f"Error during recognition: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        if self.camera is not None:
            self.camera.release()
        print("Cleanup complete")

def main():
    parser = argparse.ArgumentParser(description='Headless Face Recognition System')
    parser.add_argument('--capture', type=int, help='Capture faces for user ID')
    parser.add_argument('--train', action='store_true', help='Train the model')
    parser.add_argument('--recognize', type=int, default=30, help='Run recognition for N seconds')
    parser.add_argument('--refresh', action='store_true', help='Refresh the model')
    
    args = parser.parse_args()
    
    app = HeadlessFaceRecognition()
    
    try:
        if args.capture:
            app.capture_faces(args.capture)
        
        if args.train:
            app.train_model()
        
        if args.refresh:
            app.refresh_model()
        
        if args.recognize:
            app.recognize_faces(args.recognize)
        
        # If no arguments, show interactive menu
        if not any([args.capture, args.train, args.recognize, args.refresh]):
            while True:
                print("\n=== Face Recognition System ===")
                print("1. Capture faces for training")
                print("2. Train model")
                print("3. Run face recognition")
                print("4. Refresh model")
                print("5. Exit")
                
                choice = input("\nEnter your choice (1-5): ")
                
                if choice == '1':
                    user_id = input("Enter user ID: ")
                    try:
                        app.capture_faces(int(user_id))
                    except ValueError:
                        print("Invalid user ID")
                
                elif choice == '2':
                    app.train_model()
                
                elif choice == '3':
                    duration = input("Enter recognition duration in seconds (default 30): ")
                    try:
                        app.recognize_faces(int(duration) if duration else 30)
                    except ValueError:
                        print("Invalid duration")
                
                elif choice == '4':
                    app.refresh_model()
                
                elif choice == '5':
                    break
                
                else:
                    print("Invalid choice")
    
    except KeyboardInterrupt:
        print("\nExiting...")
    
    finally:
        app.cleanup()

if __name__ == "__main__":
    main() 