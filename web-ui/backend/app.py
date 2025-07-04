from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import cv2
import numpy as np
import base64
import io
from PIL import Image
import os
import sys

# Add parent directories to path to import face recognition modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../../FacialRecognition'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../FaceDetection'))

app = Flask(__name__)
CORS(app)

# Initialize face cascade
face_cascade = cv2.CascadeClassifier('../../FacialRecognition/haarcascade_frontalface_default.xml')

# Create directory for dataset if it doesn't exist
DATASET_DIR = '../../FacialRecognition/dataset'
TRAINER_DIR = '../../FacialRecognition/trainer'
os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(TRAINER_DIR, exist_ok=True)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/api/detect-face', methods=['POST'])
def detect_face():
    try:
        data = request.json
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        # Convert to OpenCV format
        image = Image.open(io.BytesIO(image_bytes))
        image_np = np.array(image)
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Draw rectangles and prepare response
        result_image = image_np.copy()
        face_coords = []
        
        for (x, y, w, h) in faces:
            cv2.rectangle(result_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            face_coords.append({'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)})
        
        # Convert result back to base64
        result_pil = Image.fromarray(result_image)
        buffered = io.BytesIO()
        result_pil.save(buffered, format="PNG")
        result_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'faces': face_coords,
            'image': f'data:image/png;base64,{result_base64}',
            'face_count': len(faces)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/create-dataset', methods=['POST'])
def create_dataset():
    try:
        data = request.json
        user_id = data['userId']
        user_name = data['userName']
        images = data['images']
        
        # Create user directory
        user_dir = os.path.join(DATASET_DIR, f'User.{user_id}.{user_name}')
        os.makedirs(user_dir, exist_ok=True)
        
        count = 0
        for idx, image_data in enumerate(images):
            try:
                # Decode image
                image_bytes = base64.b64decode(image_data.split(',')[1])
                image = Image.open(io.BytesIO(image_bytes))
                image_np = np.array(image)
                gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
                
                # Detect face
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                
                for (x, y, w, h) in faces:
                    count += 1
                    # Save face image
                    face_img = gray[y:y+h, x:x+w]
                    cv2.imwrite(f'{user_dir}/User.{user_id}.{count}.jpg', face_img)
                    
            except Exception as e:
                print(f"Error processing image {idx}: {e}")
                continue
        
        return jsonify({
            'success': True,
            'message': f'Dataset created with {count} face images',
            'userId': user_id,
            'userName': user_name
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/train-model', methods=['POST'])
def train_model():
    try:
        import cv2
        from PIL import Image
        import numpy as np
        
        # Get all user faces and labels
        faces = []
        labels = []
        
        for user_folder in os.listdir(DATASET_DIR):
            if user_folder.startswith('User.'):
                user_id = int(user_folder.split('.')[1])
                user_path = os.path.join(DATASET_DIR, user_folder)
                
                for image_name in os.listdir(user_path):
                    if image_name.endswith('.jpg'):
                        image_path = os.path.join(user_path, image_name)
                        pil_image = Image.open(image_path).convert('L')
                        image_np = np.array(pil_image, 'uint8')
                        faces.append(image_np)
                        labels.append(user_id)
        
        # Train recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(faces, np.array(labels))
        
        # Save trained model
        recognizer.save(os.path.join(TRAINER_DIR, 'trainer.yml'))
        
        return jsonify({
            'success': True,
            'message': f'Model trained with {len(faces)} face samples',
            'users': len(set(labels))
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/recognize-face', methods=['POST'])
def recognize_face():
    try:
        data = request.json
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        # Load trained model
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(os.path.join(TRAINER_DIR, 'trainer.yml'))
        
        # Get user names mapping
        user_names = {}
        for user_folder in os.listdir(DATASET_DIR):
            if user_folder.startswith('User.'):
                parts = user_folder.split('.')
                user_id = int(parts[1])
                user_name = parts[2] if len(parts) > 2 else 'Unknown'
                user_names[user_id] = user_name
        
        # Convert to OpenCV format
        image = Image.open(io.BytesIO(image_bytes))
        image_np = np.array(image)
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Recognize faces
        result_image = image_np.copy()
        recognized_faces = []
        
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            
            # Predict
            user_id, confidence = recognizer.predict(roi_gray)
            
            # Draw rectangle and label
            cv2.rectangle(result_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            if confidence < 100:
                name = user_names.get(user_id, f'User {user_id}')
                confidence_percent = round(100 - confidence)
            else:
                name = "Unknown"
                confidence_percent = 0
            
            cv2.putText(result_image, f'{name} ({confidence_percent}%)', 
                       (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            recognized_faces.append({
                'name': name,
                'confidence': confidence_percent,
                'userId': user_id if confidence < 100 else None,
                'box': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)}
            })
        
        # Convert result back to base64
        result_pil = Image.fromarray(result_image)
        buffered = io.BytesIO()
        result_pil.save(buffered, format="PNG")
        result_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'faces': recognized_faces,
            'image': f'data:image/png;base64,{result_base64}'
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = []
        for user_folder in os.listdir(DATASET_DIR):
            if user_folder.startswith('User.'):
                parts = user_folder.split('.')
                user_id = int(parts[1])
                user_name = parts[2] if len(parts) > 2 else 'Unknown'
                
                # Count images
                user_path = os.path.join(DATASET_DIR, user_folder)
                image_count = len([f for f in os.listdir(user_path) if f.endswith('.jpg')])
                
                users.append({
                    'id': user_id,
                    'name': user_name,
                    'imageCount': image_count
                })
        
        return jsonify({'success': True, 'users': users}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)