import React from 'react';
import { Outlet, Navigate } from 'react-router-dom';

const LoginRoute = () => {
    const Token = localStorage.getItem('authToken');

    console.log("authToken:", Token);

    // While waiting for authToken to be determined (i.e., null), don't render anything.
    if (Token === null) {
        return <Outlet />; // Or a loading spinner if necessary
    }

    // If the user is not authenticated, show the child routes (login, register).
    if (!Token) {
        return <Outlet />;
    }

    // If the user is authenticated, redirect them to the home page.
    return <Navigate to="/" />;
};

export default LoginRoute;
