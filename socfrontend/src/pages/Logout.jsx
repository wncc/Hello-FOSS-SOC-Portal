import React, { useEffect } from 'react'
import api from "../utils/api";
import { useNavigate } from 'react-router-dom';

function Logout() {
    const navigate = useNavigate();
    useEffect(() => {
        api.get(process.env.REACT_APP_BACKEND_URL+"/accounts/logout/")
            .then((res) => {
                console.log(res.data);
                window.location.reload();
                localStorage.removeItem('authToken');
                navigate('/login')
                
            })
            .catch(err => {
                console.log(err);
                window.location.reload();
                localStorage.removeItem('authToken');
                navigate('/login')
              
            })
    }, [])




  return (
    <div>Logout</div>
  )
}

export default Logout