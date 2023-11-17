import React, { useEffect, useState } from "react";
import Axios from "axios";
import ResourceCard from "./LearnPageCard";
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

// import "../Styles/SalariesPageStyles.css";
import "../Styles/LearningPageStyles.css";
// import "../Styles/LearningPageStyles.css"; // Import the new CSS file here
import { styles } from "../styles"

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
      <Container style={{ minHeight: `100vh`, minWidth:`100vh` }}>
        <h1 className={`${styles.heroHeadText}`} style={{ fontWeight: 'bold', fontSize: '50px', textAlign: 'center', marginBottom: '35px', paddingTop: `70px` }}>Improve Your Skills!</h1>
        <Col style={{ marginBottom: `90px`, padding:`20px` }}>
          <div style={{ width: '100%' }}>
            {/* Add any relevant components or elements here */}
          </div>
          {resourceList?.map((resource, index) => (
            <div key={index} className="scholarship-card" style={{ background: '#FFFFFF', margin: `1% 0`, borderRadius: '35px', textAlign: 'left', padding: '35px', marginLeft:'20px', marginRight:'20px',  position: 'relative' }}>
              <h2 className={`${styles.SubHeader}`} style={{ fontWeight: 'bold', fontSize: '35px', textAlign: 'center', paddingTop: `15px` }}>{resource.category}</h2>
              <h3 className={`${styles.SubHeader}`} style={{ fontWeight: 'bold', color:'#6D84C6', fontSize: '22px', textAlign: 'center', marginBottom: '35px', paddingTop: `5px` }}>courses for you to enhance your skillset</h3>
          
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gridGap: '0px' }}>
                {resource.activities?.map((value, valueIndex) => (
                  <div key={valueIndex} style={{ padding: '15px' }}>
                    <ResourceCard
                      activity={value.activity}
                      link={value.link}
                      description={value.description}
                      image={value.image}
                    />
                  </div>
                ))}
              </div>
            </div>
          ))}
        </Col>
      </Container>

  );
}
