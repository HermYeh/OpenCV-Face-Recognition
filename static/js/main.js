// Face Recognition System JavaScript
class FaceRecognitionUI {
    constructor() {
        this.isRecognitionActive = false;
        this.isDetectionActive = false;
        this.isCameraActive = false;
        this.recognitionResults = [];
        this.statsUpdateInterval = null;
        this.resultsUpdateInterval = null;
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateSystemStats();
        this.startPeriodicUpdates();
        this.updateThresholdDisplay();
    }

    bindEvents() {
        // Camera controls
        document.getElementById('start-camera').addEventListener('click', () => this.startCamera());
        document.getElementById('stop-camera').addEventListener('click', () => this.stopCamera());
        
        // Detection and recognition toggles
        document.getElementById('toggle-detection').addEventListener('click', () => this.toggleDetection());
        document.getElementById('toggle-recognition').addEventListener('click', () => this.toggleRecognition());
        
        // Settings
        document.getElementById('confidence-threshold').addEventListener('input', (e) => {
            this.updateThresholdDisplay();
        });
        
        document.getElementById('auto-recognition').addEventListener('change', (e) => {
            if (e.target.checked && this.isCameraActive) {
                this.enableDetection();
                this.enableRecognition();
            }
        });
        
        document.getElementById('show-confidence').addEventListener('change', (e) => {
            // This could be used to show/hide confidence in the UI
            console.log('Show confidence toggled:', e.target.checked);
        });
    }

    async startCamera() {
        try {
            const response = await fetch('/camera/start');
            const result = await response.json();
            
            if (response.ok) {
                this.isCameraActive = true;
                this.updateCameraStatus();
                this.showNotification('Camera started successfully', 'success');
                
                // Show the video feed
                const videoFeed = document.getElementById('video-feed');
                videoFeed.src = '/video_feed?' + new Date().getTime();
                
                // Show recording indicator
                document.getElementById('recording-indicator').style.display = 'flex';
            } else {
                this.showNotification('Failed to start camera', 'error');
            }
        } catch (error) {
            console.error('Error starting camera:', error);
            this.showNotification('Error starting camera', 'error');
        }
    }

    async stopCamera() {
        try {
            const response = await fetch('/camera/stop');
            const result = await response.json();
            
            if (response.ok) {
                this.isCameraActive = false;
                this.isDetectionActive = false;
                this.isRecognitionActive = false;
                this.updateCameraStatus();
                this.updateDetectionStatus();
                this.updateRecognitionStatus();
                this.showNotification('Camera stopped', 'info');
                
                // Hide recording indicator
                document.getElementById('recording-indicator').style.display = 'none';
            } else {
                this.showNotification('Failed to stop camera', 'error');
            }
        } catch (error) {
            console.error('Error stopping camera:', error);
            this.showNotification('Error stopping camera', 'error');
        }
    }

    async toggleDetection() {
        if (!this.isCameraActive) {
            this.showNotification('Please start the camera first', 'warning');
            return;
        }

        try {
            const response = await fetch('/detection/toggle');
            const result = await response.json();
            
            if (response.ok) {
                this.isDetectionActive = result.status;
                this.updateDetectionStatus();
                this.showNotification(
                    `Detection ${this.isDetectionActive ? 'enabled' : 'disabled'}`, 
                    'success'
                );
            } else {
                this.showNotification('Failed to toggle detection', 'error');
            }
        } catch (error) {
            console.error('Error toggling detection:', error);
            this.showNotification('Error toggling detection', 'error');
        }
    }

    async toggleRecognition() {
        if (!this.isCameraActive) {
            this.showNotification('Please start the camera first', 'warning');
            return;
        }

        try {
            const response = await fetch('/recognition/toggle');
            const result = await response.json();
            
            if (response.ok) {
                this.isRecognitionActive = result.status;
                this.updateRecognitionStatus();
                this.showNotification(
                    `Recognition ${this.isRecognitionActive ? 'enabled' : 'disabled'}`, 
                    'success'
                );
            } else {
                this.showNotification('Failed to toggle recognition', 'error');
            }
        } catch (error) {
            console.error('Error toggling recognition:', error);
            this.showNotification('Error toggling recognition', 'error');
        }
    }

    async updateSystemStats() {
        try {
            const response = await fetch('/system_stats');
            const stats = await response.json();
            
            if (response.ok) {
                document.getElementById('total-faces').textContent = stats.total_faces;
                document.getElementById('recent-recognitions').textContent = stats.recent_recognitions;
                document.getElementById('camera-active').textContent = stats.camera_active ? 'Active' : 'Inactive';
                
                // Update internal state
                this.isCameraActive = stats.camera_active;
                this.isDetectionActive = stats.detection_enabled;
                this.isRecognitionActive = stats.recognition_enabled;
                
                // Update UI status
                this.updateCameraStatus();
                this.updateDetectionStatus();
                this.updateRecognitionStatus();
            }
        } catch (error) {
            console.error('Error fetching system stats:', error);
        }
    }

    async updateRecognitionResults() {
        try {
            const response = await fetch('/recognition_results');
            const results = await response.json();
            
            if (response.ok && JSON.stringify(results) !== JSON.stringify(this.recognitionResults)) {
                this.recognitionResults = results;
                this.displayRecognitionResults();
            }
        } catch (error) {
            console.error('Error fetching recognition results:', error);
        }
    }

    displayRecognitionResults() {
        const resultsContainer = document.getElementById('recognition-results');
        
        if (this.recognitionResults.length === 0) {
            resultsContainer.innerHTML = '<div class="no-results">No recognitions yet</div>';
            return;
        }

        resultsContainer.innerHTML = this.recognitionResults
            .slice(-10) // Show last 10 results
            .reverse()  // Show most recent first
            .map(result => `
                <div class="recognition-item">
                    <div class="recognition-name">${result.name}</div>
                    <div class="recognition-confidence">Confidence: ${result.confidence}</div>
                    <div class="recognition-time">${result.timestamp}</div>
                </div>
            `).join('');
    }

    updateCameraStatus() {
        const cameraIcon = document.getElementById('camera-icon');
        const cameraStatus = document.getElementById('camera-status');
        const statusItem = cameraIcon.parentElement;
        
        if (this.isCameraActive) {
            cameraStatus.textContent = 'Camera On';
            statusItem.classList.add('active');
        } else {
            cameraStatus.textContent = 'Camera Off';
            statusItem.classList.remove('active');
        }
    }

    updateDetectionStatus() {
        const detectionIcon = document.getElementById('detection-icon');
        const detectionStatus = document.getElementById('detection-status');
        const statusItem = detectionIcon.parentElement;
        
        if (this.isDetectionActive) {
            detectionStatus.textContent = 'Detection On';
            statusItem.classList.add('active');
        } else {
            detectionStatus.textContent = 'Detection Off';
            statusItem.classList.remove('active');
        }
    }

    updateRecognitionStatus() {
        const recognitionIcon = document.getElementById('recognition-icon');
        const recognitionStatus = document.getElementById('recognition-status');
        const statusItem = recognitionIcon.parentElement;
        
        if (this.isRecognitionActive) {
            recognitionStatus.textContent = 'Recognition On';
            statusItem.classList.add('active');
        } else {
            recognitionStatus.textContent = 'Recognition Off';
            statusItem.classList.remove('active');
        }
    }

    updateThresholdDisplay() {
        const slider = document.getElementById('confidence-threshold');
        const display = document.getElementById('threshold-value');
        display.textContent = slider.value;
    }

    showNotification(message, type) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '15px 20px',
            borderRadius: '10px',
            color: 'white',
            fontWeight: '600',
            zIndex: '1000',
            transform: 'translateX(100%)',
            transition: 'transform 0.3s ease',
            boxShadow: '0 4px 15px rgba(0, 0, 0, 0.2)'
        });
        
        // Set background color based on type
        switch (type) {
            case 'success':
                notification.style.background = 'linear-gradient(135deg, #48bb78, #38a169)';
                break;
            case 'error':
                notification.style.background = 'linear-gradient(135deg, #e53e3e, #c53030)';
                break;
            case 'warning':
                notification.style.background = 'linear-gradient(135deg, #ed8936, #dd6b20)';
                break;
            case 'info':
                notification.style.background = 'linear-gradient(135deg, #3182ce, #2b77cb)';
                break;
        }
        
        // Add to DOM
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    startPeriodicUpdates() {
        // Update stats every 2 seconds
        this.statsUpdateInterval = setInterval(() => {
            this.updateSystemStats();
        }, 2000);
        
        // Update recognition results every 1 second
        this.resultsUpdateInterval = setInterval(() => {
            this.updateRecognitionResults();
        }, 1000);
    }

    stopPeriodicUpdates() {
        if (this.statsUpdateInterval) {
            clearInterval(this.statsUpdateInterval);
        }
        if (this.resultsUpdateInterval) {
            clearInterval(this.resultsUpdateInterval);
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FaceRecognitionUI();
});

// Clean up intervals when page is unloaded
window.addEventListener('beforeunload', () => {
    if (window.faceRecognitionUI) {
        window.faceRecognitionUI.stopPeriodicUpdates();
    }
});