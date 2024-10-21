import { useState } from 'react';
import api from "../utils/api";
import { useNavigate, Link } from 'react-router-dom';
import { useEffect } from 'react';



export default function Login() {
    // States for user profile
    const [profile, setProfile] = useState({
        username: '',
        password: '',
    });

    // States for checking the errors
    const [error, setError] = useState(false);
    const [showPassword, setShowPassword] = useState(false); // State to manage password visibility
    const navigate = useNavigate();

    // Handling input change
    const handleProfile = (e) => {
        const { id, value } = e.target;
        setProfile((prevProfile) => ({
            ...prevProfile,
            [id]: value,
        }));
        setError(''); // Reset error message on input change
    };

 

    // Handling form submission
    const handleSubmit = (e) => {
        e.preventDefault();

        // Check for empty fields
        if (!profile.username && !profile.password) {
            setError('Please fill in both Username and Password.');
            return;
        } else if (!profile.username) {
            setError('Please fill in your Username');
            return;
        } else if (!profile.password) {
            setError('Please fill in your Password.');
        }
          else {
            setError("Wrong Username or Password ") 
            return;
        }
        
        const formData = new FormData();
        Object.keys(profile).forEach(key => {
            formData.append(key, profile[key]);
        });

        api.post(process.env.REACT_APP_BACKEND_URL+'/accounts/token/', formData)
            .then(function (response) {
                const token = response.data.access;  // Extract token
                console.log("Login successful, token:", token);

                // Store the token in localStorage
                localStorage.setItem("authToken", token);
                // Redirect to Dashboard and reload the page
                window.location.reload();
                
                
                
            })
            .catch(err => {
                console.log("Login failed:", err);
                setError(true);
                localStorage.removeItem('authToken');
            });
    };

    // Error message display
    // const errorMessage = () => {
    //     return (
    //             <div
    //                 className="error"
    //                 style={{ display: error ? '' : 'none' }}>
    //                 <div role="alert" className="rounded border-s-4 border-red-500 bg-red-50 p-4">
    //                     <div className="flex items-center gap-2 text-red-800">
    //                         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="h-5 w-5">
    //                             <path
    //                                 fillRule="evenodd"
    //                                 d="M9.401 3.003c1.155-2 4.043-2 5.197 0l7.355 12.748c1.154 2-.29 4.5-2.599 4.5H4.645c-2.309 0-3.752-2.5-2.598-4.5L9.4 3.003zM12 8.25a.75.75 0 01.75.75v3.75a.75.75 0 01-1.5 0V9a.75.75 0 01.75-.75zm0 8.25a.75.75 0 100-1.5.75.75 0 000 1.5z"
    //                                 clipRule="evenodd"
    //                             />
    //                         </svg>
    //                         <strong className="block font-medium"> Wrong Username or Password </strong>
    //                     </div>
    //                 </div>
    //             </div>
    //     );
    // };
    const errorMessage = () => {
        return (
            <div className="error" style={{ display: error ? '' : 'none' }}>
                <div role="alert" className="rounded border-s-4 border-red-500 bg-red-50 p-4">
                    <div className="flex items-center gap-2 text-red-800">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="h-5 w-5">
                            <path
                                fillRule="evenodd"
                                d="M9.401 3.003c1.155-2 4.043-2 5.197 0l7.355 12.748c1.154 2-.29 4.5-2.599 4.5H4.645c-2.309 0-3.752-2.5-2.598-4.5L9.4 3.003zM12 8.25a.75.75 0 01.75.75v3.75a.75.75 0 01-1.5 0V9a.75.75 0 01.75-.75zm0 8.25a.75.75 0 100-1.5.75.75 0 000 1.5z"
                                clipRule="evenodd"
                            />
                        </svg>
                        <strong className="block font-medium"> {error} </strong>
                    </div>
                </div>
            </div>
        );
    };
        // Toggle password visibility
        const togglePasswordVisibility = () => {
            setShowPassword((prevState) => !prevState);
        };

    return (
        <div className="form">
            <div className="messages">
                {errorMessage()}
                
            </div>

            <div className="mx-auto max-w-screen-xl px-4 py-16 sm:px-6 lg:px-8">
                <div className="mx-auto max-w-lg">
                    <h1 className="text-center text-2xl font-bold text-indigo-600 sm:text-3xl flex items-center justify-center">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-10 h-10">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M17.25 6.75 22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3-4.5 16.5" />
                        </svg>
                        <span className="mx-3">Seasons of Code</span>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-10 h-10">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M17.25 6.75 22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3-4.5 16.5" />
                        </svg>
                    </h1>

                    <form onSubmit={handleSubmit} className="mb-0 mt-6 space-y-4 rounded-lg p-4 shadow-lg sm:p-6 lg:p-8">
                        <p className="text-center text-lg font-medium">Login to your account</p>

                        <div>
                            <label htmlFor="username">Roll No.</label>
                            <div className="relative">
                                <input
                                    type="text"
                                    id="username"
                                    className="w-full rounded-lg border-gray-200 p-4 pe-12 text-sm shadow-sm"
                                    placeholder="Enter Roll No."
                                    onChange={handleProfile}
                                    
                                />
                            </div>
                        </div>

                        <div>
                            <label htmlFor="password">Password</label>
                            <div className="relative">
                                <input
                                     type={showPassword ? "text" : "password"} // Change input type based on visibility state
                                     id="password"
                                     className="w-full rounded-lg border-gray-200 p-4 pe-12 text-sm shadow-sm"
                                     placeholder="Enter Password"
                                     onChange={handleProfile}
                                     
                                 />
                                 <button
                                     type="button"
                                     className="absolute inset-y-0 right-0 flex items-center pr-3"
                                     onClick={togglePasswordVisibility} // Toggle visibility on click
                                     aria-label="Toggle password visibility"
                                 >
                                     {showPassword ? (
                                         <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                             <path strokeLinecap="round" strokeLinejoin="round" d="M3 12c1.24-2.71 3.12-5 6-5s5.76 2.29 7 5c-1.24 2.71-3.12 5-6 5s-5.76-2.29-7-5z" />
                                             <path strokeLinecap="round" strokeLinejoin="round" d="M15 12c0 1.78-1.5 3-3 3s-3-1.22-3-3" />
                                         </svg>
                                     ) : (
                                         <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                             <path strokeLinecap="round" strokeLinejoin="round" d="M15 12c0 1.78-1.5 3-3 3s-3-1.22-3-3" />
                                             <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c4.418 0 8 3.582 8 8s-3.582 8-8 8a8.001 8.001 0 01-6.69-3.33" />
                                             <path strokeLinecap="round" strokeLinejoin="round" d="M6.34 6.34C5.46 7.27 4.785 8.5 4.337 9.83M12 12c-.22 0-.434-.028-.641-.079M12 12c-.186.051-.395.079-.641.079" />
                                         </svg>
                                     )}
                                 </button>
    
                            </div>
                        </div>

                        <button
                            type="submit"
                            className="block w-full rounded-lg bg-indigo-600 px-5 py-3 text-sm font-medium text-white"
                        >
                            Login
                        </button>

                        <p className="text-center text-sm text-gray-500">
                            No account? <Link className="underline" to="/register">Register Now</Link>
                        </p>
                        <p className="text-center text-sm text-blue-500">
                            <Link className="underline" to="/forget-password">Forget Password?</Link>
                        </p>
                    </form>
                </div>
            </div>
        </div>
    );
}


