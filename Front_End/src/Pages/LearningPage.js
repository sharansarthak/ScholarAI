import React, { useEffect, useState } from "react";
import Axios from "axios";
import { Container, Row } from "react-bootstrap";
import ResourceCard from "./LearnPageCard";

// import "../Styles/SalariesPageStyles.css";
import "../Styles/LearningPageStyles.css";
// import "../Styles/LearningPageStyles.css"; // Import the new CSS file here

export default function LearningPage() {
  const [resourceList, setResourceList] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await Axios.get(
          "http://127.0.0.1:5000/get_all_resources?username=zeeshan",
          {}
        );
        setResourceList(response.data);
      } catch (error) {
        console.error("Error in getting resources for learning page", error);
      }
    };

    fetchData();
  }, []); 

  return (
    <Container style={{ textAlign: `left` }}>
      <h1 className="SalaryHeader">Improve Your Skills!</h1>
      <div className="learnPageCards"> 
      {resourceList?.map((resource, index) => (
        <div key={index}>
          <h2 className="SubHeader">{resource.category}</h2>
          <div className="learnPageCards2"> 
          {resource.activities?.map((value, valueIndex) => (
            <Row key={valueIndex}>
              <ResourceCard
                activity={value.activity}
                link={value.link}
                description={value.description}
              />
            </Row>
          ))}
          </div>
        </div>
      ))}
      </div>
    </Container>
  );
}
