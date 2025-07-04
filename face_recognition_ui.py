"""
Face Recognition UI Application
Real-time webcam feed with face recognition, dataset collection, and training
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import cv2
import numpy as np
from PIL import Image, ImageTk
import os
import threading
import time
from datetime import datetime

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition System")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        # Initialize variables
        self.video_capture = None
        self.is_running = False
        self.is_collecting_dataset = False
        self.face_cascade = cv2.CascadeClassifier('FacialRecognition/haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.current_user_id = None
        self.dataset_count = 0
        self.names = ['None']  # Default names list
        
        # Load trained model if exists
        self.load_trained_model()
        
        # Setup UI
        self.setup_ui()
        
        # Start video capture
        self.start_video_capture()
    
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="Face Recognition System", 
                              font=('Arial', 24, 'bold'), fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Video frame
        video_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        video_frame.pack(pady=(0, 20))
        
        # Video label
        self.video_label = tk.Label(video_frame, bg='#34495e', width=80, height=25)
        self.video_label.pack(padx=10, pady=10)
        
        # Control frame
        control_frame = tk.Frame(main_frame, bg='#2c3e50')
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Left side controls
        left_controls = tk.Frame(control_frame, bg='#2c3e50')
        left_controls.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Status label
        self.status_label = tk.Label(left_controls, text="Status: Ready", 
                                   font=('Arial', 12), fg='#27ae60', bg='#2c3e50')
        self.status_label.pack(anchor='w')
        
        # Recognition info
        self.recognition_label = tk.Label(left_controls, text="Recognition: Waiting for trained model...", 
                                        font=('Arial', 10), fg='#f39c12', bg='#2c3e50')
        self.recognition_label.pack(anchor='w', pady=(5, 0))
        
        # Right side controls (buttons)
        right_controls = tk.Frame(control_frame, bg='#2c3e50')
        right_controls.pack(side=tk.RIGHT)
        
        # Dataset collection button (positioned in lower right)
        self.collect_button = tk.Button(right_controls, text="Start Dataset Collection", 
                                      command=self.start_dataset_collection,
                                      font=('Arial', 12, 'bold'), bg='#3498db', fg='white',
                                      padx=20, pady=10, relief=tk.RAISED, bd=3)
        self.collect_button.pack(pady=(0, 10))
        
        # Train model button
        self.train_button = tk.Button(right_controls, text="Train Model", 
                                    command=self.train_model,
                                    font=('Arial', 12, 'bold'), bg='#e74c3c', fg='white',
                                    padx=20, pady=10, relief=tk.RAISED, bd=3)
        self.train_button.pack(pady=(0, 10))
        
        # Add user button
        self.add_user_button = tk.Button(right_controls, text="Add User Name", 
                                       command=self.add_user_name,
                                       font=('Arial', 12, 'bold'), bg='#27ae60', fg='white',
                                       padx=20, pady=10, relief=tk.RAISED, bd=3)
        self.add_user_button.pack()
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                          maximum=100, length=300)
        self.progress_bar.pack(pady=(0, 10))
        
        # Progress label
        self.progress_label = tk.Label(main_frame, text="", 
                                     font=('Arial', 10), fg='#ecf0f1', bg='#2c3e50')
        self.progress_label.pack()
    
    def start_video_capture(self):
        """Start video capture from webcam"""
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.is_running = True
        
        # Start video thread
        self.video_thread = threading.Thread(target=self.video_loop)
        self.video_thread.daemon = True
        self.video_thread.start()
    
    def video_loop(self):
        """Main video processing loop"""
        while self.is_running:
            ret, frame = self.video_capture.read()
            if ret:
                frame = cv2.flip(frame, 1)  # Mirror the image
                self.process_frame(frame)
                time.sleep(0.03)  # ~30 FPS
    
    def process_frame(self, frame):
        """Process each frame for face detection and recognition"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # If collecting dataset
            if self.is_collecting_dataset:
                self.save_face_sample(gray[y:y+h, x:x+w])
                cv2.putText(frame, f"Collecting: {self.dataset_count}/30", 
                           (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # If model is trained, perform recognition
            elif hasattr(self, 'model_trained') and self.model_trained:
                try:
                    user_id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])
                    if confidence < 100:
                        name = self.names[user_id] if user_id < len(self.names) else "Unknown"
                        confidence_text = f"{round(100 - confidence)}%"
                    else:
                        name = "Unknown"
                        confidence_text = f"{round(100 - confidence)}%"
                    
                    cv2.putText(frame, f"{name}", (x+5, y-5), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(frame, f"Confidence: {confidence_text}", (x+5, y+h-5), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
                except Exception as e:
                    print(f"Recognition error: {e}")
        
        # Convert frame to PhotoImage and display
        self.display_frame(frame)
    
    def display_frame(self, frame):
        """Display frame in tkinter label"""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        pil_image = Image.fromarray(rgb_frame)
        
        # Resize to fit the label
        pil_image = pil_image.resize((640, 480), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(pil_image)
        
        # Update label
        self.video_label.configure(image=photo)
        self.video_label.image = photo
    
    def start_dataset_collection(self):
        """Start collecting dataset for a new user"""
        if self.is_collecting_dataset:
            messagebox.showwarning("Warning", "Dataset collection already in progress!")
            return
        
        # Get user ID
        user_id = simpledialog.askinteger("User ID", "Enter user ID (positive integer):")
        if user_id is None or user_id <= 0:
            return
        
        self.current_user_id = user_id
        self.dataset_count = 0
        self.is_collecting_dataset = True
        
        # Update UI
        self.collect_button.configure(text="Stop Collection", command=self.stop_dataset_collection)
        self.status_label.configure(text=f"Status: Collecting dataset for User {user_id}")
        self.progress_var.set(0)
        
        # Start collection thread
        collection_thread = threading.Thread(target=self.dataset_collection_loop)
        collection_thread.daemon = True
        collection_thread.start()
    
    def dataset_collection_loop(self):
        """Dataset collection loop"""
        while self.is_collecting_dataset and self.dataset_count < 30:
            time.sleep(0.1)
            # Update progress
            progress = (self.dataset_count / 30) * 100
            self.progress_var.set(progress)
            self.progress_label.configure(text=f"Collected {self.dataset_count}/30 samples")
        
        if self.dataset_count >= 30:
            self.stop_dataset_collection()
            self.root.after(100, self.auto_train_model)
    
    def save_face_sample(self, face_roi):
        """Save a face sample to dataset"""
        if self.dataset_count < 30:
            filename = f"dataset/User.{self.current_user_id}.{self.dataset_count + 1}.jpg"
            cv2.imwrite(filename, face_roi)
            self.dataset_count += 1
    
    def stop_dataset_collection(self):
        """Stop dataset collection"""
        self.is_collecting_dataset = False
        self.collect_button.configure(text="Start Dataset Collection", command=self.start_dataset_collection)
        self.status_label.configure(text="Status: Dataset collection completed")
        self.progress_var.set(100)
        self.progress_label.configure(text=f"Collection completed: {self.dataset_count} samples")
    
    def auto_train_model(self):
        """Automatically start training after dataset collection"""
        if messagebox.askyesno("Auto Training", "Dataset collection completed! Start training automatically?"):
            self.train_model()
    
    def train_model(self):
        """Train the face recognition model"""
        if not os.path.exists('dataset') or not os.listdir('dataset'):
            messagebox.showerror("Error", "No dataset found! Please collect dataset first.")
            return
        
        self.status_label.configure(text="Status: Training model...")
        self.progress_var.set(0)
        self.progress_label.configure(text="Training in progress...")
        
        # Start training thread
        training_thread = threading.Thread(target=self.train_model_thread)
        training_thread.daemon = True
        training_thread.start()
    
    def train_model_thread(self):
        """Training thread"""
        try:
            # Get images and labels
            face_samples = []
            ids = []
            
            image_paths = [os.path.join('dataset', f) for f in os.listdir('dataset')]
            
            for image_path in image_paths:
                self.progress_var.set((len(face_samples) / len(image_paths)) * 50)
                
                pil_img = Image.open(image_path).convert('L')
                img_numpy = np.array(pil_img, 'uint8')
                
                user_id = int(os.path.split(image_path)[-1].split(".")[1])
                faces = self.face_cascade.detectMultiScale(img_numpy)
                
                for (x, y, w, h) in faces:
                    face_samples.append(img_numpy[y:y+h, x:x+w])
                    ids.append(user_id)
            
            # Train recognizer
            self.progress_var.set(75)
            self.recognizer.train(face_samples, np.array(ids))
            
            # Save model
            self.recognizer.write('trainer/trainer.yml')
            self.model_trained = True
            
            # Update UI
            self.progress_var.set(100)
            self.status_label.configure(text="Status: Model trained successfully")
            self.progress_label.configure(text=f"Training completed: {len(np.unique(ids))} users trained")
            self.recognition_label.configure(text="Recognition: Active", fg='#27ae60')
            
            messagebox.showinfo("Success", f"Training completed!\n{len(np.unique(ids))} users trained successfully.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Training failed: {str(e)}")
            self.status_label.configure(text="Status: Training failed")
    
    def load_trained_model(self):
        """Load pre-trained model if exists"""
        if os.path.exists('trainer/trainer.yml'):
            try:
                self.recognizer.read('trainer/trainer.yml')
                self.model_trained = True
                self.recognition_label.configure(text="Recognition: Active", fg='#27ae60')
            except:
                self.model_trained = False
        else:
            self.model_trained = False
    
    def add_user_name(self):
        """Add a user name to the names list"""
        user_id = simpledialog.askinteger("User ID", "Enter user ID:")
        if user_id is None or user_id <= 0:
            return
        
        name = simpledialog.askstring("User Name", f"Enter name for User {user_id}:")
        if name:
            # Extend names list if necessary
            while len(self.names) <= user_id:
                self.names.append("Unknown")
            
            self.names[user_id] = name
            messagebox.showinfo("Success", f"Name '{name}' added for User {user_id}")
    
    def on_closing(self):
        """Handle window closing"""
        self.is_running = False
        if self.video_capture:
            self.video_capture.release()
        cv2.destroyAllWindows()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()