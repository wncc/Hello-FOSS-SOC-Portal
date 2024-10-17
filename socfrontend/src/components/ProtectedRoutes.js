import React from 'react';
import { Outlet, Navigate } from 'react-router-dom'


const ProtectedRoutes = () => {
    const authToken = localStorage.getItem('authToken');
    console.log("authToken:", authToken);
    if (authToken) {
        return <Outlet/>
    } else {
        return <Navigate to="/login" />
    }
};

export default ProtectedRoutes;