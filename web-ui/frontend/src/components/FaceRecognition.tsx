import React, { useRef, useCallback, useState } from 'react';
import Webcam from 'react-webcam';
import { Box, Button, Typography, Card, CardContent, CircularProgress, Chip, Alert } from '@mui/material';
import Grid2 from '@mui/material/Unstable_Grid2';
import CameraAltIcon from '@mui/icons-material/CameraAlt';
import PersonSearchIcon from '@mui/icons-material/PersonSearch';
import VerifiedUserIcon from '@mui/icons-material/VerifiedUser';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

interface RecognizedFace {
  name: string;
  confidence: number;
  userId: number | null;
  box: {
    x: number;
    y: number;
    width: number;
    height: number;
  };
}

const FaceRecognition: React.FC = () => {
  const webcamRef = useRef<Webcam>(null);
  const [recognizing, setRecognizing] = useState(false);
  const [recognizedImage, setRecognizedImage] = useState<string | null>(null);
  const [recognizedFaces, setRecognizedFaces] = useState<RecognizedFace[]>([]);
  const [error, setError] = useState<string | null>(null);

  const recognize = useCallback(async () => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        setRecognizing(true);
        setError(null);
        
        try {
          const response = await axios.post(`${API_URL}/recognize-face`, {
            image: imageSrc
          });
          
          setRecognizedImage(response.data.image);
          setRecognizedFaces(response.data.faces);
        } catch (err: any) {
          if (err.response?.status === 500 && err.response?.data?.error?.includes('trainer.yml')) {
            setError('No trained model found. Please register and train users first.');
          } else {
            setError('Failed to recognize faces. Please try again.');
          }
          console.error('Recognition error:', err);
        } finally {
          setRecognizing(false);
        }
      }
    }
  }, [webcamRef]);

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 4, fontWeight: 600 }}>
        Face Recognition
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}
      
      <Grid2 container spacing={4}>
        <Grid2 size={{ xs: 12, md: 6 }}>
          <Card sx={{ 
            background: 'rgba(255, 255, 255, 0.05)', 
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.1)'
          }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <CameraAltIcon /> Live Camera
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
              <Button
                variant="contained"
                fullWidth
                size="large"
                onClick={recognize}
                disabled={recognizing}
                startIcon={recognizing ? <CircularProgress size={20} /> : <PersonSearchIcon />}
                sx={{ mt: 3, py: 1.5 }}
              >
                {recognizing ? 'Recognizing...' : 'Recognize Face'}
              </Button>
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
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <PersonSearchIcon /> Recognition Result
              </Typography>
              
              <Box sx={{ 
                position: 'relative', 
                borderRadius: 2, 
                overflow: 'hidden',
                background: '#000',
                aspectRatio: '4/3',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                mb: 2
              }}>
                {recognizedImage ? (
                  <img 
                    src={recognizedImage} 
                    alt="Recognized faces" 
                    style={{ 
                      width: '100%', 
                      height: '100%',
                      objectFit: 'cover'
                    }} 
                  />
                ) : (
                  <Typography variant="body1" color="text.secondary">
                    No recognition results yet
                  </Typography>
                )}
              </Box>
              
              {recognizedFaces.length > 0 && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle2" gutterBottom color="text.secondary">
                    Recognized People:
                  </Typography>
                  {recognizedFaces.map((face, index) => (
                    <Box key={index} sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                      {face.name !== 'Unknown' && <VerifiedUserIcon color="success" fontSize="small" />}
                      <Chip
                        label={face.name}
                        color={face.name !== 'Unknown' ? 'success' : 'default'}
                        size="small"
                        variant={face.name !== 'Unknown' ? 'filled' : 'outlined'}
                      />
                      {face.confidence > 0 && (
                        <Typography variant="caption" color="text.secondary">
                          {face.confidence}% confidence
                        </Typography>
                      )}
                    </Box>
                  ))}
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid2>
      </Grid2>
    </Box>
  );
};

export default FaceRecognition;