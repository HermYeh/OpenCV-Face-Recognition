import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import numpy as np
import threading
import time
from datetime import datetime

class FaceRecognitionApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Face Recognition System")
        self.window.geometry("900x700")
        
        # Set modern dark theme colors
        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.accent_color = "#4CAF50"
        self.button_color = "#2196F3"
        self.danger_color = "#f44336"
        
        self.window.configure(bg=self.bg_color)
        
        # Initialize face detection and recognition
        self.face_cascade = cv2.CascadeClassifier('FacialRecognition/haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # Camera settings
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)  # Width
        self.cap.set(4, 480)  # Height
        
        # State variables
        self.is_capturing = False
        self.current_user_id = None
        self.current_user_name = ""
        self.capture_count = 0
        self.names = ['Unknown']  # Default name for id=0
        self.is_recognizing = True
        self.training_in_progress = False
        
        # Create directories if they don't exist
        os.makedirs('dataset', exist_ok=True)
        os.makedirs('trainer', exist_ok=True)
        
        # Load existing model and names if available
        self.load_model()
        
        # Setup UI
        self.setup_ui()
        
        # Start video loop
        self.update_frame()
        
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.window, bg=self.bg_color)
        title_frame.pack(pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="Face Recognition System",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        title_label.pack()
        
        # Main container
        main_container = tk.Frame(self.window, bg=self.bg_color)
        main_container.pack(expand=True, fill="both", padx=20)
        
        # Left panel - Video feed
        left_panel = tk.Frame(main_container, bg=self.bg_color)
        left_panel.pack(side="left", expand=True, fill="both")
        
        # Video label
        self.video_label = tk.Label(left_panel, bg="#000000")
        self.video_label.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(
            left_panel,
            text="Ready",
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.accent_color
        )
        self.status_label.pack(pady=5)
        
        # Right panel - Controls
        right_panel = tk.Frame(main_container, bg=self.bg_color, width=250)
        right_panel.pack(side="right", fill="y", padx=(20, 0))
        right_panel.pack_propagate(False)
        
        # User info section
        info_frame = tk.LabelFrame(
            right_panel,
            text="User Information",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
            labelanchor="n"
        )
        info_frame.pack(fill="x", pady=10)
        
        # Name entry
        tk.Label(
            info_frame,
            text="Name:",
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(pady=5)
        
        self.name_entry = tk.Entry(
            info_frame,
            font=("Arial", 10),
            bg="#2d2d2d",
            fg=self.fg_color,
            insertbackground=self.fg_color
        )
        self.name_entry.pack(padx=10, pady=5)
        
        # Recognition toggle
        self.recognition_var = tk.BooleanVar(value=True)
        self.recognition_check = tk.Checkbutton(
            right_panel,
            text="Enable Recognition",
            variable=self.recognition_var,
            command=self.toggle_recognition,
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor=self.bg_color,
            activebackground=self.bg_color
        )
        self.recognition_check.pack(pady=10)
        
        # Registered users
        users_frame = tk.LabelFrame(
            right_panel,
            text="Registered Users",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
            labelanchor="n"
        )
        users_frame.pack(fill="both", expand=True, pady=10)
        
        # Users listbox
        self.users_listbox = tk.Listbox(
            users_frame,
            bg="#2d2d2d",
            fg=self.fg_color,
            font=("Arial", 10),
            selectbackground=self.accent_color
        )
        self.users_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Update users list
        self.update_users_list()
        
        # Bottom controls
        bottom_frame = tk.Frame(self.window, bg=self.bg_color)
        bottom_frame.pack(side="bottom", fill="x", pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            bottom_frame,
            length=400,
            mode='determinate',
            maximum=30
        )
        self.progress.pack(pady=10)
        
        # Capture button (positioned at lower right)
        button_container = tk.Frame(bottom_frame, bg=self.bg_color)
        button_container.pack()
        
        self.capture_btn = tk.Button(
            button_container,
            text="Start Capture",
            command=self.toggle_capture,
            font=("Arial", 14, "bold"),
            bg=self.button_color,
            fg=self.fg_color,
            padx=30,
            pady=15,
            relief="flat",
            cursor="hand2"
        )
        self.capture_btn.pack(side="right", padx=10)
        
        # Train button
        self.train_btn = tk.Button(
            button_container,
            text="Train Model",
            command=self.train_model_thread,
            font=("Arial", 14, "bold"),
            bg=self.accent_color,
            fg=self.fg_color,
            padx=30,
            pady=15,
            relief="flat",
            cursor="hand2"
        )
        self.train_btn.pack(side="right", padx=10)
        
        # Clear dataset button
        self.clear_btn = tk.Button(
            button_container,
            text="Clear Dataset",
            command=self.clear_dataset,
            font=("Arial", 14, "bold"),
            bg=self.danger_color,
            fg=self.fg_color,
            padx=20,
            pady=15,
            relief="flat",
            cursor="hand2"
        )
        self.clear_btn.pack(side="right", padx=10)
        
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            # Process each face
            for (x, y, w, h) in faces:
                # Draw rectangle around face
                cv2.rectangle(rgb_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Perform recognition if enabled and model is loaded
                if self.is_recognizing and hasattr(self, 'recognizer'):
                    try:
                        # Check if model exists
                        if os.path.exists('trainer/trainer.yml'):
                            id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])
                            
                            # Determine name and confidence
                            if confidence < 100:
                                name = self.names[id] if id < len(self.names) else "Unknown"
                                conf_text = f"{round(100 - confidence)}%"
                            else:
                                name = "Unknown"
                                conf_text = "0%"
                            
                            # Display name and confidence
                            cv2.putText(rgb_frame, name, (x+5, y-10), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                            cv2.putText(rgb_frame, conf_text, (x+5, y+h+20), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
                    except:
                        pass
                
                # Capture face if in capture mode
                if self.is_capturing and self.capture_count < 30:
                    self.capture_count += 1
                    face_img = gray[y:y+h, x:x+w]
                    filename = f"dataset/User.{self.current_user_id}.{self.capture_count}.jpg"
                    cv2.imwrite(filename, face_img)
                    
                    # Update progress
                    self.progress['value'] = self.capture_count
                    self.status_label.config(
                        text=f"Capturing... {self.capture_count}/30",
                        fg=self.accent_color
                    )
                    
                    # Check if capture is complete
                    if self.capture_count >= 30:
                        self.complete_capture()
            
            # Convert to PhotoImage and display
            img = Image.fromarray(rgb_frame)
            img = img.resize((640, 480), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image=img)
            self.video_label.config(image=photo)
            self.video_label.image = photo
        
        # Schedule next update
        self.window.after(10, self.update_frame)
    
    def toggle_capture(self):
        if not self.is_capturing:
            # Validate name entry
            name = self.name_entry.get().strip()
            if not name:
                messagebox.showwarning("Warning", "Please enter a name!")
                return
            
            # Start capture
            self.current_user_name = name
            self.current_user_id = len(self.names)
            self.names.append(name)
            self.capture_count = 0
            self.is_capturing = True
            
            # Update UI
            self.capture_btn.config(text="Stop Capture", bg=self.danger_color)
            self.name_entry.config(state="disabled")
            self.progress['value'] = 0
            self.status_label.config(text="Look at the camera...", fg=self.accent_color)
        else:
            # Stop capture
            self.stop_capture()
    
    def stop_capture(self):
        self.is_capturing = False
        self.capture_btn.config(text="Start Capture", bg=self.button_color)
        self.name_entry.config(state="normal")
        self.status_label.config(text="Capture stopped", fg=self.danger_color)
        
    def complete_capture(self):
        self.is_capturing = False
        self.capture_btn.config(text="Start Capture", bg=self.button_color)
        self.name_entry.config(state="normal")
        self.name_entry.delete(0, tk.END)
        self.status_label.config(text="Capture complete! Starting training...", fg=self.accent_color)
        
        # Update users list
        self.update_users_list()
        
        # Save names
        self.save_names()
        
        # Automatically start training
        self.window.after(1000, self.train_model_thread)
    
    def train_model_thread(self):
        if self.training_in_progress:
            messagebox.showinfo("Info", "Training already in progress!")
            return
            
        # Check if dataset exists
        if not os.listdir('dataset'):
            messagebox.showwarning("Warning", "No dataset found! Capture some faces first.")
            return
        
        # Start training in a separate thread
        thread = threading.Thread(target=self.train_model)
        thread.daemon = True
        thread.start()
    
    def train_model(self):
        self.training_in_progress = True
        self.status_label.config(text="Training model...", fg=self.accent_color)
        self.train_btn.config(state="disabled")
        
        try:
            # Get images and labels
            faces = []
            ids = []
            
            for filename in os.listdir('dataset'):
                if filename.endswith('.jpg'):
                    path = os.path.join('dataset', filename)
                    # Extract ID from filename
                    id = int(filename.split('.')[1])
                    
                    # Load and process image
                    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    if img is not None:
                        faces.append(img)
                        ids.append(id)
            
            if len(faces) > 0:
                # Train the recognizer
                self.recognizer.train(faces, np.array(ids))
                
                # Save the model
                self.recognizer.write('trainer/trainer.yml')
                
                # Update status
                unique_ids = len(set(ids))
                self.status_label.config(
                    text=f"Training complete! {unique_ids} users trained.",
                    fg=self.accent_color
                )
                messagebox.showinfo("Success", f"Model trained successfully!\n{unique_ids} users registered.")
            else:
                self.status_label.config(text="No faces found in dataset!", fg=self.danger_color)
                
        except Exception as e:
            self.status_label.config(text=f"Training failed: {str(e)}", fg=self.danger_color)
            messagebox.showerror("Error", f"Training failed: {str(e)}")
        finally:
            self.training_in_progress = False
            self.train_btn.config(state="normal")
    
    def toggle_recognition(self):
        self.is_recognizing = self.recognition_var.get()
        status = "enabled" if self.is_recognizing else "disabled"
        self.status_label.config(text=f"Recognition {status}", fg=self.accent_color)
    
    def load_model(self):
        try:
            if os.path.exists('trainer/trainer.yml'):
                self.recognizer.read('trainer/trainer.yml')
                
            # Load saved names
            if os.path.exists('names.txt'):
                with open('names.txt', 'r') as f:
                    self.names = [line.strip() for line in f.readlines()]
                    if not self.names:
                        self.names = ['Unknown']
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def save_names(self):
        with open('names.txt', 'w') as f:
            for name in self.names:
                f.write(f"{name}\n")
    
    def update_users_list(self):
        self.users_listbox.delete(0, tk.END)
        for i, name in enumerate(self.names[1:], 1):  # Skip 'Unknown' at index 0
            self.users_listbox.insert(tk.END, f"{i}. {name}")
    
    def clear_dataset(self):
        result = messagebox.askyesno(
            "Confirm", 
            "This will delete all captured faces and the trained model. Continue?"
        )
        if result:
            # Clear dataset
            for file in os.listdir('dataset'):
                if file.endswith('.jpg'):
                    os.remove(os.path.join('dataset', file))
            
            # Clear model
            if os.path.exists('trainer/trainer.yml'):
                os.remove('trainer/trainer.yml')
            
            # Clear names
            self.names = ['Unknown']
            self.save_names()
            self.update_users_list()
            
            # Reset progress
            self.progress['value'] = 0
            self.status_label.config(text="Dataset cleared", fg=self.accent_color)
            messagebox.showinfo("Success", "Dataset and model cleared successfully!")
    
    def __del__(self):
        if hasattr(self, 'cap'):
            self.cap.release()

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    
    # Handle window close
    def on_closing():
        if hasattr(app, 'cap'):
            app.cap.release()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()