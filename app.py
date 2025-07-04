from flask import Flask, render_template, Response, request, jsonify
import cv2
import numpy as np
import os
import json
from datetime import datetime
import base64

app = Flask(__name__)

class FaceRecognitionSystem:
    def __init__(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.cascade_path = "FacialRecognition/haarcascade_frontalface_default.xml"
        self.face_cascade = cv2.CascadeClassifier(self.cascade_path)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.names = ['None', 'Marcelo', 'Paula', 'Ilza', 'Z', 'W']
        self.camera = None
        self.detection_enabled = False
        self.recognition_enabled = False
        self.recognition_results = []
        
        # Load trained model if it exists
        if os.path.exists('trainer/trainer.yml'):
            self.recognizer.read('trainer/trainer.yml')
            self.recognition_enabled = True
    
    def start_camera(self):
        if self.camera is None:
            self.camera = cv2.VideoCapture(0)
            self.camera.set(3, 640)
            self.camera.set(4, 480)
    
    def stop_camera(self):
        if self.camera is not None:
            self.camera.release()
            self.camera = None
    
    def process_frame(self):
        if self.camera is None:
            return None
        
        ret, frame = self.camera.read()
        if not ret:
            return None
            
        frame = cv2.flip(frame, -1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if self.detection_enabled:
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                if self.recognition_enabled:
                    id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])
                    
                    if confidence < 100:
                        name = self.names[id] if id < len(self.names) else "Unknown"
                        confidence_text = f"{round(100 - confidence)}%"
                    else:
                        name = "Unknown"
                        confidence_text = f"{round(100 - confidence)}%"
                    
                    cv2.putText(frame, name, (x+5, y-5), self.font, 1, (255, 255, 255), 2)
                    cv2.putText(frame, confidence_text, (x+5, y+h-5), self.font, 1, (255, 255, 0), 1)
                    
                    # Store recognition result
                    self.recognition_results.append({
                        'name': name,
                        'confidence': confidence_text,
                        'timestamp': datetime.now().strftime('%H:%M:%S')
                    })
                    
                    # Keep only last 10 results
                    if len(self.recognition_results) > 10:
                        self.recognition_results.pop(0)
        
        return frame

face_system = FaceRecognitionSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera/start')
def start_camera():
    face_system.start_camera()
    return jsonify({'status': 'Camera started'})

@app.route('/camera/stop')
def stop_camera():
    face_system.stop_camera()
    return jsonify({'status': 'Camera stopped'})

@app.route('/detection/toggle')
def toggle_detection():
    face_system.detection_enabled = not face_system.detection_enabled
    return jsonify({'status': face_system.detection_enabled})

@app.route('/recognition/toggle')
def toggle_recognition():
    face_system.recognition_enabled = not face_system.recognition_enabled
    return jsonify({'status': face_system.recognition_enabled})

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            frame = face_system.process_frame()
            if frame is not None:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/recognition_results')
def get_recognition_results():
    return jsonify(face_system.recognition_results)

@app.route('/system_stats')
def get_system_stats():
    return jsonify({
        'detection_enabled': face_system.detection_enabled,
        'recognition_enabled': face_system.recognition_enabled,
        'camera_active': face_system.camera is not None,
        'total_faces': len(face_system.names) - 1,
        'recent_recognitions': len(face_system.recognition_results)
    })

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('trainer', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)