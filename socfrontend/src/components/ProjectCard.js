import React, { useState, useEffect } from "react";
import api from '../utils/api';
import { Link } from "react-router-dom";

export default function ProjectCard(props) {
  const [Added, setAdded] = useState(props.isInWishlist);

  // Update state when isInWishlist prop changes
  useEffect(() => {
    setAdded(props.isInWishlist);
  }, [props.isInWishlist]);

  const details = {
    project_id: props.ProjectId,
    title: props.title,
    banner_image: props.link,
    general_category: props.general_category,
  };

    const WishlistAdd = () => {
      // const token = localStorage.getItem('authToken');

      if (!authtoken) {
        console.log("No authentication token found. Please log in.");
        return;
      }
    
      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authtoken}`,
        },
      };
    
      if (!Added) {
        // Add to wishlist
        api
          .post(`${process.env.REACT_APP_BACKEND_URL}/projects/wishlist/`, details, axiosConfig) // Updated URL
          .then((res) => {
            console.log("Added to wishlist:", res.data);
            setAdded(true);
          })
          .catch((err) => {
            if (err.response && err.response.status === 401) {
              console.log("Unauthorized request. Please log in.");
            } else {
              console.log("Error adding to wishlist:", err);
            }
          });
      } else {
        // Remove from wishlist
        api
          .delete(process.env.REACT_APP_BACKEND_URL+`/projects/wishlist?project_id=${props.ProjectId}`, axiosConfig) // Updated URL
          .then((res) => {
            console.log("Removed from wishlist:", res.data);
            setAdded(false);
          })
          .catch((err) => {
            if (err.response && err.response.status === 401) {
              console.log("Unauthorized request. Please log in.");
            } else {
              console.log("Error removing from wishlist:", err);
            }
          });
      }
    };
    

  return (
    <div>
      <article className="overflow-hidden rounded-lg shadow transition hover:shadow-lg">
        <Link to={`/current_projects/${props.ProjectId}`}>
          <img
            alt={props.title}
            src={props.link}
            className="h-56 w-full object-contain"
          />
        </Link>
        <Link to={`/current_projects/${props.ProjectId}`}>
          <div className="bg-white p-4 sm:p-6">
            <h3 className="mt-0.5 text-lg line-clamp-1 text-gray-900">
              {props.title}
            </h3>
          </div>
        </Link>
        <div className="p-4 sm:p-6">
          <button
            onClick={WishlistAdd}
            className={`text-white font-bold ${Added ? "bg-red-600 hover:bg-red-700" : "bg-indigo-600 hover:bg-indigo-700"} py-2 px-4 rounded inline-flex items-center`}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="w-6 h-6 mr-2"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M6.75 7.5l3 2.25-3 2.25m4.5 0h3m-9 8.25h13.5A2.25 2.25 0 0021 18V6a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 6v12a2.25 2.25 0 002.25 2.25Z"
              />
            </svg>
            <p>{Added ? "Remove From Wishlist" : "Add To Wishlist"}</p>
          </button>
        </div>
      </article>
    </div>
  );
}
