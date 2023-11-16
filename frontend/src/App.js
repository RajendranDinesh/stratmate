import React from 'react';
import { Navigate, BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Cookies from 'js-cookie';

import Login from './user/login';
import SignUp from './user/signup';
import UserDashboard from './user/user';
import Dashboard from './dashboard/dashboard';

function App() {

  const authToken = Cookies.get('authToken');

  return (
    <Router>
      <Routes>
        <Route path="/"  element={<Navigate to="/dashboard" replace={true} />}/>

        {authToken ? (
            <Route path="/dashboard" element={<Dashboard />} />
          ) : (
            <Route path="/dashboard" element={<Navigate to="/login" replace={true} />}/> 
          )}

        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<SignUp />} />
        <Route path="/user/:username" element={<UserDashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
