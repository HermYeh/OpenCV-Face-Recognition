import cv2
import os
import numpy as np
from PIL import Image, ImageTk
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox

# Paths & initial setup
CASCADE_PATH = os.path.join('FacialRecognition', 'haarcascade_frontalface_default.xml')
DATASET_DIR = 'dataset'
TRAINER_DIR = 'trainer'
TRAINER_FILE = os.path.join(TRAINER_DIR, 'trainer.yml')

os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(TRAINER_DIR, exist_ok=True)

# Load cascade for face detection
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

# Global recognizer instance (lazy loaded)
recognizer = None
if os.path.exists(TRAINER_FILE):
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(TRAINER_FILE)
    except Exception as e:
        print('[WARN] Could not load trained model:', e)
        recognizer = None

# Camera setup
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

minW = 0.1 * cam.get(cv2.CAP_PROP_FRAME_WIDTH)
minH = 0.1 * cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

# Capture state
capture_flag = False
capture_id = None
capture_count = 0
CAPTURE_TARGET = 30  # number of images per person

# Tkinter UI
root = tk.Tk()
root.title('Real-Time Face Recognition')

video_label = tk.Label(root)
video_label.pack()

# Bottom-right button frame
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)

def ask_and_start_capture():
    global capture_flag, capture_id, capture_count
    if capture_flag:
        return  # ignore if already capturing
    user_input = simpledialog.askstring('Input', 'Enter numeric user ID:', parent=root)
    if user_input and user_input.isdigit():
        capture_id = int(user_input)
        capture_flag = True
        capture_count = 0
        messagebox.showinfo('Capture', f'Starting capture for user {capture_id}. Look at the camera…')
    else:
        messagebox.showwarning('Invalid input', 'Please enter a numeric user ID.')

def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith('.jpg')]
    face_samples = []
    ids = []
    for image_path in image_paths:
        pil_img = Image.open(image_path).convert('L')
        img_numpy = np.array(pil_img, 'uint8')
        # Filename pattern: User.<id>.<imagenum>.jpg
        try:
            id_ = int(os.path.split(image_path)[-1].split('.')[1])
        except (IndexError, ValueError):
            continue
        faces = face_cascade.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            face_samples.append(img_numpy[y:y + h, x:x + w])
            ids.append(id_)
    return face_samples, ids

def train_recognizer_async():
    # Run training in a background thread to avoid blocking UI
    threading.Thread(target=_train_recognizer, daemon=True).start()

def _train_recognizer():
    global recognizer
    faces, ids = get_images_and_labels(DATASET_DIR)
    if len(ids) == 0:
        print('[INFO] No faces found for training.')
        return
    print('[INFO] Training faces…')
    new_recognizer = cv2.face.LBPHFaceRecognizer_create()
    new_recognizer.train(faces, np.array(ids))
    new_recognizer.write(TRAINER_FILE)
    recognizer = new_recognizer
    print(f'[INFO] Training complete. {len(np.unique(ids))} unique faces.')
    messagebox.showinfo('Training', 'Training completed successfully.')

def draw_frame():
    global capture_flag, capture_count
    ret, frame = cam.read()
    if not ret:
        root.after(10, draw_frame)
        return
    frame = cv2.flip(frame, 1)  # mirror
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH))
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Recognition (if model is loaded)
        label_text = 'Unknown'
        if recognizer is not None:
            id_pred, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            if confidence < 100:
                label_text = f'ID {id_pred} ({round(100 - confidence)}%)'
            else:
                label_text = f'Unknown ({round(100 - confidence)}%)'
        cv2.putText(frame, label_text, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Handle dataset capture
        if capture_flag and capture_count < CAPTURE_TARGET:
            img_path = os.path.join(DATASET_DIR, f'User.{capture_id}.{capture_count + 1}.jpg')
            cv2.imwrite(img_path, gray[y:y + h, x:x + w])
            capture_count += 1
            cv2.putText(frame, f'Capturing {capture_count}/{CAPTURE_TARGET}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            if capture_count >= CAPTURE_TARGET:
                capture_flag = False
                messagebox.showinfo('Capture', 'Capture complete. Starting training…')
                train_recognizer_async()

    # Convert BGR to RGB for Tkinter
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb_frame)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk  # type: ignore  # keep reference
    video_label.configure(image=imgtk)

    root.after(10, draw_frame)

# UI Button
capture_button = tk.Button(button_frame, text='Capture Face', command=ask_and_start_capture)
capture_button.pack(side=tk.RIGHT)

# Start the video loop
root.after(0, draw_frame)
root.protocol('WM_DELETE_WINDOW', lambda: (cam.release(), root.destroy()))
root.mainloop()