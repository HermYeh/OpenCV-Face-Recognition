import React, { useState, useEffect } from 'react';
import { 
  Box, Typography, Card, CardContent, Table, TableBody, TableCell, 
  TableContainer, TableHead, TableRow, IconButton, Button, 
  CircularProgress, Alert, Chip, Paper
} from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import PersonIcon from '@mui/icons-material/Person';
import GroupIcon from '@mui/icons-material/Group';
import ModelTrainingIcon from '@mui/icons-material/ModelTraining';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

interface User {
  id: number;
  name: string;
  imageCount: number;
}

const UserManagement: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [training, setTraining] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const fetchUsers = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.get(`${API_URL}/users`);
      setUsers(response.data.users);
    } catch (err) {
      setError('Failed to fetch users. Please try again.');
      console.error('Fetch users error:', err);
    } finally {
      setLoading(false);
    }
  };

  const trainModel = async () => {
    setTraining(true);
    setError(null);
    setSuccess(null);
    
    try {
      const response = await axios.post(`${API_URL}/train-model`);
      setSuccess(response.data.message);
    } catch (err) {
      setError('Failed to train model. Please try again.');
      console.error('Training error:', err);
    } finally {
      setTraining(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const totalImages = users.reduce((sum, user) => sum + user.imageCount, 0);

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 600 }}>
          User Management
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={fetchUsers}
            disabled={loading}
          >
            Refresh
          </Button>
          <Button
            variant="contained"
            startIcon={training ? <CircularProgress size={20} /> : <ModelTrainingIcon />}
            onClick={trainModel}
            disabled={training || users.length === 0}
          >
            {training ? 'Training...' : 'Train Model'}
          </Button>
        </Box>
      </Box>

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

      <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 3, mb: 4 }}>
        <Card sx={{ 
          background: 'rgba(255, 255, 255, 0.05)', 
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.1)'
        }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <GroupIcon sx={{ fontSize: 40, color: 'primary.main' }} />
              <Box>
                <Typography variant="h3" sx={{ fontWeight: 700 }}>
                  {users.length}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Registered Users
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ 
          background: 'rgba(255, 255, 255, 0.05)', 
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.1)'
        }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <PersonIcon sx={{ fontSize: 40, color: 'secondary.main' }} />
              <Box>
                <Typography variant="h3" sx={{ fontWeight: 700 }}>
                  {totalImages}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Total Face Images
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </Box>

      <TableContainer 
        component={Paper} 
        sx={{ 
          background: 'rgba(255, 255, 255, 0.05)', 
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.1)'
        }}
      >
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>User ID</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>Face Images</TableCell>
              <TableCell>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={4} align="center">
                  <CircularProgress />
                </TableCell>
              </TableRow>
            ) : users.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} align="center">
                  <Typography color="text.secondary">
                    No users registered yet
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              users.map((user) => (
                <TableRow key={user.id}>
                  <TableCell>{user.id}</TableCell>
                  <TableCell>{user.name}</TableCell>
                  <TableCell>{user.imageCount}</TableCell>
                  <TableCell>
                    <Chip 
                      label="Active" 
                      color="success" 
                      size="small" 
                      variant="outlined"
                    />
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default UserManagement;