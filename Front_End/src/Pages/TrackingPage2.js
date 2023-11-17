// TrackingPage2.js

import React, { useState, useEffect } from 'react';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import axios from 'axios';
import "../Styles/TrackingPage.css"

const API_BASE_URL = 'http://127.0.0.1:5000';

const TrackingPage2 = () => {
  const [applications, setApplications] = useState({
    in_progress: [],
    in_progress: [],
    interview: [],
    accepted: [],
    rejected: [],
  });

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

        console.log(response);

        // Categorize applications based on the 'status' key in the response
        response.data.forEach((application) => {
          const Status  = application.Status;
          console.log(Status);
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
    <DragDropContext onDragEnd={onDragEnd}>
      <div className="TrackingPage2">
        <div className="columns-container">
          {Object.keys(applications).map((column) => (
            <Droppable droppableId={column} key={column}>
              {(provided) => (
                <div
                  {...provided.droppableProps}
                  ref={provided.innerRef}
                  className="column"
                >
                  <h2>{column}</h2>
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
  );
};

export default TrackingPage2;
