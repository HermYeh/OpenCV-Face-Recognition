import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Container, AppBar, Toolbar, Typography, Tab, Tabs, Box, Paper } from '@mui/material';
import FaceIcon from '@mui/icons-material/Face';
import CameraEnhanceIcon from '@mui/icons-material/CameraEnhance';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import GroupIcon from '@mui/icons-material/Group';
import FaceDetection from './components/FaceDetection';
import FaceRecognition from './components/FaceRecognition';
import UserRegistration from './components/UserRegistration';
import UserManagement from './components/UserManagement';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#2196f3',
    },
    secondary: {
      main: '#ff4081',
    },
    background: {
      default: '#0a0e27',
      paper: '#151b3b',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h3: {
      fontWeight: 700,
    },
  },
  shape: {
    borderRadius: 12,
  },
});

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`tabpanel-${index}`}
      aria-labelledby={`tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

function App() {
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1, minHeight: '100vh', background: 'linear-gradient(135deg, #0a0e27 0%, #151b3b 100%)' }}>
        <AppBar position="static" elevation={0} sx={{ background: 'rgba(21, 27, 59, 0.8)', backdropFilter: 'blur(10px)' }}>
          <Toolbar>
            <FaceIcon sx={{ mr: 2, fontSize: 32 }} />
            <Typography variant="h5" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
              Face Recognition System
            </Typography>
          </Toolbar>
        </AppBar>
        
        <Container maxWidth="lg" sx={{ mt: 4 }}>
          <Paper 
            elevation={3} 
            sx={{ 
              background: 'rgba(21, 27, 59, 0.6)', 
              backdropFilter: 'blur(20px)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              overflow: 'hidden'
            }}
          >
            <Tabs 
              value={tabValue} 
              onChange={handleTabChange} 
              variant="fullWidth"
              sx={{
                borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
                '& .MuiTab-root': {
                  minHeight: 64,
                  textTransform: 'none',
                  fontSize: '1rem',
                  fontWeight: 500,
                }
              }}
            >
              <Tab icon={<CameraEnhanceIcon />} label="Face Detection" />
              <Tab icon={<FaceIcon />} label="Face Recognition" />
              <Tab icon={<PersonAddIcon />} label="Register User" />
              <Tab icon={<GroupIcon />} label="Manage Users" />
            </Tabs>
            
            <TabPanel value={tabValue} index={0}>
              <FaceDetection />
            </TabPanel>
            <TabPanel value={tabValue} index={1}>
              <FaceRecognition />
            </TabPanel>
            <TabPanel value={tabValue} index={2}>
              <UserRegistration />
            </TabPanel>
            <TabPanel value={tabValue} index={3}>
              <UserManagement />
            </TabPanel>
          </Paper>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;
