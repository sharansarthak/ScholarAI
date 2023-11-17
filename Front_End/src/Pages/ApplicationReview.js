import { useEffect, useState } from "react";
import { Button } from "react-bootstrap";
import Axios from 'axios';

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
    try {
      await Axios.post("http://127.0.0.1:5000/submit_responses", {
        username: "zeeshan",
        responses: scholarshipName,
      });

      console.log("Submit responses successful");
    } catch (error) {
      console.error("Error submitting responses:", error);
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
