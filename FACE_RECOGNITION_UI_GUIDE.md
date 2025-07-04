# Face Recognition UI - User Guide

## Overview
This is a modern, user-friendly face recognition application with a graphical interface that provides:
- Real-time webcam feed with face detection
- Face dataset collection with a single button
- Automatic training after capturing faces
- Live face recognition with confidence scores
- User management features

## Features

### 1. **Real-time Webcam Feed**
- Shows live video from your webcam
- Automatically detects faces and draws green rectangles around them
- When recognition is enabled, displays the person's name and confidence percentage

### 2. **Face Dataset Collection**
- Enter a person's name in the text field
- Click "Start Capture" button (lower right corner)
- The system will automatically capture 30 images of the face
- Progress bar shows capture progress
- After 30 images, training starts automatically

### 3. **Automatic Training**
- Once face capture is complete, the model trains automatically
- You can also manually trigger training with the "Train Model" button
- Training typically takes a few seconds
- The system will notify you when training is complete

### 4. **Face Recognition**
- Toggle face recognition on/off with the checkbox
- Recognized faces show the person's name and confidence percentage
- Higher confidence means better match (displayed as percentage)

### 5. **User Management**
- View all registered users in the right panel
- Clear all data with the "Clear Dataset" button
- Names are persisted between sessions

## Getting Started

### Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python run_face_recognition.py
   ```
   
   Or directly:
   ```bash
   python face_recognition_ui.py
   ```

### First Time Setup

1. **Launch the application**
2. **Allow camera access** when prompted by your system
3. **Add your first user:**
   - Enter a name in the "Name" field
   - Position your face in front of the camera
   - Click "Start Capture"
   - Keep your face visible while the system captures 30 images
   - Wait for automatic training to complete

### Usage Tips

1. **For Best Results:**
   - Ensure good lighting
   - Face the camera directly
   - Remove glasses if possible during capture
   - Stay still during capture
   - Capture faces in the same conditions where recognition will occur

2. **Adding Multiple Users:**
   - Complete one user's capture and training before adding another
   - Each user needs 30 face samples
   - Use unique names for each person

3. **Recognition Accuracy:**
   - Confidence above 70% is generally a good match
   - Lower confidence may indicate poor lighting or angle
   - The system shows "Unknown" for unrecognized faces

## UI Components

### Main Window
- **Title Bar**: "Face Recognition System"
- **Video Feed**: Center-left, shows webcam stream
- **Status Label**: Below video, shows current system status

### Right Panel
- **User Information**: Name entry field for new users
- **Enable Recognition**: Checkbox to toggle recognition
- **Registered Users**: List of all registered users

### Bottom Controls
- **Progress Bar**: Shows capture progress (0-30 images)
- **Start Capture**: Begin face capture (changes to "Stop Capture" when active)
- **Train Model**: Manually trigger model training
- **Clear Dataset**: Delete all faces and reset the system

## Troubleshooting

### Camera Not Working
- Check if another application is using the camera
- Ensure camera permissions are granted
- Try restarting the application

### Face Not Detected
- Improve lighting conditions
- Face the camera directly
- Move closer to the camera
- Ensure face is fully visible

### Low Recognition Confidence
- Retrain with better quality images
- Ensure consistent lighting between training and recognition
- Add more training samples if needed

### Application Crashes
- Check if all dependencies are installed
- Ensure OpenCV is properly installed with: `pip install opencv-contrib-python`
- Check Python version (3.7+ recommended)

## File Structure

```
/workspace/
├── face_recognition_ui.py    # Main application
├── run_face_recognition.py   # Launcher script
├── requirements.txt          # Dependencies
├── dataset/                  # Captured face images
├── trainer/                  # Trained model files
├── names.txt                # User names database
└── FacialRecognition/       # Original scripts
    ├── haarcascade_frontalface_default.xml
    └── ...
```

## Notes

- The application uses LBPH (Local Binary Patterns Histograms) for face recognition
- Face images are stored in grayscale to reduce file size
- The model file is saved as `trainer/trainer.yml`
- Names are mapped to numeric IDs internally

## Security Considerations

- Face images are stored locally in the `dataset/` folder
- No data is sent to external servers
- Clear dataset feature permanently deletes all face data
- Consider encrypting the dataset folder for sensitive applications