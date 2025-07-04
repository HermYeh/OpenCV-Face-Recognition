import React, { useRef, useCallback, useState } from 'react';
import Webcam from 'react-webcam';
import { Box, Button, Typography, Card, CardContent, CircularProgress, Chip } from '@mui/material';
import Grid2 from '@mui/material/Unstable_Grid2';
import CameraAltIcon from '@mui/icons-material/CameraAlt';
import FaceRetouchingNaturalIcon from '@mui/icons-material/FaceRetouchingNatural';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const FaceDetection: React.FC = () => {
  const webcamRef = useRef<Webcam>(null);
  const [detecting, setDetecting] = useState(false);
  const [detectedImage, setDetectedImage] = useState<string | null>(null);
  const [faceCount, setFaceCount] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const capture = useCallback(async () => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        setDetecting(true);
        setError(null);
        
        try {
          const response = await axios.post(`${API_URL}/detect-face`, {
            image: imageSrc
          });
          
          setDetectedImage(response.data.image);
          setFaceCount(response.data.face_count);
        } catch (err) {
          setError('Failed to detect faces. Please try again.');
          console.error('Detection error:', err);
        } finally {
          setDetecting(false);
        }
      }
    }
  }, [webcamRef]);

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 4, fontWeight: 600 }}>
        Face Detection
      </Typography>
      
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
                onClick={capture}
                disabled={detecting}
                startIcon={detecting ? <CircularProgress size={20} /> : <FaceRetouchingNaturalIcon />}
                sx={{ mt: 3, py: 1.5 }}
              >
                {detecting ? 'Detecting Faces...' : 'Detect Faces'}
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
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <FaceRetouchingNaturalIcon /> Detection Result
                </Typography>
                {faceCount > 0 && (
                  <Chip 
                    label={`${faceCount} ${faceCount === 1 ? 'Face' : 'Faces'} Detected`}
                    color="primary"
                    size="small"
                  />
                )}
              </Box>
              
              <Box sx={{ 
                position: 'relative', 
                borderRadius: 2, 
                overflow: 'hidden',
                background: '#000',
                aspectRatio: '4/3',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                {detectedImage ? (
                  <img 
                    src={detectedImage} 
                    alt="Detected faces" 
                    style={{ 
                      width: '100%', 
                      height: '100%',
                      objectFit: 'cover'
                    }} 
                  />
                ) : (
                  <Typography variant="body1" color="text.secondary">
                    No detection results yet
                  </Typography>
                )}
              </Box>
              
              {error && (
                <Typography color="error" variant="body2" sx={{ mt: 2 }}>
                  {error}
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid2>
      </Grid2>
    </Box>
  );
};

export default FaceDetection;