import { useEffect, useState } from "react";
import { Container, Form, FormLabel, Row, Card, Modal, Button, Col } from "react-bootstrap";
import Axios from 'axios';
import "../Styles/ApplicationReview.css";

export default function ApplicationReview() {
  const [scholarshipName, setscholarshipName] = useState("");
  const [scholarshipDescription, setscholarshipDescription] = useState("");
  const [questions, setQuestions] = useState([]);
  const [responses, setResponses] = useState([]);
  const [editingIndex, setEditingIndex] = useState(-1);
  const [editedText, setEditedText] = useState("");

  useEffect(() => { 
    Axios.get("http://127.0.0.1:5000/get_all_scholarships?username=zeeshan", {})
      .then((res) => {
        const jsonData = res.data;
        if (jsonData.length > 0) {
          setscholarshipDescription(jsonData[0].Description);
          setscholarshipName(jsonData[0].Title);
          setQuestions(jsonData[0].Questions);
          setResponses(jsonData[0].Answers);
        };
      })
      .catch((error) => {
        console.error("Error fetching scholarship description:", error);
      });
  }, []);

  const handleEditClick = (index) => {
    setEditingIndex(index);
    setEditedText(responses[index]);
  };

  const handleSaveClick = async (index) => {
    // Save the edited text, you can perform any save/update logic here
    const updatedResponses = [...responses];
    updatedResponses[index] = editedText;
    setResponses(updatedResponses);

    // Reset editing state
    setEditingIndex(-1);
    setEditedText("");
    
    // Send a POST request to update the server
    try {
      await Axios.post("http://127.0.0.1:5000/update_scholarship_answer", {
        username: "zeeshan",
        questionIndex: index, // Assuming the server expects the question index
        answer: editedText,
      });

      // Handle success if needed
      console.log("Post request successful");
    } catch (error) {
      console.error("Error sending post request:", error);
      // Handle error if needed
    }
  };

  const handleInputChange = (event) => {
    setEditedText(event.target.value);
  };

  const handleEnhanceClick = (index) => {
    // Send a Get Request to the backend server and receive an enhanced answer
    Axios.get("http://127.0.0.1:5000/get_all_scholarships?username=zeeshan", {})
      .then((res) => {
        // Create a copy of the responses array
        const updatedResponses = [...responses];
        
        // Modify the specific element in the copied array
        // For example, setting the response at the given index to the enhanced answer
        updatedResponses[index] = res.data;

        // Update the state with the modified array
        setResponses(updatedResponses);
      })
      .catch((error) => {
        console.error("Error getting enhanced Answer back from the server", error);
      });
  };

  const handleSubmitClick = async () => {
    // Send a request to the server to submit the responses
    try {
      await Axios.post("http://127.0.0.1:5000/submit_responses", {
        username: "zeeshan",
        responses: responses,
      });

      // Handle success if needed
      console.log("Submit responses successful");
    } catch (error) {
      console.error("Error submitting responses:", error);
      // Handle error if needed
    }
  };

  return (
    <div style={{ minHeight: `77vh`, textAlign: `left` }}>
      <div className="card">
        <div className="SalaryHeader">{scholarshipName}</div>
        <p>{scholarshipDescription}</p>
        <div className="questiondiv">
          {questions.map((questionItem, index) => (
            <div key={index}>
              <strong className="ColumnSubHeader">Question:</strong> {questions[index]}
              <br />
              <label htmlFor={`textInput-${index}`} className="ColumnSubHeader">Answer:</label>
              {editingIndex === index ? (
                <div>
                  <input
                    type="text"
                    id={`textInput-${index}`}
                    name={`textInput-${index}`}
                    value={editedText}
                    onChange={handleInputChange}
                  />
                  <button onClick={() => handleSaveClick(index)}>Save</button>
                </div>
              ) : (
                <div>
                  <p>{responses[index]}</p>
                  <button onClick={() => handleEditClick(index)}>Edit</button>
                  <button onClick={() => handleEnhanceClick(index)}>Enhance</button>
                </div>
              )}
            </div>
          ))}
        </div>
        <Button onClick={handleSubmitClick}>Submit Responses</Button>
      </div>
    </div>
  );
}
