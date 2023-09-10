// AppContent.tsx
import React from 'react';
import { useAuth } from './AuthContext';
import LoginPage from './Pages/LoginPage';
const AppContent: React.FC = () => {
  const { user, userLoading } = useAuth();

  if (userLoading) {
    return <div>Loading...</div>;
  }

  if (!user && !userLoading) {
    return (
        <LoginPage />
    );
  }

  // This is where your main content would go after a user is logged in.
  return (
    <>
      <h1>Logged in as {user?.email}</h1>
    </>
  )

};

export default AppContent;
