# Face Recognition Web UI 🎥

A beautiful, modern web-based interface for real-time face detection and recognition using OpenCV and Flask.

![Face Recognition System](https://img.shields.io/badge/OpenCV-4.11.0-blue.svg) ![Flask](https://img.shields.io/badge/Flask-3.1.1-green.svg) ![Python](https://img.shields.io/badge/Python-3.13-yellow.svg)

## 🚀 Features

- **Real-time Face Detection**: Live camera feed with face detection using Haar Cascades
- **Face Recognition**: Identify known faces with confidence scores using LBPH (Local Binary Patterns Histograms)
- **Beautiful Web Interface**: Modern, responsive design with smooth animations
- **Live Statistics**: Real-time system stats and recognition history
- **Interactive Controls**: Easy-to-use camera and detection controls
- **Recognition History**: Track all face recognition events with timestamps
- **Configurable Settings**: Adjust confidence thresholds and toggle features

## 📋 Requirements

- Python 3.8+
- OpenCV 4.x
- Flask 3.x
- NumPy
- Webcam/Camera access

## 🛠️ Installation

### Quick Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd OpenCV-Face-Recognition
```

2. Run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Installation

1. Install Python dependencies:
```bash
pip3 install --break-system-packages flask opencv-python numpy opencv-contrib-python
```

2. Create necessary directories:
```bash
mkdir -p trainer dataset static/css static/js templates
```

## 🎯 Usage

### Starting the Application

1. Start the Flask web server:
```bash
python3 app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

### Using the Interface

#### Camera Controls
- **Start Camera**: Activates your webcam for live video feed
- **Stop Camera**: Deactivates the camera and stops all processing
- **Toggle Detection**: Enable/disable face detection (requires camera to be started)
- **Toggle Recognition**: Enable/disable face recognition (requires trained model)

#### Features Overview

**Video Feed**
- Live camera stream with real-time face detection
- Green rectangles around detected faces
- Name labels and confidence scores for recognized faces
- Recording indicator when camera is active

**System Statistics**
- Number of registered faces in the system
- Recent recognition count
- Real-time camera status

**Recognition History**
- Live feed of face recognition events
- Shows person's name, confidence score, and timestamp
- Automatically scrolls to show recent results

**Settings Panel**
- Auto Recognition: Automatically enable detection and recognition when camera starts
- Show Confidence: Toggle confidence score display
- Confidence Threshold: Adjust recognition sensitivity

## 🔧 Configuration

### Adding New Faces

To add new faces to the recognition system:

1. Use the original training scripts:
```bash
python3 FacialRecognition/01_face_dataset.py    # Capture face images
python3 FacialRecognition/02_face_training.py   # Train the model
```

2. Update the names list in `app.py`:
```python
self.names = ['None', 'Person1', 'Person2', 'Person3', ...]
```

3. Restart the Flask application to load the new model

### Model Training

The system uses LBPH (Local Binary Patterns Histograms) for face recognition:

- **Dataset**: Face images are stored in the `dataset/` directory
- **Training**: The trained model is saved as `trainer/trainer.yml`
- **Recognition**: The model is loaded automatically when the web app starts

## 📁 File Structure

```
OpenCV-Face-Recognition/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── setup.sh                       # Installation script
├── README.md                      # This file
├── templates/
│   └── index.html                 # Web interface template
├── static/
│   ├── css/
│   │   └── style.css              # Styling
│   └── js/
│       └── main.js                # JavaScript functionality
├── FacialRecognition/             # Original OpenCV scripts
│   ├── 01_face_dataset.py
│   ├── 02_face_training.py
│   ├── 03_face_recognition.py
│   └── haarcascade_frontalface_default.xml
├── FaceDetection/                 # Face detection scripts
│   ├── faceDetection.py
│   ├── faceEyeDetection.py
│   └── ...
├── trainer/                       # Trained models
│   └── trainer.yml
└── dataset/                       # Face image dataset
    ├── User.1.1.jpg
    ├── User.1.2.jpg
    └── ...
```

## 🎨 Interface Preview

The web interface features:

- **Modern Design**: Glass-morphism effects with gradient backgrounds
- **Responsive Layout**: Works on desktop, tablet, and mobile devices
- **Smooth Animations**: Engaging transitions and hover effects
- **Live Notifications**: Toast notifications for system events
- **Status Indicators**: Visual feedback for camera, detection, and recognition states

## 🔒 Security Notes

- The application runs on `localhost` by default
- Camera access requires user permission
- No data is stored or transmitted externally
- All processing happens locally on your machine

## 🤝 Contributing

This project is based on the original OpenCV Face Recognition tutorial by Marcelo Rovai. The web interface adds modern usability and visual appeal to the core functionality.

## 📚 References

- [Original Tutorial](https://www.hackster.io/mjrobot/real-time-face-recognition-an-end-to-end-project-a10826)
- [OpenCV Documentation](https://opencv.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🐛 Troubleshooting

### Common Issues

1. **Camera not working**: Check camera permissions and ensure no other application is using the camera
2. **Recognition not working**: Ensure the `trainer/trainer.yml` file exists and contains trained data
3. **Import errors**: Make sure all dependencies are installed correctly

### Getting Help

If you encounter issues:
1. Check the browser console for JavaScript errors
2. Check the Flask application logs in the terminal
3. Verify camera permissions in your browser
4. Ensure all Python dependencies are installed

## 📄 License

This project is based on the original work by Marcelo Rovai and is shared for educational purposes.
