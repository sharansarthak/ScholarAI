import { useEffect, useState } from "react";
import {
  Container,
  Form,
  FormLabel,
  Row,
  Card,
  Modal,
  Button,
  Col,
} from "react-bootstrap";
import Axios from 'axios';
import "../Styles/ApplicationReview.css";

const exampleDataPopular = [
  {
    scholarshipName: "Google Scholarship",
    description: "A scholarship is a financial award provided to individuals based on their academic achievements, talents, or specific characteristics. This form of educational funding is designed to support students in pursuing their academic goals by alleviating the financial burden associated with tuition, books, and other educational expenses. Scholarships can be merit-based, focusing on academic excelle",
    questions: [
      { question: "what is your favorite sport?" },
      { question: "how old are you ?" },
      { question: "what is your favourite activity?" }
    ],
    responses: [
        { response: "blah blah blah 0" },
        { response: "blah blah blah 1" },
        { response: "blah blah blah 2" }
    ],
  }]
;

export default function ApplicationReview() {

    const [scholarshipName, setscholarshipName] = useState("");
    const [scholarshipDescription, setscholarshipDescription] = useState("");
    const [questions, setQuestions] = useState([]);
    const [responses, setResponses] = useState([]);


    useEffect(() => { 
            // Checks for token in storage, indicating signed in.
        // if(localStorage.getItem("token") == null){
        //   window.location.href = "http://127.0.0.1:5000/login";
        // }

        Axios.get("http://127.0.0.1:5000/get_all_scholarships", {})
        .then((res) => {
          const jsonData = res.data;
      
          if(jsonData.length > 0){
              setscholarshipDescription(jsonData[0].Title);
              setscholarshipName(jsonData[0].Title);
              setQuestions(jsonData[0].Questions);
              setResponses(jsonData[0].Answers);
              console.log(scholarshipName,scholarshipDescription);
          };

        // for (let i = 0; i < questions.length; i++){
        //     console.log(questions[i]);
        // };

        })
        .catch((error) => {
        console.error("Error fetching scholarship description:", error);
        });


    }, []);

    return (
        <div style={{ minHeight: `77vh`, textAlign: `left` }}>
            <div className="card">
                <div className="SalaryHeader">{scholarshipName}</div>
                <p>{scholarshipDescription}</p>
                <div className="questiondiv">
                    {questions.map((questionItem, index) => (
                    <li key={index}>
                    <strong className="ColumnSubHeader">Question:</strong> {questionItem.question}
                    <br />
                    <strong className="ColumnSubHeader" >Answer:</strong> {responses[index].response}
                    </li>
                    ))}
                </div>
            </div>
        </div>
      );
}
