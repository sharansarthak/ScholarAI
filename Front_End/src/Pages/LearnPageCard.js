// LearnPageCard.js
import React from "react";
import { Card, Col, Row } from "react-bootstrap";
import "../Styles/Learnpagecard.css";

const ResourceCard = ({ activity, description, link }) => {
  return (
    <Card className="resourceCard">
      <Card.Header>
        <Card.Title>
          <Row>
            <Col onClick={() => window.open(link, "_blank").focus()}>
              {activity}
            </Col>
          </Row>
        </Card.Title>
      </Card.Header>
      <Card.Body>
        <Card.Text>
          {description && <span>Description: {description}</span>}
        </Card.Text>
      </Card.Body>
    </Card>
  );
};

export default ResourceCard;
