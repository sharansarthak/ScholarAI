// LearnPageCard.js
import React from "react";
import { Card, Col, Row } from "react-bootstrap";
import "../Styles/Learnpagecard.css";
import { styles } from "../styles"

const ResourceCard = ({ activity, description, link, image }) => {
  return (
    <div className="scholarship-card" style={{ background: '#FFEBE7', borderRadius: '35px', border:'solid', borderWidth:'10px', borderColor:'#FFC0BE', textAlign: 'left', padding: '18px', position: 'relative', marginBottom: '20px' }}>
      <div style={{ borderRadius: '20px', overflow: 'hidden', height: '90%', width:'80%', display: 'flex', justifyContent: 'center', alignItems: 'center', marginBottom: '0' }}>
          <img
            src={image} // Replace with the actual image URL
            alt="Activity Image"
            style={{ width: '100%', marginBottom: '5px', borderRadius: '20px', border:'solid', borderWidth:'7px', borderColor:'#FFC0BE'}}
          />
      </div>
      <div style={{display: 'flex', justifyContent: 'left', alignItems: 'left' }}>
      <h3 style={{ fontWeight: 'bold', color:'black', fontSize: '22px', textAlign: 'left', marginBottom: '15px', paddingTop: `15px` }} onClick={() => window.open(link, "_blank").focus()}>
        {activity}
      </h3>
      </div>
      <div style={{ padding: '10px' }}>
        <p className="description-text">
          {description && <span>{description}</span>}
        </p>
      </div>
    </div>
  );
};


export default ResourceCard;
