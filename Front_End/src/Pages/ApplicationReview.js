import { useEffect, useState } from "react";
import Axios from 'axios';
import '../Styles/ApplicationReview.css'
import { chatgptlogo } from "../Constants";
import chatgpt from '../assets/chatgpt.png'

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

export default function ApplicationReview() {
  const param1 = localStorage.getItem("ApplicationReviewTitle");
  const [scholarshipName, setScholarshipName] = useState(param1);
  const [scholarshipDescription, setScholarshipDescription] = useState("");
  const [questions, setQuestions] = useState([]);
  const [responses, setResponses] = useState([]);
  const [editingIndex, setEditingIndex] = useState(-1);
  const [editedText, setEditedText] = useState("");

  useEffect(() => {
    Axios.get("http://127.0.0.1:5000/get_all_scholarships?username=zeeshan", {})
      .then((res) => {
        const jsonData = res.data;
        if (jsonData.length > 0) {
          const scholarshipData = jsonData.find(item => item.Title === scholarshipName);
          if (scholarshipData) {
            setScholarshipDescription(scholarshipData.Description);
            setScholarshipName(scholarshipData.Title);
            setQuestions(scholarshipData.Questions);
            setResponses(scholarshipData.Answers);
          } else {
            console.error(`Scholarship with title ${scholarshipName} not found in jsonData`);
          }
        }
      })
      .catch((error) => {
        console.error("Error fetching scholarship description:", error);
      });
  }, [scholarshipName]); // Include scholarshipName as a dependency

  const handleEditClick = (index) => {
    setEditingIndex(index);
    setEditedText(responses[index]);
  };

  const handleSaveClick = async (index) => {
    const updatedResponses = [...responses];
    updatedResponses[index] = editedText;
    setResponses(updatedResponses);

    setEditingIndex(-1);
    setEditedText("");

    try {
      await Axios.post("http://127.0.0.1:5000/update_scholarship_answer", {
        username: "zeeshan",
        title: scholarshipName,
        index: index,
        updated_answer: editedText,
      });

      console.log("Post request successful");
    } catch (error) {
      console.error("Error sending post request:", error);
    }
  };

  const handleInputChange = (event) => {
    setEditedText(event.target.value);
  };

  const handleEnhanceClick = async (index) => {
    const enhancedResponse = await Axios.post("http://127.0.0.1:5000/get_enhanced_essay", {
      question: questions[index],
      answer: responses[index],
    });

    const updatedResponses = [...responses];
    updatedResponses[index] = enhancedResponse.data.response;
    setResponses(updatedResponses);
  };

  const handleSubmitClick = async () => {
    console.log(scholarshipName);
    try {
      await Axios.post("http://127.0.0.1:5000/submit_application", {
        username: "zeeshan",
        title: scholarshipName,
      });
      
      console.log("Submit responses successful");
    } catch (error) {
      console.error("Error submitting responses:", error);
    }
  };

  return (
    <div className="container">
      <div style={{ minHeight: `77vh`, textAlign: `left` }}>
        <div className="cardd">
          <div className={`${styles.heroHeadText}`} style={{ fontWeight: 'bold', fontSize: '50px', textAlign: 'center', marginBottom: '35px', paddingTop: `70px` }}>{scholarshipName}</div>
          <p className={`${styles.heroHeadText}`} style={{ fontSize: '25px', textAlign: 'center', marginBottom: '35px' }}>{scholarshipDescription}</p>
          <Container className="outer-container" style={{ minHeight: `100vh`, minWidth:`100vh` }}>
          <div className="questiondiv"  style={{ minHeight: `100vh`, minWidth:`100vh`, alignContent:`center`, alignItems:`center` }}>
            {questions.map((questionItem, index) => (
              <div key={index} className="question-container" style={{ display: 'flex', flexDirection:'column', alignItems: 'center', justifyContent: 'center' }}>
                <div style={{ width: "50rem", height: "100%", boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)', background: '#FFEBE7', margin: `1% 0`, border:'solid', borderWidth:'4px', borderColor:'#FF82A9', borderRadius: '15px', padding: '15px', position: 'relative', alignText: 'center', justifyContent: 'space-between'  }}>
                    <strong className={`${styles.heroHeadText}`} style={{ fontSize: '20px', textAlign: 'center', marginBottom: '35px' }}>Question:</strong> {questions[index]}
                    <br />
                </div>
                <div style={{ width: "50rem", height: "100%", boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)', background: '#FFEBE7', margin: `1% 0`, border:'solid', borderWidth:'4px', borderColor:'#FF82A9', borderRadius: '15px', padding: '15px', position: 'relative', alignText: 'center', justifyContent: 'space-between'  }}>
                <label htmlFor={`textInput-${index}`} className={`${styles.heroHeadText}`}  style={{ fontSize: '20px', fontWeight:'bold', textAlign: 'center'}} >Answer:</label>
                    {editingIndex === index ? (
                      <div >
                        <textarea
                          id={`textInput-${index}`}
                          name={`textInput-${index}`}
                          value={editedText}
                          onChange={handleInputChange}
                          rows={4}
                          style={{ width: '100%', background: 'black', padding: '10px', boxSizing: 'border-box' }}
                        />
                        <button className="invisiblePadding saveButton" style={{ marginRight: '10px', fontWeight:'bold', color:'black'  }} onClick={() => handleSaveClick(index)}>Save</button>
                      </div>
                    ) : (
                      <div className="answer-container" style={{ overflow: 'hidden' }}>
                        <p style={{ whiteSpace: 'pre-wrap', overflow: 'hidden' }}>{responses[index]}</p>
                        <div className="buttonContainer" style={{ display: 'flex', flexDirection:'row', alignItems: 'center', justifyContent: 'center' }}>
                          <span style={{ padding: '0 8px' }}></span>
                          <button className="invisiblePadding editButton" style={{ height:'58px', marginRight: '10px', fontWeight:'bold', color:'black'  }} onClick={() => handleEditClick(index)}>Edit</button>
                          <span style={{ padding: '0 8px' }}></span>
                          <button className="invisiblePadding enhanceButton" style={{ width: '140px', marginRight: '10px', fontWeight:'bold', color:'black', display:'flex', flex:'wrap'}}  onClick={() => handleEnhanceClick(index)}> <img src={chatgpt} alt="ChatGPT Icon" style={{ marginRight: '5px', height: '30px', width: '30px' }} /> Enhance</button>
                          <span style={{ padding: '0 8px' }}></span>
                        </div>
                      </div>
                    )}
                </div>
              </div>
      
            ))} 
          </div>
          </Container>
          <div style={{ textAlign: "center" }}>
            <button className="SignupButton"   style={{
                    backgroundColor: `#FFC0BE`,
                    color: `black`,
                    borderColor: `#FF82A9`,
                    borderWidth:'4px',
                    width:'400px',
                    borderRadius: '15px',
                    fontWeight:'bold',
                    marginBottom:'40px',
                  }} onClick={handleSubmitClick}>
              Submit
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
