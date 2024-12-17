import ProjectCard from "../components/ProjectCard"
import api from '../utils/api';
import "../components/Filter.css"
import { useEffect } from "react";
import { useState } from "react";
import { useMemo } from "react";
import "../components/ProjectCard.css";
import {Outlet} from 'react-router-dom'

export default function Projects() {

  const [details, setDetails] = useState([]);
  const [wishlist, setWishlist] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Make an HTTP request to fetch the card image from the backend
    api.get(process.env.REACT_APP_BACKEND_URL+'/projects/')
      .then((response) => {
        // Assuming the response contains the image URL
        console.log(response.data);
        setDetails(response.data);
      })
      .catch((error) => {
        console.error('Error fetching card image:', error);
      });
  }, []);

  useEffect(() => {
    // Make an HTTP request to fetch the card image from the backend
    api.get(process.env.REACT_APP_BACKEND_URL+'/projects/wishlist/')
      .then((response) => {
        // Assuming the response contains the image URL
        console.log(response.data);
        setWishlist(response.data);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching card image:', error);
        setIsLoading(false);
      });
  }, []);

  // const filteredDetails = details.filter(
  //   (detail) => !wishlist.some((item) => item.id === detail.id)
  // );
  // console.log(filteredDetails);

//   const details = [
//     {
//       "id": 1,
//       "title": "Speech emotion recognition",
//       "general_category": "ML",
//       "banner_image": "http://127.0.0.1:8000/media/projects/emotion_detection.png"
//   },
//   {
//       "id": 2,
//       "title": "Test Project",
//       "general_category": "Development",
//       "banner_image": "http://127.0.0.1:8000/media/projects/For_his_participation_in_the_5-day_Grand_Entrepreneur_Workshop_held_by_Liceria__Co..png"
//     },
//     {
//       "id": 3,
//       "title": "Speech emotion recognition",
//       "general_category": "Blockchain",
//       "banner_image": "http://127.0.0.1:8000/media/projects/emotion_detection.png"
//   },
//   {
//       "id": 4,
//       "title": "Test Project",
//       "general_category": "CP",
//       "banner_image": "http://127.0.0.1:8000/media/projects/For_his_participation_in_the_5-day_Grand_Entrepreneur_Workshop_held_by_Liceria__Co..png"
//     },
//   {
//       "id": 5,
//       "title": "Test Project",
//       "general_category": "Others",
//       "banner_image": "http://127.0.0.1:8000/media/projects/For_his_participation_in_the_5-day_Grand_Entrepreneur_Workshop_held_by_Liceria__Co..png"
//     }
//   ]

// GeneralCategoryChoices = (
//   ('ML', 'ML'),
//   ('Developement', 'Development'),
//   ('Blockchain', 'Blockchain'),
//   ('CP', 'CP'),
//   ('Others', 'Others'),
//     )


  
  const [filterValue, setFilterValue] = useState('All');

  const filteredProjects = useMemo(() => {
    return details.filter(project => project.general_category.includes(filterValue) || filterValue==="All");
  }, [details, filterValue]);

  const handleFilterChange = (value) => {
    setFilterValue(value);
  };

  const [active, setActive] = useState('b1');


  return (
  
  <section className="project-card min-h-[calc(100vh-72px)] dark:bg-gray-800 dark:text-white " >

    <div className="pt-8 flex items-center justify-center ">
      <div className="inline-flex sm:flex-wrap rounded-md shadow-sm" role="group">
        <button type="button" onClick={() => {handleFilterChange('All'); setActive('b1')}} className={`w-40 px-4 py-2 text-sm font-medium ${active==='b1' ? 'text-white' :'text-gray-900'} ${active==='b1' ? 'bg-indigo-600' : 'bg-white dark:bg-slate-400'} border border-gray-500 rounded-s-lg hover:bg-indigo-600 hover:text-white focus:z-10 focus:ring-2  `}>
          ALL
        </button>
        <button type="button" onClick={() => {handleFilterChange('ML'); setActive('b2')}} className={`w-40 px-4 py-2 text-sm font-medium ${active==='b2' ? 'text-white' :'text-gray-900'} ${active==='b2' ? 'bg-indigo-600' : 'bg-white dark:bg-slate-400'} border border-gray-500 hover:bg-indigo-600 hover:text-white focus:z-10 focus:ring-2`}>
          ML
        </button>
        <button type="button" onClick={() => {handleFilterChange('Development'); setActive('b3')}} className={`w-40 px-4 py-2 text-sm font-medium ${active==='b3' ? 'text-white' :'text-gray-900'} ${active==='b3' ? 'bg-indigo-600' : 'bg-white dark:bg-slate-400'} border border-gray-500 hover:bg-indigo-600 hover:text-white focus:z-10 focus:ring-2 `}>
          Development
        </button>
        <button type="button" onClick={() => {handleFilterChange('Blockchain'); setActive('b4')}} className={`w-40 px-4 py-2 text-sm font-medium ${active==='b4' ? 'text-white' :'text-gray-900'} ${active==='b4' ? 'bg-indigo-600' : 'bg-white dark:bg-slate-400'} border border-gray-500 hover:bg-indigo-600 hover:text-white focus:z-10 focus:ring-2 `}>
          Blockchain
        </button>
        <button type="button" onClick={() => {handleFilterChange('CP'); setActive('b5')}} className={`w-40 px-4 py-2 text-sm font-medium ${active==='b5' ? 'text-white' :'text-gray-900'} ${active==='b5' ? 'bg-indigo-600' : 'bg-white dark:bg-slate-400'} border border-gray-500 hover:bg-indigo-600 hover:text-white focus:z-10 focus:ring-2 `}>
          CP
        </button>
        <button type="button" onClick={() => {handleFilterChange('Others'); setActive('b6')}} className={`w-40 px-4 py-2 text-sm font-medium ${active==='b6' ? 'text-white' :'text-gray-900'} ${active==='b6' ? 'bg-indigo-600' : 'bg-white dark:bg-slate-400'} border border-gray-500 rounded-e-lg hover:bg-indigo-600 hover:text-white focus:z-10 focus:ring-2 focus:ring-blue-700 `}>
          Others
        </button>
      </div>
    </div>
    {/* <div className="px-24  pt-10 grid grid-cols-1 gap-4 lg:grid-cols-3 lg:gap-8 ">
      <ProjectCard ProjectId="1" general_category="ML" link="https://itc.gymkhana.iitb.ac.in/wncc/assets/images/soc/2023/item221.jpg" title="TEXT SUMMARIZATION WEB APP"/>
      <ProjectCard ProjectId="2" general_category="Development" link="https://itc.gymkhana.iitb.ac.in/wncc/assets/images/soc/2023/item222.jpg" title="Competitive Programming"/>
      <ProjectCard ProjectId="3" general_category="Blockchain" link="https://itc.gymkhana.iitb.ac.in/wncc/assets/images/soc/2023/item226.png" title="Developing Trading Strategy with Pine Script"/>
      <ProjectCard ProjectId="4" general_category="CP" link="https://images.unsplash.com/photo-1524758631624-e2822e304c36?ixlib=rb-1.2.1&ixid=MnwxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80" title="How to position your furniture for positivity"/>
      <ProjectCard ProjectId="5" general_category="Others" link="https://images.unsplash.com/photo-1524758631624-e2822e304c36?ixlib=rb-1.2.1&ixid=MnwxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80" title="How to position your furniture for positivity"/>
    </div> */}
    {isLoading ? <div className="h-screen flex justify-center items-center">
        <div class="flex gap-2">
          <div class="w-5 h-5 rounded-full animate-pulse bg-blue-600"></div>
          <div class="w-5 h-5 rounded-full animate-pulse bg-blue-600"></div>
          <div class="w-5 h-5 rounded-full animate-pulse bg-blue-600"></div>
        </div>
      </div> : <div className="px-24 grid grid-cols-1 gap-4 lg:grid-cols-3 lg:gap-8 py-20">
    {/* {details.map((details, index) => (
      <div key={index}>
        <ProjectCard ProjectId={`project+${details.id}`} link={details.banner_image} title={details.title} description={details.props} />
      </div>
    ))} */}
    {filteredProjects.map((project, index) =>(
      <div key={index}>
        <ProjectCard ProjectId={project.id} link={project.banner_image} title={project.title} general_category={project.general_category} isInWishlist={wishlist.some((item) => item.id === project.id)}/>
      </div>
    ))}
    </div>}
    
  </section>);
}
