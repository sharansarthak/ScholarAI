// TrackingPage2.js

import React, { useState, useEffect } from 'react';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import axios from 'axios';
import "../Styles/TrackingPage.css"
import ApplicationReview from "./ApplicationReview";
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
import { styles } from "../styles"

const API_BASE_URL = 'http://127.0.0.1:5000';

const TrackingPage2 = () => {
  const [applications, setApplications] = useState({
    applied: [],
    in_progress: [],
    interview: [],
    accepted: [],
    rejected: [],
  });

    const redirectToApplicationReview = (applicationTitle) => {
    localStorage.setItem("ApplicationReviewTitle",applicationTitle);
    // Reloads the current page
    window.location.reload();
    // Redirects to the main page
    window.location.href = "http://localhost:3000/applicationReview";
  };

  const Get_Title_Name = (given_name) => {
    switch (given_name) {
      case "applied":
        return "Applied";
      case "in_progress":
        return "In Progress";
      case "interview":
        return "Interview";
      case "accepted":
        return "Accepted";
      case "rejected":
        return "Rejected";
      default:
        return given_name; // return the given name if it doesn't match any case
    }
  };

  useEffect(() => {
    // Fetch scholarship applications from the backend
    axios.get(`${API_BASE_URL}/get_all_scholarships?username=zeeshan`)
      .then((response) => {
        const categorizedApplications = {
          applied: [],
          in_progress: [],
          interview: [],
          accepted: [],
          rejected: [],
        };

        // console.log(response);

        // Categorize applications based on the 'status' key in the response
        response.data.forEach((application) => {
          const Status  = application.Status;
        //   console.log(Status);
          categorizedApplications[Status].push(application);
        });

        // Set the categorized applications to the state
        setApplications(categorizedApplications);
      })
      .catch((error) => {
        console.error('Error fetching scholarship applications:', error);
      });
  }, []);

  const onDragEnd = async (result) => {
    const { destination, source, draggableId } = result;

    // Check if the item was dropped outside any valid droppable area
    if (!destination) {
      return;
    }

    // If the item was dropped in a different column
    if (destination.droppableId !== source.droppableId) {
      const updatedApplications = { ...applications };
      const sourceColumn = updatedApplications[source.droppableId];
      const destinationColumn = updatedApplications[destination.droppableId];
      const movedApplication = sourceColumn.find(
        (app) => app.id === draggableId
      );

      // Remove from the source column
      sourceColumn.splice(source.index, 1);

      // Add to the destination column
      destinationColumn.splice(destination.index, 0, movedApplication);

      // Update the state
      setApplications(updatedApplications);

      // Update the backend
      await axios.post(`${API_BASE_URL}/update_status`, {
        username: 'zeeshan',
        title: movedApplication.Title,
        new_status: destination.droppableId,
      });
    }
  };

  return (
    <Container style={{ minHeight: `100vh`, minWidth:`100vh` }}>
      <DragDropContext onDragEnd={onDragEnd}>
        <div className="TrackingPage2">
          <div className="columns-container ">
            {Object.keys(applications).map((column) => (
              <Droppable droppableId={column} key={column}>
                {(provided) => (
                  <div
                    {...provided.droppableProps}
                    ref={provided.innerRef}
                    className="column"
                  >
                    <h2 className={`${styles.SubHeader}`} style={{ fontWeight: 'bold', fontSize: '28px', textAlign: 'center', paddingTop: `15px`, paddingBottom:`10px`, fontWeight:`bolder`, color:`#7F95D1`}}>{Get_Title_Name(column)}</h2>
                    {applications[column].map((application, index) => (
                      <Draggable
                        key={application.id}
                        draggableId={application.id}
                        index={index}
                      >
                        {(provided) => (
                          <div
                            ref={provided.innerRef}
                            {...provided.draggableProps}
                            {...provided.dragHandleProps}
                            className="card"
                            onClick={() => redirectToApplicationReview(application.Title)}
                          >
                            <p>{application.Title}</p>
                            {/* Add more details if needed */}
                          </div>
                        )}
                      </Draggable>
                    ))}
                    {provided.placeholder}
                  </div>
                )}
              </Droppable>
            ))}
          </div>
        </div>
      </DragDropContext>
    </Container>
  );
  
};

export default TrackingPage2;
