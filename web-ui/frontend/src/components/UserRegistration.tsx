import React, { useRef, useState } from 'react';
import Webcam from 'react-webcam';
import { 
  Box, Button, Typography, Card, CardContent, TextField, 
  Stepper, Step, StepLabel, Alert, LinearProgress, Chip, CircularProgress
} from '@mui/material';
import Grid2 from '@mui/material/Unstable_Grid2';
import CameraAltIcon from '@mui/icons-material/CameraAlt';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import ModelTrainingIcon from '@mui/icons-material/ModelTraining';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const steps = ['Enter Details', 'Capture Photos', 'Train Model'];

const UserRegistration: React.FC = () => {
  const webcamRef = useRef<Webcam>(null);
  const [activeStep, setActiveStep] = useState(0);
  const [userId, setUserId] = useState('');
  const [userName, setUserName] = useState('');
  const [capturedImages, setCapturedImages] = useState<string[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const captureImage = () => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        setCapturedImages([...capturedImages, imageSrc]);
      }
    }
  };

  const handleNext = async () => {
    setError(null);
    setSuccess(null);

    if (activeStep === 0) {
      // Validate user details
      if (!userId || !userName) {
        setError('Please enter both User ID and Name');
        return;
      }
      setActiveStep(1);
    } else if (activeStep === 1) {
      // Create dataset
      if (capturedImages.length < 5) {
        setError('Please capture at least 5 photos');
        return;
      }
      
      setIsProcessing(true);
      try {
        const response = await axios.post(`${API_URL}/create-dataset`, {
          userId,
          userName,
          images: capturedImages
        });
        
        setSuccess(response.data.message);
        setActiveStep(2);
      } catch (err) {
        setError('Failed to create dataset. Please try again.');
        console.error('Dataset creation error:', err);
      } finally {
        setIsProcessing(false);
      }
    } else if (activeStep === 2) {
      // Train model
      setIsProcessing(true);
      try {
        const response = await axios.post(`${API_URL}/train-model`);
        setSuccess(response.data.message);
        
        // Reset after successful training
        setTimeout(() => {
          setActiveStep(0);
          setUserId('');
          setUserName('');
          setCapturedImages([]);
          setSuccess(null);
        }, 3000);
      } catch (err) {
        setError('Failed to train model. Please try again.');
        console.error('Training error:', err);
      } finally {
        setIsProcessing(false);
      }
    }
  };

  const handleReset = () => {
    setActiveStep(0);
    setUserId('');
    setUserName('');
    setCapturedImages([]);
    setError(null);
    setSuccess(null);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 4, fontWeight: 600 }}>
        User Registration
      </Typography>

      <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 3 }} onClose={() => setSuccess(null)}>
          {success}
        </Alert>
      )}

      {activeStep === 0 && (
        <Card sx={{ 
          background: 'rgba(255, 255, 255, 0.05)', 
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          maxWidth: 600,
          mx: 'auto'
        }}>
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <PersonAddIcon /> User Details
            </Typography>
            
            <TextField
              fullWidth
              label="User ID"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              margin="normal"
              variant="outlined"
              helperText="Enter a unique numeric ID"
              type="number"
            />
            
            <TextField
              fullWidth
              label="User Name"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              margin="normal"
              variant="outlined"
              helperText="Enter the person's name"
            />
            
            <Button
              variant="contained"
              fullWidth
              size="large"
              onClick={handleNext}
              sx={{ mt: 3 }}
              disabled={!userId || !userName}
            >
              Next: Capture Photos
            </Button>
          </CardContent>
        </Card>
      )}

      {activeStep === 1 && (
        <Grid2 container spacing={4}>
          <Grid2 size={{ xs: 12, md: 6 }}>
            <Card sx={{ 
              background: 'rgba(255, 255, 255, 0.05)', 
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(255, 255, 255, 0.1)'
            }}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <CameraAltIcon /> Capture Photos
                </Typography>
                
                <Box sx={{ 
                  position: 'relative', 
                  borderRadius: 2, 
                  overflow: 'hidden',
                  background: '#000',
                  aspectRatio: '4/3'
                }}>
                  <Webcam
                    ref={webcamRef}
                    audio={false}
                    screenshotFormat="image/jpeg"
                    style={{
                      width: '100%',
                      height: '100%',
                      objectFit: 'cover'
                    }}
                  />
                </Box>
                
                <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
                  <Button
                    variant="contained"
                    fullWidth
                    onClick={captureImage}
                    startIcon={<CameraAltIcon />}
                  >
                    Capture Photo
                  </Button>
                  <Button
                    variant="outlined"
                    onClick={handleReset}
                  >
                    Reset
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid2>
          
          <Grid2 size={{ xs: 12, md: 6 }}>
            <Card sx={{ 
              background: 'rgba(255, 255, 255, 0.05)', 
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(255, 255, 255, 0.1)'
            }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">Captured Photos</Typography>
                  <Chip 
                    label={`${capturedImages.length} / 30 photos`}
                    color={capturedImages.length >= 5 ? 'success' : 'default'}
                    size="small"
                  />
                </Box>
                
                <Box sx={{ 
                  display: 'grid', 
                  gridTemplateColumns: 'repeat(auto-fill, minmax(80px, 1fr))',
                  gap: 1,
                  mb: 2
                }}>
                  {capturedImages.map((img, index) => (
                    <Box
                      key={index}
                      sx={{
                        borderRadius: 1,
                        overflow: 'hidden',
                        aspectRatio: '1',
                        background: '#000'
                      }}
                    >
                      <img 
                        src={img} 
                        alt={`Capture ${index + 1}`}
                        style={{ 
                          width: '100%', 
                          height: '100%',
                          objectFit: 'cover'
                        }}
                      />
                    </Box>
                  ))}
                </Box>
                
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Capture at least 5 photos from different angles for better recognition accuracy.
                </Typography>
                
                <Button
                  variant="contained"
                  fullWidth
                  size="large"
                  onClick={handleNext}
                  disabled={capturedImages.length < 5 || isProcessing}
                  startIcon={isProcessing ? <CircularProgress size={20} /> : <CheckCircleIcon />}
                  sx={{ mt: 2 }}
                >
                  {isProcessing ? 'Creating Dataset...' : 'Create Dataset'}
                </Button>
              </CardContent>
            </Card>
          </Grid2>
        </Grid2>
      )}

      {activeStep === 2 && (
        <Card sx={{ 
          background: 'rgba(255, 255, 255, 0.05)', 
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          maxWidth: 600,
          mx: 'auto'
        }}>
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <ModelTrainingIcon /> Train Model
            </Typography>
            
            <Typography variant="body1" color="text.secondary" gutterBottom>
              The face recognition model needs to be trained with the captured images.
              This process may take a few moments.
            </Typography>
            
            {isProcessing && (
              <Box sx={{ mt: 3, mb: 2 }}>
                <LinearProgress />
                <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                  Training model with face data...
                </Typography>
              </Box>
            )}
            
            <Button
              variant="contained"
              fullWidth
              size="large"
              onClick={handleNext}
              disabled={isProcessing}
              startIcon={isProcessing ? <CircularProgress size={20} /> : <ModelTrainingIcon />}
              sx={{ mt: 3 }}
            >
              {isProcessing ? 'Training in Progress...' : 'Train Model'}
            </Button>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default UserRegistration;