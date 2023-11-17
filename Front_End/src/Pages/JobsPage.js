import Axios from "axios";
import { useEffect, useState } from "react";
import Switch from "react-switch";
import {
  Container,
  DropdownButton,
  Dropdown,
  Row,
  Form,
  FormLabel,
  Button,
  Card,
  Modal,
  Col,
} from "react-bootstrap";

// import { Tilt } from "react-tilt";

import "../Styles/JobsPageStyles.css";
import "../Styles/SearchBar.css";
import "../Styles/VerticalMenu.css";
import ApplicationReview from "./ApplicationReview";
import { styles } from "../styles"


export default function JobsPage() {
  const [jobs, setJobsToShow] = useState([]);
  const [resultsToShow, setResultsToShow] = useState([]);
  const [showApplyJob, setShowApplyJob] = useState(false);
  const [currJob, setCurrJob] = useState({});
  const [documents, setDocuments] = useState([]);
  const [showAddDoc, setShowAddDoc] = useState(false);
  const [resume, setResume] = useState();
  const [coverLetter, setCoverLetter] = useState();
  const [scholarships, setScholarships] = useState();
  const [eligibleScholarshipSwitch, setEligibleScholarshipSwitch] = useState(false);
  const [myInstitutionSwitch, setMyInstitutionSwitch ] = useState(false);
  const [needSwitch, setneedSwitch ] = useState(false);
  const [meritSwitch, setmeritSwitch ] = useState(false);
  const [deadlineSwitch, setdeadlineSwitch ] = useState(false);

  const eligibleScholarshipSwitchHandler = (checked) => {
    setEligibleScholarshipSwitch(checked);
  };

  const myInstitutionSwitchHandler = (checked) => {
    setMyInstitutionSwitch(checked);
  };

  const needSwitchHandler = (checked) => {
    setneedSwitch(checked);
  };
  const meritSwitchHandler = (checked) => {
    setmeritSwitch(checked);
  };
  const deadlineSwitchHandler = (checked) => {
    setdeadlineSwitch(checked);
  };

  useEffect(() => {
    // Checks for token in storage, indicating signed in.
    // if(localStorage.getItem("token") == null){
    //   window.location.href = "http://localhost:3000/login";
    // }
    const fetchData = async () => {
      try {
        const response = await Axios.get("https://www.scholarshipappplication.online/get_all_scholarships_brief?username=zeeshan", {
        })
        console.log(response);
        setScholarships(response.data);
        // setResourceList(response.data);
      } catch (error) {
        console.error("Error in getting resources for Scholarship page", error);
      }
    };

    fetchData();

    Axios.get("http://127.0.0.1:5000/api/jobPostings", {})
    .then((res) => {
      console.log(res)
      setJobsToShow(res.data);
      setResultsToShow(res.data);
    })
    
    Axios.get("http://127.0.0.1:5000/api/getUserDocumentsNames", {
      params: {
        token: localStorage.getItem("token"),
      }
    })
    .then((res) => {
      setDocuments(res.data);
    })
    
  }, [])

  const redirectToApplicationReview = (applicationTitle) => {
    localStorage.setItem("ApplicationReviewTitle",applicationTitle);
    // Reloads the current page
    window.location.reload();
    // Redirects to the main page
    window.location.href = "http://localhost:3000/applicationReview";
  };

  function handleCloseAddDoc() {
    setShowAddDoc(false);
  }

  function handleCloseApplyJob() {
    setShowApplyJob(false);
  }

  function handleSearch(e) {
    if (e === "Enter") {
      let query = document.getElementById("searchBar").value.toLowerCase();
      if (query === "") {
        setResultsToShow(jobs);
      } else {
        let res = jobs.filter((job) => {
          if (
            job.companyName.toLowerCase() === query ||
            job.industry.toLowerCase() === query ||
            job.Title.toLowerCase() === query
          ) {
            return true;
          } else {
            return false;
          }
        });

        if (res.length === 0) {
          document.getElementById("errorMessage").classList.add("ShowError");
        } else {
          document.getElementById("errorMessage").classList.remove("ShowError");
          setResultsToShow(res);
        }
      }
    }
  }

  function apply(id) {
    setCurrJob(jobs.find((job) => (job.id = id)));
    setShowApplyJob(true);
  }

  function applyForJob(id, resumeDNo, coverDno) {
    let temp = [resumeDNo];
    if(coverDno !== ""){
      temp.push(coverDno);
    }
    console.log(temp)
    Axios.post("http://127.0.0.1:5000/api/apply", {
      token: localStorage.getItem("token"),
      JobID: id,
      dNo:  temp,
    })
    setShowApplyJob(false);
  }
  
  function submitDocuments(resume, coverLetter){
    if(resume !== undefined){
      let formData = new FormData();
      formData.append("file", resume[0]);
      Axios.post("http://127.0.0.1:5000/api/addUserDocument", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          token: localStorage.getItem("token"),
          type: "resume",
        }
      })
    }

    if(coverLetter !== undefined){
      let formData1 = new FormData();
      formData1.append("file", coverLetter[0]);
      Axios.post("http://127.0.0.1:5000/api/addUserDocument", formData1, {
        headers: {
          'Content-Type': 'multipart/form-data',
          token: localStorage.getItem("token"),
          type: "coverLetter",
        }
      })
    }

    setShowAddDoc(false);
  }

  
  // const ScholarshipCard = ({
  //   name,
  //   company,
  //   tags,
  //   image,
  //   deadline,
  //   time,
  // }) => {
  //   return (
  //       <div
  //         className='bg-tertiary p-5 rounded-2xl sm:w-[360px] w-full'
  //       >
  //         <div className='relative w-full h-[230px]'>
  //           <img
  //             src={image}
  //             alt='project_image'
  //             className='w-full h-full object-cover rounded-2xl'
  //           />
  
  //           <div className='absolute inset-0 flex justify-end m-3 card-img_hover gap-1'>
  //             <div
  //               onClick={() => window.open(source_code_link, "_blank")}
  //               className='black-gradient w-10 h-10 rounded-full flex justify-center items-center cursor-pointer'
  //             >
  //               <img
  //                 src={icon}
  //                 alt='source code'
  //                 className='w-1/2 h-1/2 object-contain'
  //               />
  //             </div>
  //           </div>
  //         </div>
  
  //         <div className='mt-5'>
  //           <h3 className='text-white font-bold text-[24px]'>{name}</h3>
  //           <p className='mt-2 text-secondary text-[14px]'>{Company}</p>
  //         </div>
  
  //         <div className='mt-4 flex flex-wrap gap-2'>
  //           {tags.map((tag) => (
  //             <p
  //               key={`${name}-${tag.name}`}
  //               className={`text-[14px] font-bold ${tag.color}`}
  //             >
  //               #{tag.name}
  //             </p>
  //           ))}
  //         </div>
  //       </div>
  //   );
  // };

  const SearchBar = () => {
    const [searchQuery, setSearchQuery] = useState('');
  
    const handleSearchChange = (e) => {
      setSearchQuery(e.target.value);
    };
  
    const handleSearchSubmit = (e) => {
      e.preventDefault();
      // Add your search logic here
      console.log('Search Query:', searchQuery);
      // You can perform your search operation with the searchQuery
    };
  
    return (
      <div className="search-container">
        <form onSubmit={handleSearchSubmit} className="search-form">
          <input
            type="text"
            value={searchQuery}
            onChange={handleSearchChange}
            placeholder="Enter your search..."
            style={{ width: '75%', color:`black` }}
          />
          <button type="submit" style={{ fontWeight: 'bold' }}>Search</button>
        </form>
      </div>
    );
  };

  

  return (
    <Container style={{ minHeight: `100vh` }}>
      <Row>
        {/* Left Side Vertical Menu */}
        <Col md={2} className="vertical-menu">
          <ul>
            <li>
              Eligible Scholarships
              <Switch
                onChange={eligibleScholarshipSwitchHandler}
                checked={eligibleScholarshipSwitch}
                onColor="#FFC0BE"
                onHandleColor="#FF82A9"
                handleDiameter={30}
                uncheckedIcon={false}
                checkedIcon={false}
                height={20}
              />
            </li>
            <li>
              My Institution
              <Switch
                onChange={myInstitutionSwitchHandler}
                checked={myInstitutionSwitch}
                onColor="#FFC0BE"
                onHandleColor="#FF82A9"
                handleDiameter={30}
                uncheckedIcon={false}
                checkedIcon={false}
                height={20}
              />
            </li>
            <li>
              Need-Based
              <Switch
                onChange={needSwitchHandler}
                checked={needSwitch}
                onColor="#FFC0BE"
                onHandleColor="#FF82A9"
                handleDiameter={30}
                uncheckedIcon={false}
                checkedIcon={false}
                height={20}
              />
            </li>
            <li>
              Merit-Based
              <Switch
                onChange={meritSwitchHandler}
                checked={meritSwitch}
                onColor="#FFC0BE"
                onHandleColor="#FF82A9"
                handleDiameter={30}
                uncheckedIcon={false}
                checkedIcon={false}
                height={20}
              />
            </li>
            <li>
              Deadline Soon
              <Switch
                onChange={deadlineSwitchHandler}
                checked={deadlineSwitch}
                onColor="#FFC0BE"
                onHandleColor="#FF82A9"
                handleDiameter={30}
                uncheckedIcon={false}
                checkedIcon={false}
                height={20}
              />
            </li>
            {/* Add more menu items as needed */}
          </ul>
        </Col>

        {/* Right Side Content */}
        <Col md={10} style={{ paddingLeft: `50px`, marginBottom:`90px`}}>
        <h1 className={`${styles.heroHeadText}`} style={{ fontWeight: 'bold', fontSize: '50px', textAlign: 'center', marginBottom: '35px', paddingTop:`70px` }}>Scholarships</h1>
        <div style={{width:'100%'}}>
          <SearchBar />
        </div>
        <Row style={{ justifyContent: `space-evenly`, gap:`25px` }}>
            {scholarships?.map((scholarship) => {
              return (
                <div key={scholarship.id} className="scholarship-card" style={{ width: "20rem", height:"100%", background: '#FFFFFF', margin: `1% 0`, borderRadius: '35px', textAlign: 'center', padding: '11px', position: 'relative' }}>
                {/* Centered Image */}
                <img
                  src={scholarship.Image} // Replace with the actual image URL
                  alt="Scholarship Logo"
                  style={{ width: '30%', marginBottom: '5px' }}
                />
              
                <Card.Body style={{ cursor: `pointer`, display:`flex`, flexDirection:'column' }} onClick={() => redirectToApplicationReview(scholarship.Title)}>
                  <Card.Title>{scholarship.Title}</Card.Title>
                  <Card.Subtitle className="mb-2 text-muted">
                    {scholarship.Institution}
                  </Card.Subtitle>
                  <div style={{ margin: '15px 0' }}>
                    {scholarship.Requirements.map((requirement, index) => (
                      <p key={index}  className="requirement-text">
                        #{requirement}
                      </p>
                    ))}
                  </div>
                  <div style={{ position: 'relative', bottom: '0', left: '0', width: '100%', borderTop: '1px solid #ccc', padding: '10px', borderRadius: '0px' }}>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gridGap: '0px' }}>
                      <div style={{ borderBottom: '1px solid #d3d3d3', borderRight: '1px solid #d3d3d3', padding: '10px' }}>💸{scholarship["Scholarship Amount"]}</div>
                      <div style={{ borderBottom: '1px solid #d3d3d3', padding: '10px' }}>📆​ {scholarship.Deadline}</div>
                      <div style={{ borderRight: '1px solid #d3d3d3', padding: '10px' }}>⌛​ {scholarship["Estimated Completion Time"]}</div>
                      <div style={{ padding: '10px' }}>📜 Upto {scholarship["Number of Recipients"]} Recipients</div>
                    </div>
                  </div>
                </Card.Body>
              </div>  
         
              );
            })}
          </Row>
        </Col>
      </Row>
    </Container>
  );
}