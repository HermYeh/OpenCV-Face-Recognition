# Face Recognition Web UI

A modern, beautiful web interface for real-time face detection and recognition using React and Flask.

![Face Recognition UI](https://img.shields.io/badge/React-18.2.0-blue.svg) ![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg) ![Material-UI](https://img.shields.io/badge/Material--UI-5.x-purple.svg)

## 🌟 Features

- **Real-time Face Detection**: Detect faces in real-time using your webcam
- **Face Recognition**: Identify registered users with confidence scores
- **User Registration**: Easy multi-step process to register new users
- **User Management**: View and manage all registered users
- **Beautiful Dark UI**: Modern, responsive design with Material-UI
- **Live Camera Feed**: Direct webcam integration for all features

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Node.js 14+
- npm or yarn
- Webcam access

### Installation & Running

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Navigate to the web-ui directory**:
   ```bash
   cd web-ui
   ```

3. **Run the application**:
   ```bash
   ./start.sh
   ```

   This will automatically:
   - Set up Python virtual environment
   - Install backend dependencies
   - Install frontend dependencies
   - Start both backend and frontend servers

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## 📋 Manual Setup (Alternative)

### Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## 🎯 How to Use

### 1. Face Detection
- Navigate to the "Face Detection" tab
- Allow camera access when prompted
- Click "Detect Faces" to see real-time face detection
- Green boxes will appear around detected faces

### 2. User Registration
- Go to the "Register User" tab
- Follow the 3-step process:
  1. Enter a unique User ID and Name
  2. Capture at least 5 photos from different angles
  3. Train the model with the captured images

### 3. Face Recognition
- Switch to the "Face Recognition" tab
- Click "Recognize Face" to identify registered users
- The system will show names and confidence scores

### 4. User Management
- View all registered users in the "Manage Users" tab
- See total users and face images
- Retrain the model when needed

## 🏗️ Architecture

### Frontend (React + TypeScript)
- **Material-UI**: For beautiful, responsive components
- **react-webcam**: For camera integration
- **axios**: For API communication

### Backend (Flask + OpenCV)
- **Flask**: REST API server
- **OpenCV**: Face detection and recognition
- **LBPH**: Face recognition algorithm

## 📁 Project Structure

```
web-ui/
├── frontend/                # React frontend application
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── FaceDetection.tsx
│   │   │   ├── FaceRecognition.tsx
│   │   │   ├── UserRegistration.tsx
│   │   │   └── UserManagement.tsx
│   │   └── App.tsx         # Main application
│   └── package.json
├── backend/                # Flask backend API
│   ├── app.py             # API endpoints
│   └── requirements.txt   # Python dependencies
├── start.sh               # Startup script
└── README.md             # This file
```

## 🔧 API Endpoints

- `GET /api/health` - Health check
- `POST /api/detect-face` - Detect faces in image
- `POST /api/create-dataset` - Create face dataset for user
- `POST /api/train-model` - Train recognition model
- `POST /api/recognize-face` - Recognize faces in image
- `GET /api/users` - Get all registered users

## 🎨 UI Features

- Dark theme with gradient backgrounds
- Glassmorphism effects
- Smooth animations and transitions
- Responsive design for all screen sizes
- Real-time feedback and loading states
- Error handling with user-friendly messages

## 🛠️ Troubleshooting

### Camera Access Issues
- Ensure your browser has camera permissions
- Check if another application is using the camera
- Try refreshing the page

### Backend Connection Issues
- Verify the backend is running on port 5000
- Check for any firewall blocking
- Ensure all Python dependencies are installed

### Model Training Issues
- Ensure you have captured enough images (minimum 5)
- Make sure faces are clearly visible in captured images
- Check that the dataset directory has write permissions

## 📝 Notes

- The face recognition model uses LBPH (Local Binary Patterns Histograms)
- Better recognition accuracy with more training images
- Optimal lighting conditions improve detection/recognition
- The system stores face data locally in the backend directory

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

This project is part of the OpenCV Face Recognition tutorial series.