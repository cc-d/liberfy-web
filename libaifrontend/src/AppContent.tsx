// AppContent.tsx
import React from 'react';
import { useAuth } from './AuthContext';
import LoginPage from './LoginPage';
const AppContent: React.FC = () => {
  const { isLoggedIn, isLoading } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isLoggedIn) {
    return (
        <LoginPage />
    );
  }

  // This is where your main content would go after a user is logged in.
  return <div>Welcome, user!</div>;
};

export default AppContent;
