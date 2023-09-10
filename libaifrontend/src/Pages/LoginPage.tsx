// src/LoginPage.tsx

import React, { useState } from 'react';
import { redirect } from 'react-router-dom';
import apiois from '../apios';  // Assuming you have apiois set up at this path
import {
  TextField,
  Button,
  Container,
  Grid,
  Typography,
} from '@mui/material';
import { UserOutToken } from '../api';

const LoginPage: React.FC = () => {
  const [loginData, setLoginData] = useState({ username: '', password: '' });
  const [registerData, setRegisterData] = useState({ email: '', password: '' });

  const handleLoginChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setLoginData((prev) => ({ ...prev, [name]: value }));
  };

  const handleRegisterChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setRegisterData((prev) => ({ ...prev, [name]: value }));
  };

  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await apiois.post('/user/tokenlogin', {
        grant_type: 'password',
        username: loginData.username,
        password: loginData.password,
      });
      const token = response.data.access_token;
      localStorage.setItem('jwt_token', token);
      redirect('/');  // Redirect to the home page
    } catch (error: any) {
      console.error("Error logging in:", error.response.data);
    }
  };

  const handleRegisterSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const resp = await apiois.post('/user/create', registerData);
      if (resp.status == 201 || resp.status == 200) {
        const userWithToken = resp.data as UserOutToken;
        localStorage.setItem('jwt_token', userWithToken.token.access_token);
        redirect('/');  // Redirect to the home page
      }
    } catch (error: any) {
      console.error("Error registering:", error.response.data);
    }
  };

  return (
    <Container>
      <Grid container spacing={3}>
        <Grid item xs={6}>
          <Typography variant="h4">Login</Typography>
          <form onSubmit={handleLoginSubmit}>
            <TextField
              fullWidth
              margin="normal"
              label="Username"
              variant="outlined"
              name="username"
              value={loginData.username}
              onChange={handleLoginChange}
            />
            <TextField
              fullWidth
              margin="normal"
              label="Password"
              variant="outlined"
              type="password"
              name="password"
              value={loginData.password}
              onChange={handleLoginChange}
            />
            <Button variant="contained" color="primary" type="submit">
              Login
            </Button>
          </form>
        </Grid>
        <Grid item xs={6}>
          <Typography variant="h4">Register</Typography>
          <form onSubmit={handleRegisterSubmit}>
            <TextField
              fullWidth
              margin="normal"
              label="Email"
              variant="outlined"
              name="email"
              value={registerData.email}
              onChange={handleRegisterChange}
            />
            <TextField
              fullWidth
              margin="normal"
              label="Password"
              variant="outlined"
              type="password"
              name="password"
              value={registerData.password}
              onChange={handleRegisterChange}
            />
            <Button variant="contained" color="primary" type="submit">
              Register
            </Button>
          </form>
        </Grid>
      </Grid>
    </Container>
  );
};

export default LoginPage;
